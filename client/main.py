from Config import *
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
from direct.gui.DirectGui import *
from direct.task.Task import Task
from direct.distributed.PyDatagramIterator import *
from direct.distributed.PyDatagram import *
from direct.interval.IntervalGlobal import *
from direct.filter.CommonFilters import CommonFilters
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
import SequenceBuilder

class Client(DirectObject):

    def __init__(self):
        self.music = base.loader.loadSfx(GAME+'/music/24.ogg')
        self.music.setLoop(True)
        self.music.play()
        self.background = GUI.Background(self.loginScreen)

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

    # Display the login window
    def loginScreen(self):
        self.loginwindow = GUI.LoginWindow(self.authenticate)

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
        self.phase = None
        self.subphase = None
        
        # Instanciate the camera handler
        self.camhandler = CameraHandler()

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
        self.setPhase('gui')

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
        self.setPhase('gui')
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
            h = self.camhandler.container.getH()
            self.matrix.sprites[charid].updateDisplayDir( h, True )
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

    # You clicked on a tile, this can mean different things, so this is a dispatcher
    def onCircleClicked(self):
        if self.phase == 'tile' and self.cursor.x is not False and self.party['yourturn']:

            if self.charcard:
                self.charcard.hide()
            
            # we clicked an active walkable tile, let's move the character
            if self.party['map']['tiles'][self.cursor.x][self.cursor.y][self.cursor.z].has_key('walkablezone'):
                charid = self.party['map']['tiles'][self.cursor.x][self.cursor.y][self.cursor.z]['walkablezone']
                self.clicked_snd.play()
                dest = (self.cursor.x, self.cursor.y, self.cursor.z)
                self.send.GET_PATH(charid, dest)
                return

            # we clicked on a character
            if self.party['map']['tiles'][self.cursor.x][self.cursor.y][self.cursor.z].has_key('char'):
                charid = self.party['map']['tiles'][self.cursor.x][self.cursor.y][self.cursor.z]['char']
                self.clicked_snd.play()

                # we clicked on a target, let's attack it!
                if self.party['map']['tiles'][self.cursor.x][self.cursor.y][self.cursor.z].has_key('attackablezone'):
                    attackable = self.party['map']['tiles'][self.cursor.x][self.cursor.y][self.cursor.z]['attackablezone']
                    self.setPhase('gui')
                    if self.charbars:
                        self.charbars.hide()
                    self.actionpreview = GUI.ActionPreview(
                        self.party['chars'][attackable],
                        self.party['chars'][charid],
                        16,
                        99,
                        lambda: GUI.AttackCheck(
                            lambda: self.send.ATTACK(attackable, charid),
                            self.send.UPDATE_PARTY
                        ),
                        self.send.UPDATE_PARTY
                    )
                    
            
                # we clicked on the currently active character, let's display the menu
                elif self.party['chars'][charid]['active'] and self.party['yourturn']:
                    
                    self.send.UPDATE_PARTY()
            else:
                self.clicked_snd.play()
                self.send.UPDATE_PARTY()
    
    def onCrossClicked(self):
        if self.phase == 'tile' and self.cursor.x is not False and self.party['yourturn']:

            if self.subphase == 'free':

                # if we clicked on a character
                if self.party['map']['tiles'][self.cursor.x][self.cursor.y][self.cursor.z].has_key('char'):
                    charid = self.party['map']['tiles'][self.cursor.x][self.cursor.y][self.cursor.z]['char']
                    self.send.GET_PASSIVE_WALKABLES(charid)

            elif self.subphase == 'passivewalkables':
                self.matrix.clearZone()
                self.cancel_snd.play()
                self.subphase = 'free'

            elif self.subphase == 'move':
                self.matrix.clearZone()
                self.cancel_snd.play()
                self.subphase = None
                self.send.UPDATE_PARTY()
            elif self.subphase == 'attack':
                self.matrix.clearZone()
                self.cancel_snd.play()
                self.subphase = None
                self.send.UPDATE_PARTY()

    # Keyboard related callback
    def onArrowClicked(self, direction):
        h = self.camhandler.container.getH()
        while h > 180:
            h -= 360
        while h < -180:
            h += 360

        if direction == 'up':
            if h >=    0 and h <  90:
                self.findTileAndUpdateCursorPos((self.cursor.x+1,self.cursor.y))
            if h >=  -90 and h <   0:
                self.findTileAndUpdateCursorPos((self.cursor.x,self.cursor.y-1))
            if h >= -180 and h < -90:
                self.findTileAndUpdateCursorPos((self.cursor.x-1,self.cursor.y))
            if h >=   90 and h < 180:
                self.findTileAndUpdateCursorPos((self.cursor.x,self.cursor.y+1))
        elif direction == 'down':
            if h >=    0 and h <  90:
                self.findTileAndUpdateCursorPos((self.cursor.x-1,self.cursor.y))
            if h >=  -90 and h <   0:
                self.findTileAndUpdateCursorPos((self.cursor.x,self.cursor.y+1))
            if h >= -180 and h < -90:
                self.findTileAndUpdateCursorPos((self.cursor.x+1,self.cursor.y))
            if h >=   90 and h < 180:
                self.findTileAndUpdateCursorPos((self.cursor.x,self.cursor.y-1))
        elif direction == 'left':
            if h >=    0 and h <  90:
                self.findTileAndUpdateCursorPos((self.cursor.x,self.cursor.y+1))
            if h >=  -90 and h <   0:
                self.findTileAndUpdateCursorPos((self.cursor.x+1,self.cursor.y))
            if h >= -180 and h < -90:
                self.findTileAndUpdateCursorPos((self.cursor.x,self.cursor.y-1))
            if h >=   90 and h < 180:
                self.findTileAndUpdateCursorPos((self.cursor.x-1,self.cursor.y))
        elif direction == 'right':
            if h >=    0 and h <  90:
                self.findTileAndUpdateCursorPos((self.cursor.x,self.cursor.y-1))
            if h >=  -90 and h <   0:
                self.findTileAndUpdateCursorPos((self.cursor.x-1,self.cursor.y))
            if h >= -180 and h < -90:
                self.findTileAndUpdateCursorPos((self.cursor.x,self.cursor.y+1))
            if h >=   90 and h < 180:
                self.findTileAndUpdateCursorPos((self.cursor.x+1,self.cursor.y))

    # Returns the closest tile for the given x and y
    # Keyboard related callback
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
    
    def setupWalkableTileChooser(self, charid, walkables):
        self.setPhase('tile')
        self.subphase = 'move'
        self.matrix.setupWalkableZone(charid, walkables)
        if self.charcard:
            self.charcard.hide()

    # Attack button clicked
    def onAttackClicked(self, charid):
        self.setPhase('gui')
        GUI.Help(
            0, 25, 155, 44,
            'shadowed', 'Check',
            'Specify the target with the cursor.\nPress the %c button to select.' % CIRCLE_BTN.upper(),
            lambda: self.send.GET_ATTACKABLES(charid),
            self.send.UPDATE_PARTY,
        )

    # Wait menu item chosen
    def onWaitClicked(self, charid):
        self.setPhase('gui')
        GUI.Help(
            0, 25, 135, 60,
            'shadowed', 'Check',
            'Specify the direction with\nthe Directional buttons.\nPress the %c button to select.' % CIRCLE_BTN.upper(),
            lambda: self.setupDirectionChooser(charid),
            self.send.UPDATE_PARTY,
        )
    
    def setupDirectionChooser(self, charid):
        self.setPhase('direction')
        self.at.hide()
        DirectionChooser(charid, self.matrix.sprites[charid], self.camhandler, self.send.WAIT, self.send.UPDATE_PARTY)

    # Cancel menu item chosen
    def onCancelClicked(self, charid):
        self.setPhase('tile')
        self.subphase = 'free'
        if self.charcard:
            self.charcard.hide()

### Tasks

    # Updates the displayed direction of a character according to the camera angle
    def characterDirectionTask(self, task):
        h = self.camhandler.container.getH()
        for charid in self.matrix.sprites:
            self.matrix.sprites[charid].updateDisplayDir( h );
        return Task.cont

### Utilities

    def setPhase(self, phase):
        self.phase = phase
        self.camhandler.phase = phase
        
        if phase == 'tile':
            self.accept(CIRCLE_BTN, self.onCircleClicked)
            self.accept(CROSS_BTN, self.onCrossClicked)
            self.accept("arrow_up", lambda: self.onArrowClicked('up'))
            self.accept("arrow_down", lambda: self.onArrowClicked('down'))
            self.accept("arrow_left", lambda: self.onArrowClicked('left'))
            self.accept("arrow_right", lambda: self.onArrowClicked('right'))
            self.accept("arrow_up-repeat", lambda: self.onArrowClicked('up'))
            self.accept("arrow_down-repeat", lambda: self.onArrowClicked('down'))
            self.accept("arrow_left-repeat", lambda: self.onArrowClicked('left'))
            self.accept("arrow_right-repeat", lambda: self.onArrowClicked('right'))
        else:
            self.subphase = False
            self.ignoreAll()

Client()
run()
