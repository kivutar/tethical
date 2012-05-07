from Config import *
import direct.directbase.DirectStart
from panda3d.core import *
from direct.gui.DirectGui import *
from direct.task.Task import Task
from direct.distributed.PyDatagramIterator import *
from direct.distributed.PyDatagram import *
from direct.interval.IntervalGlobal import *
import math
from operator import itemgetter
import json
import GUI
from CameraHandler import *
from DirectionChooser import *
from BattleGraphics import *
from Sky import *
from Matrix import *
from Cursor import *
from AT import *
from Send import *
from Controllers import *
from KeyboardTileTraverser import *
import SequenceBuilder

class Client(object):

    def __init__(self):
        self.music = base.loader.loadSfx(GAME+'/music/24.ogg')
        self.music.setLoop(True)
        self.music.play()
        self.background = GUI.Background(self.loginScreen)

    # Display the login window
    def loginScreen(self):
        self.loginwindow = GUI.LoginWindow(self.authenticate)

    def processData(self, datagram):
        iterator = PyDatagramIterator(datagram)
        source = datagram.getConnection()
        callback = iterator.getString()
        getattr(globals()[callback], 'execute')(self, iterator)

    # This task process data sent by the server, if any
    def tskReaderPolling(self, taskdata):
        if self.cReader.dataAvailable():
            datagram=NetDatagram()
            if self.cReader.getData(datagram):
                self.processData(datagram)
        return Task.cont

    # Setup connection and send the LOGIN datagram with credentials
    def authenticate(self):
        login = self.loginwindow.loginEntry.get()
        password = self.loginwindow.passwordEntry.get()

        self.cManager  = QueuedConnectionManager()
        self.cListener = QueuedConnectionListener(self.cManager, 0)
        self.cReader   = QueuedConnectionReader(self.cManager, 0)
        self.cReader.setTcpHeaderSize(4)

        self.myConnection = self.cManager.openTCPClientConnection(IP, PORT, 5000)
        if self.myConnection:
            self.cReader.addConnection(self.myConnection)
            self.send = Send(self.cManager, self.myConnection)
            print 'Client listening on', IP, ':', PORT
            taskMgr.add(self.tskReaderPolling, "Poll the connection reader")

            self.send.LOGIN_MESSAGE(login, password)

        else:
            print 'Can\'t connect to server on', IP, ':', PORT

    # The battle begins
    def battle_init(self):
        self.subphase = None

        # Instanciate the camera handler
        self.camhandler = CameraHandler()

        # Instanciate the keyboard tile traverser
        self.inputs = KeyboardTileTraverser(self)

        # Instanciate the battle graphics
        self.battleGraphics = BattleGraphics(self.party['map'])
        
        # Light the scene
        self.battleGraphics.lightScene()
        
        # Display the terrain
        self.battleGraphics.displayTerrain()
        
        # Play the background music
        self.music = base.loader.loadSfx(GAME+'/music/'+self.party['map']['music']+'.ogg')
        self.music.setLoop(True)
        self.music.play()
        
        # Load sounds
        self.hover_snd   = base.loader.loadSfx(GAME+"/sounds/hover.ogg")
        self.clicked_snd = base.loader.loadSfx(GAME+"/sounds/clicked.ogg")
        self.cancel_snd  = base.loader.loadSfx(GAME+"/sounds/cancel.ogg")
        self.attack_snd  = base.loader.loadSfx(GAME+"/sounds/attack.ogg")
        self.die_snd     = base.loader.loadSfx(GAME+"/sounds/die.ogg")
        
        # Place highlightable tiles on the map
        self.matrix = Matrix(self.battleGraphics, self.party['map'])
        self.matrix.placeChars(self.party['chars'])
        
        # Instanciate and hide the AT flag
        self.at = AT()
        self.at.hide()
        
        self.charbars = None
        self.charcard = None
        self.actionpreview = None

        # Generate the sky and attach it to the camera
        self.sky = Sky(self.party['map'])

        # Tasks
        taskMgr.add(self.characterDirectionTask , 'characterDirectionTask')

        # Cursor stuff
        self.cursor = Cursor(self.battleGraphics, self.matrix.container)

        # Add the special effects
        self.battleGraphics.addEffects()

        # Battle intro animation
        SequenceBuilder.battleIntroduction(self).start()

    def updateAllSpritesAnimations(self, animation):
        for i,charid in enumerate(self.matrix.sprites):
            Sequence(
                Wait(float(i)/6.0),
                Func(self.updateSpriteAnimation, charid, animation),
            ).start()

    def end(self):
        taskMgr.remove('characterDirectionTask')
        for child in render.getChildren():
            child.removeNode()
        self.camhandler.destroy()
        self.coords.destroy()
        self.sky.remove()
        self.background = GUI.Background(self.send.GET_PARTIES)

    def showMenu(self, charid):
        self.inputs.ignoreAll()
        self.camhandler.ignoreAll()

        canmove = self.party['chars'][charid]['canmove']
        canact  = self.party['chars'][charid]['canact']

        columns = [ { 'x': -25, 'font': GUI.regularfont, 'align': TextNode.ALeft   }, ]

        rows = [
            { 'cells': ['Move'        ], 'enabled': canmove, 'callback': lambda: self.send.GET_WALKABLES  (charid) },
            { 'cells': ['Act'         ], 'enabled': canact , 'callback': lambda: self.onAttackClicked(charid) },
            { 'cells': ['Wait'        ], 'enabled': True   , 'callback': lambda: self.onWaitClicked  (charid) },
            { 'cells': ['Status'      ], 'enabled': False  , 'callback': lambda: self.onWaitClicked  (charid) },
            { 'cells': ['Auto-Battle' ], 'enabled': False  , 'callback': lambda: self.onWaitClicked  (charid) },
        ]

        GUI.ScrollableList(
            'shadowed', 73, -8, 62.0, 91.0, 16, 
            columns, rows, 5, 
            lambda: self.onCancelClicked(charid), 
            'Menu'
        )

    def moveCheck(self, charid, orig, origdir, dest):
        self.inputs.ignoreAll()
        self.camhandler.ignoreAll()
        GUI.MoveCheck(
            lambda: self.send.MOVE_TO(charid, dest),
            lambda: self.cancelMove(charid, orig, origdir)
        )

    def cancelMove(self, charid, orig, origdir):
        self.matrix.sprites[charid].node.setPos(self.battleGraphics.logic2terrain(orig))
        self.matrix.sprites[charid].setRealDir(origdir)
        self.send.UPDATE_PARTY()

    # Makes a character look at another one
    def characterLookAt(self, charid, targetid):
        (x1, y1, z1) = self.matrix.getCharacterCoords(charid)
        (x2, y2, z2) = self.matrix.getCharacterCoords(targetid)
        if x1 > x2:
            self.matrix.sprites[charid].setRealDir(3)
        if x1 < x2:
            self.matrix.sprites[charid].setRealDir(1)
        if y1 > y2:
            self.matrix.sprites[charid].setRealDir(4)
        if y1 < y2:
            self.matrix.sprites[charid].setRealDir(2)

    # Update the status (animation) of a sprite after something happened
    def updateSpriteAnimation(self, charid, animation=False):
        if animation:
            self.matrix.sprites[charid].animation = animation
        else:
            stats = self.party['chars'][charid]
            if stats['hp'] >= (stats['hpmax']/2):
                self.matrix.sprites[charid].animation = 'walk'
            if stats['hp'] < (stats['hpmax']/2):
                self.matrix.sprites[charid].animation = 'weak'
            if stats['hp'] <= 0:
                self.matrix.sprites[charid].animation = 'dead'
                self.die_snd.play()
        h = self.camhandler.container.getH()
        self.matrix.sprites[charid].updateDisplayDir( h, True )

### Events

    def updateCursorPos(self, pos):

        self.camhandler.move(self.battleGraphics.logic2terrain(pos))

        (x, y, z) = pos
        tile = self.party['map']['tiles'][x][y][z]

        self.cursor.move(x, y, z, tile)

        if self.charbars:
            self.charbars.hide()

        if self.party['map']['tiles'][x][y][z].has_key('char'):
            charid = self.party['map']['tiles'][x][y][z]['char']
            char = self.party['chars'][charid]
            if self.subphase == 'attack':
                self.charbars = GUI.CharBarsRight(char)
            else:
                self.charbars = GUI.CharBarsLeft(char)

        try:
            self.coords.update(tile)
        except:
            self.coords = GUI.Coords(tile)

    # Returns the closest tile for the given x and y
    # Keyboard related callback, move this to the KeyboardTileTraverser
    def findTileAndUpdateCursorPos(self, pos):
        fux, fuy = pos

        # list the possibles tiles, on official maps, this list should not excess 2 items
        possibles = []
        for x,xs in enumerate(self.party['map']['tiles']):
            for y,ys in enumerate(xs):
                for z,zs in enumerate(ys):
                    if not self.party['map']['tiles'][x][y][z] is None:
                        if fux == x and fuy == y:
                            d = math.fabs(z-self.cursor.z) # for each possible, compute the Z delta with the current tile
                            possibles.append((x, y, z, d))

        if len(possibles):
            # sort the possibles on Z delta, and get the closer tile
            selected = sorted(possibles, key=itemgetter(3))[0][0:3]

            self.hover_snd.play()
            self.updateCursorPos(selected)

    # Battle func
    def setupWalkableTileChooser(self, charid, walkables):
        self.inputs.acceptAll()
        self.camhandler.acceptAll()
        self.subphase = 'move'
        self.matrix.setupWalkableZone(charid, walkables)
        if self.charcard:
            self.charcard.hide()

    # Battle func
    def setupAttackableTileChooser(self, charid, attackables):
        self.inputs.acceptAll()
        self.camhandler.acceptAll()
        self.subphase = 'attack'
        self.matrix.setupAttackableZone(charid, attackables)
        if self.charcard:
            self.charcard.hide()

    # Battle func
    def setupDirectionChooser(self, charid):
        self.inputs.ignoreAll()
        self.camhandler.acceptAll()
        self.at.hide()
        DirectionChooser(charid, self.matrix.sprites[charid], self.camhandler, self.send.WAIT, self.send.UPDATE_PARTY)

    # Attack button clicked
    def onAttackClicked(self, charid):
        self.inputs.ignoreAll()
        self.camhandler.ignoreAll()
        GUI.Help(
            0, 25, 155, 44,
            'shadowed', 'Check',
            'Specify the target with the cursor.\nPress the %c button to select.' % CIRCLE_BTN.upper(),
            lambda: self.send.GET_ATTACKABLES(charid),
            self.send.UPDATE_PARTY,
        )

    # Wait menu item chosen
    def onWaitClicked(self, charid):
        self.inputs.ignoreAll()
        self.camhandler.ignoreAll()
        GUI.Help(
            0, 25, 135, 60,
            'shadowed', 'Check',
            'Specify the direction with\nthe Directional buttons.\nPress the %c button to select.' % CIRCLE_BTN.upper(),
            lambda: self.setupDirectionChooser(charid),
            self.send.UPDATE_PARTY,
        )

    # Cancel menu item chosen
    def onCancelClicked(self, charid):
        self.inputs.acceptAll()
        self.camhandler.acceptAll()
        if self.charcard:
            self.charcard.hide()

### Tasks

    # Updates the displayed direction of a character according to the camera angle
    def characterDirectionTask(self, task):
        h = self.camhandler.container.getH()
        for charid in self.matrix.sprites:
            self.matrix.sprites[charid].updateDisplayDir( h );
        return Task.cont

Client()
run()
