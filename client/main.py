from pandac.PandaModules import loadPrcFileData
loadPrcFileData("", "window-title Tethical")
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.task.Task import Task
from direct.distributed.PyDatagramIterator import *
from direct.distributed.PyDatagram import *
from direct.interval.IntervalGlobal import *
from direct.filter.CommonFilters import CommonFilters
import math
from operator import itemgetter
import json
import GUI
import CameraHandler
import Direction
import Sprite

IP = '127.0.0.1' #'88.190.20.195' #'95.130.11.221'
PORT =  3001

LOGIN_MESSAGE = 1
LOGIN_SUCCESS = 2
LOGIN_FAIL = 3
CREATE_PARTY = 4
PARTY_CREATED = 5
GET_MAPS = 6
MAP_LIST = 7
GET_PARTIES = 8
PARTY_LIST = 9
JOIN_PARTY = 10
PARTY_JOINED = 11
START_BATTLE = 12
UPDATE_PARTY = 13
PARTY_UPDATED = 14
GET_WALKABLES = 15
WALKABLES_LIST = 16
GET_PATH = 17
PATH = 18
MOVE_TO = 19
MOVED = 20
MOVED_PASSIVE = 21
WAIT = 22
WAIT_SUCCESS = 23
WAIT_PASSIVE = 24
GET_ATTACKABLES = 25
ATTACKABLES_LIST = 26
ATTACK = 27
ATTACK_SUCCESS = 28
ATTACK_PASSIVE = 29
UPDATE_PARTY_LIST = 30
PARTY_JOIN_FAIL = 31
BATTLE_COMPLETE = 32
GAME_OVER = 33
GET_PASSIVE_WALKABLES = 34
PASSIVE_WALKABLES_LIST = 35

class Client(DirectObject):

    def __init__(self):

        self.music = base.loader.loadSfx('music/24.ogg')
        self.music.setLoop(True)
        self.music.play()
        self.background = GUI.Background(self.loginScreen)

    def processData(self, datagram):
        iterator = PyDatagramIterator(datagram)
        msgID = iterator.getUint8()
        if msgID == LOGIN_SUCCESS:
            self.loginwindow.commandanddestroy(self.partyListScreen)
        elif msgID == LOGIN_FAIL:
            print iterator.getString()
        elif msgID == PARTY_CREATED:
            party = json.loads(iterator.getString32())
            self.party = party
        elif msgID == MAP_LIST:
            maps = json.loads(iterator.getString())
            self.mapchooserwindow = GUI.MapChooser(maps, self.background.frame, self.createParty, self.partyListScreen)
        elif msgID == PARTY_LIST:
            parties = json.loads(iterator.getString32())
            self.partylistwindow = GUI.PartyListWindow(self.joinParty, self.mapChooserScreen)
            self.partylistwindow.refresh(parties)
            print 'Received the party list:'
            for k in parties.keys():
                print ' - ',k
        elif msgID == UPDATE_PARTY_LIST:
            parties = json.loads(iterator.getString32())
            self.partylistwindow.refresh(parties)
        elif msgID == PARTY_JOINED:
            party = json.loads(iterator.getString32())
            self.party = party
        elif msgID == PARTY_JOIN_FAIL:
            print iterator.getString()
            parties = json.loads(iterator.getString32())
            self.partylistwindow = GUI.PartyListWindow(self.joinParty, self.mapChooserScreen)
            self.partylistwindow.refresh(parties)
            print 'Received the party list:'
            for k in parties.keys():
                print ' - ',k
        elif msgID == START_BATTLE:
            self.party = json.loads(iterator.getString32())
            self.transitionframe = DirectFrame( frameSize = ( -2, 2, -2, 2 ) )
            self.transitionframe.setTransparency(True)
            seq = Sequence()
            seq.append(LerpColorInterval(self.transitionframe, 2, (0,0,0,1), startColor=(0,0,0,0)))
            seq.append(Func(self.background.frame.destroy))
            seq.append(Func(self.music.stop))
            seq.append(Func(self.battle_init))
            seq.start()
        elif msgID == PARTY_UPDATED:
            self.party['yourturn'] = iterator.getBool()
            self.party['chars'] = json.loads(iterator.getString32())
            self.party_updated()
        elif msgID == WALKABLES_LIST:
            charid = iterator.getString()
            walkables = json.loads(iterator.getString())
            if walkables:
                self.setPhase('gui')
                GUI.Help(
                    'move_help',
                    lambda: self.setupWalkableTileChooser(charid, walkables),
                    self.turn
                )
            else:
                #TODO: show message "no walkable tile"
                print "no walkable tile"
                self.turn()
        elif msgID == PASSIVE_WALKABLES_LIST:
            charid = iterator.getString()
            walkables = json.loads(iterator.getString())
            if walkables:
                self.clicked_snd.play()
                self.setupPassiveWalkableZone(walkables)
                self.subphase = 'passivewalkables'
            else:
                #TODO: show message "no walkable tile"
                print "no walkable tile"
                self.turn()
        elif msgID == PATH:
            charid = iterator.getString()
            orig = json.loads(iterator.getString())
            origdir = iterator.getUint8()
            dest = json.loads(iterator.getString())
            path = json.loads(iterator.getString())
            
            seq = Sequence()
            seq.append( Func(self.hideAT) )
            seq.append( Func(self.updateSpriteAnimation, charid, 'run') )
            seq.append( Func(self.clearZone) )
            seq.append( self.getCharacterMoveSequence(charid, path) )
            seq.append( Func(self.updateSpriteAnimation, charid) )
            seq.append( Func(self.moveCheck, charid, orig, origdir, dest) )
            seq.start()
        elif msgID == MOVED:
            charid = iterator.getString()
            x2 = iterator.getUint8()
            y2 = iterator.getUint8()
            z2 = iterator.getUint8()

            (x1, y1, z1) = self.getCharacterCoords(charid)
            del self.party['map']['tiles'][x1][y1][z1]['char']
            self.party['map']['tiles'][x2][y2][z2]['char'] = charid
            self.turn()
        elif msgID == MOVED_PASSIVE:
            charid = iterator.getString()
            walkables = json.loads(iterator.getString())
            path = json.loads(iterator.getString())

            self.setPhase('animation')
            (x1, y1, z1) = path[0]
            (x2, y2, z2) = path[-1]
            del self.party['map']['tiles'][x1][y1][z1]['char']
            self.party['map']['tiles'][x2][y2][z2]['char'] = charid
            seq = Sequence()
            seq.append( Func(self.setupPassiveWalkableZone, walkables) )
            seq.append( Wait(0.5) )
            seq.append( Func(self.updateCursorPos, (x2, y2, z2)) )
            seq.append( Wait(0.5) )
            seq.append( Func(self.hideAT) )
            seq.append( Func(self.updateSpriteAnimation, charid, 'run') )
            seq.append( Func(self.camhandler.move, self.logic2terrain((x2, y2, z2))) )
            seq.append( self.getCharacterMoveSequence(charid, path) )
            seq.append( Wait(0.5) )
            seq.append( Func(self.updateSpriteAnimation, charid) )
            seq.append( Func(self.clearZone) )
            seq.append( Func(self.showAT, self.sprites[charid]) )
            seq.append( Func(self.setPhase, 'listen') )
            seq.start()
        elif msgID == WAIT_SUCCESS:
            self.turn()
        elif msgID == WAIT_PASSIVE:
            charid = iterator.getString()
            direction = iterator.getUint8()
            
            self.setPhase('animation')
            seq = Sequence()
            seq.append( Func(self.hideAT) )
            seq.append( Wait(0.5) )
            seq.append( Func(self.sprites[charid].setRealDir, direction) )
            seq.append( Wait(0.5) )
            seq.append( Func(self.setPhase, 'listen') )
            seq.append( Func(self.turn) )
            seq.start()
        elif msgID == ATTACKABLES_LIST:
            charid = iterator.getString()
            attackables = json.loads(iterator.getString())

            self.setPhase('tile')
            self.subphase = 'attack'
            self.setupAttackableZone(charid, attackables)
            if self.charcard2:
                self.charcard2.hide()
        elif msgID == ATTACK_SUCCESS:
            charid = iterator.getString()
            targetid = iterator.getString()
            damages = iterator.getUint8()

            print damages
            target = self.party['chars'][targetid]
            target['hp'] = target['hp'] - damages
            if target['hp'] < 0:
                target['hp'] = 0

            seq = Sequence()
            seq.append( self.getCharacterAttackSequence(charid, targetid) )
            seq.append( Func(self.turn) )
            seq.start()
        elif msgID == ATTACK_PASSIVE:
            charid = iterator.getString()
            targetid = iterator.getString()
            damages = iterator.getUint8()
            attackables = json.loads(iterator.getString())

            print damages
            target = self.party['chars'][targetid]
            target['hp'] = target['hp'] - damages
            if target['hp'] < 0:
                target['hp'] = 0

            self.setPhase('animation')
            seq = Sequence()
            seq.append( Func(self.setupAttackableZone, charid, attackables) )
            seq.append( Wait(0.5) )
            seq.append( Func(self.updateCursorPos, self.getCharacterCoords(targetid)) )
            seq.append( Func(self.camhandler.move, self.logic2terrain(self.getCharacterCoords(targetid))) )
            seq.append( Wait(0.5) )
            seq.append( self.getCharacterAttackSequence(charid, targetid) )
            seq.append( Func(self.camhandler.move, self.logic2terrain(self.getCharacterCoords(charid))) )
            seq.append( Func(self.setPhase, 'listen') )
            seq.start()
        elif msgID == GAME_OVER:
            if self.charcard:
                self.charcard.hide()
            if self.charcard2:
                self.charcard2.hide()
            for i,charid in enumerate(self.sprites):
                if self.sprites[charid].animation == 'walk':
                    self.updateSpriteAnimation(charid, 'stand')
            self.music.stop()
            self.music = base.loader.loadSfx('music/33.ogg')
            self.music.play()
            GUI.GameOver(self.end)
        elif msgID == BATTLE_COMPLETE:
            if self.charcard:
                self.charcard.hide()
            if self.charcard2:
                self.charcard2.hide()
            for i,charid in enumerate(self.sprites):
                if self.sprites[charid].animation == 'walk':
                    self.updateSpriteAnimation(charid, 'stand')
            self.music.stop()
            self.music = base.loader.loadSfx('music/13.ogg')
            self.music.play()
            GUI.BrownOverlay(GUI.Congratulations, self.end)

    # This task process data sent by the server, if any
    def tskReaderPolling(self, taskdata):
        if self.cReader.dataAvailable():
            datagram=NetDatagram()
            if self.cReader.getData(datagram):
                self.processData(datagram)
        return Task.cont

    def loginScreen(self):
        self.loginwindow = GUI.LoginWindow(self.authenticate)

    # Setup connection and send the LOGIN datagram with credentials
    def authenticate(self):
        login = self.loginwindow.loginEntry.get()
        password = self.loginwindow.passwordEntry.get()

        self.cManager  = QueuedConnectionManager()
        self.cListener = QueuedConnectionListener(self.cManager, 0)
        self.cReader   = QueuedConnectionReader(self.cManager, 0)
        self.cWriter   = ConnectionWriter(self.cManager, 0)
        self.cReader.setTcpHeaderSize(4)
        self.cWriter.setTcpHeaderSize(4)

        self.myConnection = self.cManager.openTCPClientConnection(IP, PORT, 5000)
        if self.myConnection:
            self.cReader.addConnection(self.myConnection)
            print 'Client listening on', IP, ':', PORT
            taskMgr.add(self.tskReaderPolling, "Poll the connection reader")

            myPyDatagram = PyDatagram()
            myPyDatagram.addUint8(LOGIN_MESSAGE)
            myPyDatagram.addString(login)
            myPyDatagram.addString(password)
            self.cWriter.send(myPyDatagram, self.myConnection)

        else:
            print 'Can\'t connect to server on', IP, ':', PORT

    def partyListScreen(self):

        myPyDatagram = PyDatagram()
        myPyDatagram.addUint8(GET_PARTIES)
        self.cWriter.send(myPyDatagram, self.myConnection)

    def mapChooserScreen(self):

        myPyDatagram = PyDatagram()
        myPyDatagram.addUint8(GET_MAPS)
        self.cWriter.send(myPyDatagram, self.myConnection)

    # Send the party details to the server in order to instanciate a party
    def createParty(self, mapname):
        import time
        partyname = str(int(time.time()))
        
        myPyDatagram = PyDatagram()
        myPyDatagram.addUint8(CREATE_PARTY)
        myPyDatagram.addString(partyname)
        myPyDatagram.addString(mapname)
        self.cWriter.send(myPyDatagram, self.myConnection)

    # Join a party
    def joinParty(self, name):
        
        myPyDatagram = PyDatagram()
        myPyDatagram.addUint8(JOIN_PARTY)
        myPyDatagram.addString(name)
        self.cWriter.send(myPyDatagram, self.myConnection)
    
    # The battle begins
    def battle_init(self):
        self.phase = None
        self.subphase = None
        
        self.camhandler = CameraHandler.CameraHandler()
        
        self.lightScene()
        
        # Display the terrain
        terrain = loader.loadModel( 'models/maps/'+self.party['map']['model'] )
        terrain.reparentTo( render )
        terrain.setScale( *self.party['map']['scale'] )
        
        # Play the background music
        self.music = base.loader.loadSfx('music/'+self.party['map']['music']+'.ogg')
        self.music.setLoop(True)
        self.music.play()
        
        # Load sounds
        self.hover_snd   = base.loader.loadSfx("sounds/hover.ogg")
        self.clicked_snd = base.loader.loadSfx("sounds/clicked.ogg")
        self.cancel_snd  = base.loader.loadSfx("sounds/cancel.ogg")
        self.attack_snd  = base.loader.loadSfx("sounds/attack.ogg")
        self.die_snd    = base.loader.loadSfx("sounds/die.ogg")
        
        # Place highlightable tiles on the map
        self.tileRoot = render.attachNewNode( "tileRoot" )
        self.tiles = [ [ [ None for z in range(self.party['map']['z']) ] for y in range(self.party['map']['y']) ] for x in range(self.party['map']['x']) ]
        self.sprites = {}

        for x,xs in enumerate(self.party['map']['tiles']):
            for y,ys in enumerate(xs):
                for z,zs in enumerate(ys):
                    if not self.party['map']['tiles'][x][y][z] is None:
                        slope = self.party['map']['tiles'][x][y][z]['slope']
                        scale = self.party['map']['tiles'][x][y][z]['scale']
                        depth = self.party['map']['tiles'][x][y][z]['depth']

                        self.tiles[x][y][z] = loader.loadModel( "models/slopes/"+slope )
                        self.tiles[x][y][z].reparentTo( self.tileRoot )
                        self.tiles[x][y][z].setPos(self.logic2terrain( (x, y, z+depth+0.05) ))
                        self.tiles[x][y][z].setScale(3.0, 3.0, 6.0/7.0*3.0*scale)
                        self.tiles[x][y][z].setTransparency(TransparencyAttrib.MAlpha)
                        self.tiles[x][y][z].setColor( 0, 0, 0, 0 )

                        if self.party['map']['tiles'][x][y][z].has_key('char'):
                            charid = self.party['map']['tiles'][x][y][z]['char']
                            char = self.party['chars'][charid]
                            sprite = Sprite.Sprite('textures/sprites/'+char['sprite']+'.png', int(char['direction']))
                            sprite.animation = 'stand'
                            sprite.node.setPos(self.logic2terrain((x,y,z)))
                            sprite.node.reparentTo( render )
                            self.sprites[charid] = sprite
        
        self.atcontainer = render.attachNewNode("atcontainer")
        self.atcontainer.setPos(0,0,3.5)
        self.atcontainer.setBillboardPointEye()
        at = loader.loadModel('models/gui/AT')
        at.setTransparency(True)
        at.reparentTo(self.atcontainer)
        at.setPos(.75,0,0)
        at.setScale(1.75)
        self.hideAT()
        
        self.charcard = None
        self.charcard2 = None

        self.drawBackground()
        
        # Tasks
        taskMgr.add(self.characterDirectionTask , 'characterDirectionTask')

        # Cursor stuff
        self.curtex = loader.loadTexture('textures/cursor.png')
        self.curtex.setMagfilter(Texture.FTNearest)
        self.curtex.setMinfilter(Texture.FTNearest)
        self.cux = False
        self.cuy = False
        self.cuz = False
        self.cursor = loader.loadModel( "models/slopes/flat" )
        self.cursor.reparentTo( self.tileRoot )
        self.cursor.setScale(3.0)
        self.cursor.setTransparency(TransparencyAttrib.MAlpha)
        self.cursor.setColor( 1, 1, 1, 1 )
        self.cursor.setTexture(self.curtex)
        
        self.wtex = loader.loadTexture('textures/walkable.png')
        self.wtex.setMagfilter(Texture.FTNearest)
        self.wtex.setMinfilter(Texture.FTNearest)
        
        self.atex = loader.loadTexture('textures/attackable.png')
        self.atex.setMagfilter(Texture.FTNearest)
        self.atex.setMinfilter(Texture.FTNearest)
        
        #filters = CommonFilters(base.win, base.cam)
        #filters.setBloom(blend=(0,0,0,1), desat=-0.5, intensity=3.0, size="medium")
        #filters.setAmbientOcclusion()
        #filters.setCartoonInk()

        # Battle intro animation
        seq = Sequence()
        i1 = LerpColorInterval(self.transitionframe, 5, (0,0,0,0), startColor=(0,0,0,1))
        cx, cy, cz = terrain.getBounds().getCenter()
        i2 = LerpPosInterval(self.camhandler.container, 5, (cx,cy,cz), startPos=(cx,cy,cz+50))
        ch, cp, cr = self.camhandler.container.getHpr()
        i3 = LerpHprInterval(self.camhandler.container, 5, (ch+90, cp, cr), (ch-180, cp, cr))
        p1 = Parallel(i1,i2,i3)
        seq.append(p1)
        seq.append(Func(self.transitionframe.destroy))
        seq.append(Wait(1))
        seq.append(Func(self.updateAllSpritesAnimations, 'walk'))
        seq.append(Func(lambda: GUI.BrownOverlay(GUI.ConditionsForWinning, self.turn)))
        seq.start()

    def updateAllSpritesAnimations(self, animation):
        for i,charid in enumerate(self.sprites):
            Sequence(
                Wait(float(i)/6.0),
                Func(self.updateSpriteAnimation, charid, animation),
            ).start()

    # The main dispatcher
    def turn(self):
        myPyDatagram = PyDatagram()
        myPyDatagram.addUint8(UPDATE_PARTY)
        self.cWriter.send(myPyDatagram, self.myConnection)

    def party_updated(self):

        self.clearZone()

        for x,xs in enumerate(self.party['map']['tiles']):
            for y,ys in enumerate(xs):
                for z,zs in enumerate(ys):
                    if not self.party['map']['tiles'][x][y][z] is None:
                        if self.party['map']['tiles'][x][y][z].has_key('char') and self.party['map']['tiles'][x][y][z]['char'] != 0:
                            charid = self.party['map']['tiles'][x][y][z]['char']
                            char = self.party['chars'][charid]

                            if char['active']:
                                self.camhandler.move(self.logic2terrain((x, y, z)))
                                self.showAT(self.sprites[charid])

                                self.updateCursorPos((x,y,z))

                                if self.charcard2:
                                    self.charcard2.hide()
                                self.charcard2 = GUI.CharCard2(char)

                                if self.party['yourturn']:
                                    if char['canmove'] or char['canact']:
                                        self.showMenu(charid)
                                    else:
                                        self.onWaitClicked(charid)

    def end(self):
        taskMgr.remove('characterDirectionTask')
        for child in render.getChildren():
            child.removeNode()
        self.camhandler.destroy()
        self.coords.destroy()
        NodePath(self.sky).removeNode()
        self.background = GUI.Background(self.partyListScreen)

    def showMenu(self, charid):
        self.setPhase('gui')
        menu = GUI.Menu( self.party['chars'][charid],
            lambda: self.onMoveClicked(charid),
            lambda: self.onAttackClicked(charid),
            lambda: self.onWaitClicked(charid),
            lambda: self.onCancelClicked(charid) )

    # Get the path from the server, and makes the character walk on it
    def path(self, charid, dest):
        orig = self.getCharacterCoords(charid)
        origdir = self.sprites[charid].realdir
        (x, y, z) = dest
        
        myPyDatagram = PyDatagram()
        myPyDatagram.addUint8(GET_PATH)
        myPyDatagram.addString(charid)
        myPyDatagram.addUint8(x)
        myPyDatagram.addUint8(y)
        myPyDatagram.addUint8(z)
        self.cWriter.send(myPyDatagram, self.myConnection)

    def moveCheck(self, charid, orig, origdir, dest):
        self.setPhase('gui')
        GUI.MoveCheck(
            lambda: self.moveCharacterTo(charid, dest),
            lambda: self.cancelMove(charid, orig, origdir)
        )

    def cancelMove(self, charid, orig, origdir):
        self.sprites[charid].node.setPos(self.logic2terrain(orig))
        self.sprites[charid].setRealDir(origdir)
        self.turn()

    # Send the moveto packet and update the map tags with new char coords
    def moveCharacterTo(self, charid, dest):

        (x2, y2, z2) = dest
        
        myPyDatagram = PyDatagram()
        myPyDatagram.addUint8(MOVE_TO)
        myPyDatagram.addString(charid)
        myPyDatagram.addUint8(x2)
        myPyDatagram.addUint8(y2)
        myPyDatagram.addUint8(z2)
        self.cWriter.send(myPyDatagram, self.myConnection)

    # Send the attack packet, get the returned damages and display the attack animation
    def attack(self, charid, targetid):
        
        myPyDatagram = PyDatagram()
        myPyDatagram.addUint8(ATTACK)
        myPyDatagram.addString(charid)
        myPyDatagram.addString(targetid)
        self.cWriter.send(myPyDatagram, self.myConnection)


    # Makes a character look at another one
    def characterLookAt(self, charid, targetid):
        (x1, y1, z1) = self.getCharacterCoords(charid)
        (x2, y2, z2) = self.getCharacterCoords(targetid)
        if x1 > x2:
            self.sprites[charid].setRealDir(3)
        if x1 < x2:
            self.sprites[charid].setRealDir(1)
        if y1 > y2:
            self.sprites[charid].setRealDir(4)
        if y1 < y2:
            self.sprites[charid].setRealDir(2)

    # Returns the sequence of a character punching another
    def getCharacterAttackSequence(self, charid, targetid):
        seq = Sequence()
        seq.append( Func(self.hideAT) )
        seq.append( Func(self.characterLookAt,       charid, targetid) )
        seq.append( Func(self.updateSpriteAnimation, charid, 'attack') )
        seq.append( Wait(0.5) )
        seq.append( Func(self.updateSpriteAnimation, targetid, 'hit') )
        seq.append( Func(self.attack_snd.play) )
        seq.append( Wait(0.5) )
        seq.append( Func(self.updateSpriteAnimation, charid) )
        seq.append( Wait(0.5) )
        seq.append( Func(self.updateSpriteAnimation, targetid) )
        seq.append( Wait(0.5) )
        seq.append( Func(self.clearZone) )
        return seq

    # Update the status (animation) of a sprite after something happened
    def updateSpriteAnimation(self, charid, animation=False):
        if animation:
            self.sprites[charid].animation = animation
            h = self.camhandler.container.getH()
            self.sprites[charid].updateDisplayDir( h, True )
        else:
            stats = self.party['chars'][charid]
            if stats['hp'] >= (stats['hpmax']/2):
                self.sprites[charid].animation = 'walk'
            if stats['hp'] < (stats['hpmax']/2):
                self.sprites[charid].animation = 'weak'
            if stats['hp'] <= 0:
                self.sprites[charid].animation = 'dead'
                self.die_snd.play()
            h = self.camhandler.container.getH()
            self.sprites[charid].updateDisplayDir( h, True )

    # Draw blue tile zone
    def setupPassiveWalkableZone(self, walkables):
        for x,y,z in walkables:
            self.tiles[x][y][z].setColor(1, 1, 1, 1)
            self.tiles[x][y][z].setTexture(self.wtex)

    # Tag a zone as walkable or active-walkable
    def setupWalkableZone(self, charid, walkables):
        for x,y,z in walkables:
            self.tiles[x][y][z].setColor(1, 1, 1, 1)
            self.tiles[x][y][z].setTexture(self.wtex)
            self.party['map']['tiles'][x][y][z]['walkablezone'] = charid

    # Draw and tag the red tile zone
    def setupAttackableZone(self, charid, attackables):
        for x,y,z in attackables:
            self.tiles[x][y][z].setColor(1, 1, 1, 1)
            self.tiles[x][y][z].setTexture(self.atex)
            self.party['map']['tiles'][x][y][z]['attackablezone'] = charid

    # Clear any tile zone
    def clearZone(self):
        for x,xs in enumerate(self.party['map']['tiles']):
            for y,ys in enumerate(xs):
                for z,zs in enumerate(ys):
                    if not self.party['map']['tiles'][x][y][z] is None:
                        self.tiles[x][y][z].setColor(0, 0, 0, 0)
                        if self.party['map']['tiles'][x][y][z].has_key('walkablezone'):
                            del self.party['map']['tiles'][x][y][z]['walkablezone']
                        if self.party['map']['tiles'][x][y][z].has_key('attackablezone'):
                            del self.party['map']['tiles'][x][y][z]['attackablezone']

    # Returns a sequence showing the character moving through a path
    def getCharacterMoveSequence(self, charid, path):
        sprite = self.sprites[charid]
        seq = Sequence()
        origin = False
        for destination in path:
            if origin:

                (x1, y1, z1) = origin
                (x2, y2, z2) = destination

                # first, face the right direction
                if x2 > x1:
                    d = 1
                elif x2 < x1:
                    d = 3
                elif y2 > y1:
                    d = 2
                elif y2 < y1:
                    d = 4
                seq.append( Func(sprite.setRealDir, d) )

                # then, add the move animation from one tile to the next
                if z2 - z1 >= 4:
                    middle = (
                        origin[0] + (destination[0] - origin[0]) / 2.0,
                        origin[1] + (destination[1] - origin[1]) / 2.0,
                        destination[2] + 0.5
                    )
                    seq.append(
                        Sequence(
                            Func(self.updateSpriteAnimation, charid, 'smalljump'),
                            LerpPosInterval(
                                sprite.node, 
                                0.125,
                                self.logic2terrain(middle), 
                                startPos=self.logic2terrain(origin)
                            ),
                            LerpPosInterval(
                                sprite.node, 
                                0.125,
                                self.logic2terrain(destination), 
                                startPos=self.logic2terrain(middle)
                            ),
                            Func(self.updateSpriteAnimation, charid, 'run'),
                        )
                    )
                elif z1 - z2 >= 4:
                    middle = (
                        origin[0] + (destination[0] - origin[0]) / 2.0,
                        origin[1] + (destination[1] - origin[1]) / 2.0,
                        origin[2] + 0.5
                    )
                    seq.append(
                        Sequence(
                            Func(self.updateSpriteAnimation, charid, 'smalljump'),
                            LerpPosInterval(
                                sprite.node, 
                                0.125,
                                self.logic2terrain(middle), 
                                startPos=self.logic2terrain(origin)
                            ),
                            LerpPosInterval(
                                sprite.node, 
                                0.125,
                                self.logic2terrain(destination), 
                                startPos=self.logic2terrain(middle)
                            ),
                            Func(self.updateSpriteAnimation, charid, 'run'),
                        )
                    )
                else:
                    seq.append(
                        LerpPosInterval(
                            sprite.node, 
                            0.25,
                            self.logic2terrain(destination), 
                            startPos=self.logic2terrain(origin)
                        )
                    )
            origin = destination
        return seq

### Events

    def updateCursorPos(self, pos):

        self.camhandler.move(self.logic2terrain(pos))

        (x, y, z) = pos
        tile = self.party['map']['tiles'][x][y][z]

        self.camhandler.move(self.logic2terrain(pos))

        self.cursor.detachNode()
        self.cursor = loader.loadModel( "models/slopes/"+tile['slope'] )
        self.cursor.reparentTo( self.tileRoot )
        self.cursor.setScale(3.0, 3.0, 6.0/7.0*3.0*tile['scale'])
        self.cursor.setTransparency(TransparencyAttrib.MAlpha)
        self.cursor.setTexture(self.curtex)
        self.cursor.setPos(self.logic2terrain((x, y, z+tile['depth']+0.1)))

        if tile['walkable']:
            self.cursor.setColor( 1, 1, 1, .75 )
        else:
            self.cursor.setColor( 1, 0, 0, .75 )

        self.cux = x
        self.cuy = y
        self.cuz = z

        if self.charcard:
            self.charcard.hide()

        if self.party['map']['tiles'][x][y][z].has_key('char'):
            charid = self.party['map']['tiles'][x][y][z]['char']
            char = self.party['chars'][charid]
            self.charcard = GUI.CharCard(char)

        try:
            self.coords.update(tile)
        except:
            self.coords = GUI.Coords(tile)

    # You clicked on a tile, this can mean different things, so this is a dispatcher
    def onCircleClicked(self):
        if self.phase == 'tile' and self.cux is not False and self.party['yourturn']:

            if self.charcard2:
                self.charcard2.hide()
            
            # we clicked an active walkable tile, let's move the character
            if self.party['map']['tiles'][self.cux][self.cuy][self.cuz].has_key('walkablezone'):
                charid = self.party['map']['tiles'][self.cux][self.cuy][self.cuz]['walkablezone']
                self.clicked_snd.play()
                dest = (self.cux, self.cuy, self.cuz)
                self.path(charid, dest)
                return

            # we clicked on a character
            if self.party['map']['tiles'][self.cux][self.cuy][self.cuz].has_key('char'):
                charid = self.party['map']['tiles'][self.cux][self.cuy][self.cuz]['char']
                self.clicked_snd.play()

                # we clicked on a target, let's attack it!
                if self.party['map']['tiles'][self.cux][self.cuy][self.cuz].has_key('attackablezone'):
                    attackable = self.party['map']['tiles'][self.cux][self.cuy][self.cuz]['attackablezone']
                    self.setPhase('gui')
                    GUI.AttackCheck(
                        lambda: self.attack(attackable, charid),
                        self.turn
                    )
            
                # we clicked on the currently active character, let's display the menu
                elif self.party['chars'][charid]['active'] and self.party['yourturn']:
                    
                    self.turn()
            else:
                self.clicked_snd.play()
                self.turn()
    
    def onCrossClicked(self):
        if self.phase == 'tile' and self.cux is not False and self.party['yourturn']:

            if self.subphase == 'free':

                # if we clicked on a character
                if self.party['map']['tiles'][self.cux][self.cuy][self.cuz].has_key('char'):
                    charid = self.party['map']['tiles'][self.cux][self.cuy][self.cuz]['char']
                    myPyDatagram = PyDatagram()
                    myPyDatagram.addUint8(GET_PASSIVE_WALKABLES)
                    myPyDatagram.addString(charid)
                    self.cWriter.send(myPyDatagram, self.myConnection)

            elif self.subphase == 'passivewalkables':
                self.clearZone()
                self.cancel_snd.play()
                self.subphase = 'free'

            elif self.subphase == 'move':
                self.clearZone()
                self.cancel_snd.play()
                self.subphase = None
                self.turn()
            elif self.subphase == 'attack':
                self.clearZone()
                self.cancel_snd.play()
                self.subphase = None
                self.turn()
    
    def onArrowClicked(self, direction):
        h = self.camhandler.container.getH()
        while h > 180:
            h -= 360
        while h < -180:
            h += 360

        if direction == 'up':
            if h >=    0 and h <  90:
                self.findTileAndUpdateCursorPos((self.cux+1,self.cuy))
            if h >=  -90 and h <   0:
                self.findTileAndUpdateCursorPos((self.cux,self.cuy-1))
            if h >= -180 and h < -90:
                self.findTileAndUpdateCursorPos((self.cux-1,self.cuy))
            if h >=   90 and h < 180:
                self.findTileAndUpdateCursorPos((self.cux,self.cuy+1))
        elif direction == 'down':
            if h >=    0 and h <  90:
                self.findTileAndUpdateCursorPos((self.cux-1,self.cuy))
            if h >=  -90 and h <   0:
                self.findTileAndUpdateCursorPos((self.cux,self.cuy+1))
            if h >= -180 and h < -90:
                self.findTileAndUpdateCursorPos((self.cux+1,self.cuy))
            if h >=   90 and h < 180:
                self.findTileAndUpdateCursorPos((self.cux,self.cuy-1))
        elif direction == 'left':
            if h >=    0 and h <  90:
                self.findTileAndUpdateCursorPos((self.cux,self.cuy+1))
            if h >=  -90 and h <   0:
                self.findTileAndUpdateCursorPos((self.cux+1,self.cuy))
            if h >= -180 and h < -90:
                self.findTileAndUpdateCursorPos((self.cux,self.cuy-1))
            if h >=   90 and h < 180:
                self.findTileAndUpdateCursorPos((self.cux-1,self.cuy))
        elif direction == 'right':
            if h >=    0 and h <  90:
                self.findTileAndUpdateCursorPos((self.cux,self.cuy-1))
            if h >=  -90 and h <   0:
                self.findTileAndUpdateCursorPos((self.cux-1,self.cuy))
            if h >= -180 and h < -90:
                self.findTileAndUpdateCursorPos((self.cux,self.cuy+1))
            if h >=   90 and h < 180:
                self.findTileAndUpdateCursorPos((self.cux+1,self.cuy))

    # Returns the closest tile for the given x and y
    def findTileAndUpdateCursorPos(self, pos):
        fux, fuy = pos

        # list the possibles tiles, on official maps, this list should not excess 2 items
        possibles = []
        for x,xs in enumerate(self.party['map']['tiles']):
            for y,ys in enumerate(xs):
                for z,zs in enumerate(ys):
                    if not self.party['map']['tiles'][x][y][z] is None:
                        if fux == x and fuy == y:
                            d = math.fabs(z-self.cuz) # for each possible, compute the Z delta with the current tile
                            possibles.append((x, y, z, d))

        if len(possibles):
            # sort the possibles on Z delta, and get the closer tile
            selected = sorted(possibles, key=itemgetter(3))[0][0:3]

            self.hover_snd.play()
            self.updateCursorPos(selected)

    # Move button clicked
    def onMoveClicked(self, charid):
        myPyDatagram = PyDatagram()
        myPyDatagram.addUint8(GET_WALKABLES)
        myPyDatagram.addString(charid)
        self.cWriter.send(myPyDatagram, self.myConnection)
    
    def setupWalkableTileChooser(self, charid, walkables):
        self.setPhase('tile')
        self.subphase = 'move'
        self.setupWalkableZone(charid, walkables)
        if self.charcard2:
            self.charcard2.hide()

    # Attack button clicked
    def onAttackClicked(self, charid):
        myPyDatagram = PyDatagram()
        myPyDatagram.addUint8(GET_ATTACKABLES)
        myPyDatagram.addString(charid)
        self.cWriter.send(myPyDatagram, self.myConnection)

    # Wait button clicked
    def onWaitClicked(self, charid):
        self.setPhase('gui')
        GUI.Help(
            'direction_help',
            lambda: self.setupDirectionChooser(charid),
            self.turn
        )
    
    def setupDirectionChooser(self, charid):
        self.setPhase('direction')
        self.hideAT()
        Direction.Chooser(charid, self.sprites[charid], self.camhandler, self.directionChosen, self.turn)

    # Cancel button clicked
    def onCancelClicked(self, charid):
        self.setPhase('tile')
        self.subphase = 'free'
        if self.charcard2:
            self.charcard2.hide()

    def directionChosen(self, charid, direction):
        myPyDatagram = PyDatagram()
        myPyDatagram.addUint8(WAIT)
        myPyDatagram.addString(charid)
        myPyDatagram.addUint8(direction)
        self.cWriter.send(myPyDatagram, self.myConnection)

### Tasks

    # Updates the displayed direction of a character according to the camera angle
    def characterDirectionTask(self, task):
        h = self.camhandler.container.getH()
        for charid in self.sprites:
            self.sprites[charid].updateDisplayDir( h );
        return Task.cont

### Utilities

    # Converts logic coordinates to panda3d coordinates
    def logic2terrain(self, tile):
        (x, y, z) = tile
        return Point3(
            (x+self.party['map']['offset'][0]+0.5) * 3.0,
            (y+self.party['map']['offset'][1]+0.5) * 3.0,
            (z+self.party['map']['offset'][2]+0.0) * 3.0/4.0*6.0/7.0,
        )

    # Returns the logic coordinates of a character
    def getCharacterCoords(self, charid):
        for x,xs in enumerate(self.party['map']['tiles']):
            for y,ys in enumerate(xs):
                for z,zs in enumerate(ys):
                    if not self.party['map']['tiles'][x][y][z] is None:
                        if self.party['map']['tiles'][x][y][z].has_key('char') and self.party['map']['tiles'][x][y][z]['char'] != 0:
                            if charid == self.party['map']['tiles'][x][y][z]['char']:
                                return (x, y, z)

    def setPhase(self, phase):
        self.phase = phase
        self.camhandler.phase = phase
        
        if phase == 'tile':
            self.accept("b", self.onCircleClicked)
            self.accept("space", self.onCrossClicked)
            self.accept("arrow_up", lambda: self.onArrowClicked('up'))
            self.accept("arrow_down", lambda: self.onArrowClicked('down'))
            self.accept("arrow_left", lambda: self.onArrowClicked('left'))
            self.accept("arrow_right", lambda: self.onArrowClicked('right'))
            self.accept("arrow_up-repeat", lambda: self.onArrowClicked('up'))
            self.accept("arrow_down-repeat", lambda: self.onArrowClicked('down'))
            self.accept("arrow_left-repeat", lambda: self.onArrowClicked('left'))
            self.accept("arrow_right-repeat", lambda: self.onArrowClicked('right'))
        else:
            self.ignoreAll()

# Graphic

    # Draw the gradient background
    def drawBackground(self):
        vdata = GeomVertexData('name_me', GeomVertexFormat.getV3c4(), Geom.UHStatic)
        vertex = GeomVertexWriter(vdata, 'vertex')
        color = GeomVertexWriter(vdata, 'color')
        primitive = GeomTristrips(Geom.UHStatic)
        film_size = base.cam.node().getLens().getFilmSize()
        x = film_size.getX() / 2.0
        z = x * 0.75
        vertex.addData3f( x, 90,  z)
        vertex.addData3f(-x, 90,  z)
        vertex.addData3f( x, 90, -z)
        vertex.addData3f(-x, 90, -z)
        color.addData4f(VBase4(*self.party['map']['backgroundcolor1']))
        color.addData4f(VBase4(*self.party['map']['backgroundcolor1']))
        color.addData4f(VBase4(*self.party['map']['backgroundcolor2']))
        color.addData4f(VBase4(*self.party['map']['backgroundcolor2']))
        primitive.addNextVertices(4)
        primitive.closePrimitive()
        geom = Geom(vdata)
        geom.addPrimitive(primitive)
        self.sky = GeomNode('sky')
        self.sky.addGeom(geom)
        base.camera.attachNewNode(self.sky)

    # Light the scene
    def lightScene(self):

        for i, light in enumerate(self.party['map']['lights']):
            if light.has_key('direction'):
                directionalLight = DirectionalLight( "directionalLight_"+str(i) )
                directionalLight.setDirection( Vec3( *light['direction'] ) )
                directionalLight.setColor( Vec4( *light['color'] ) )
                render.setLight( render.attachNewNode( directionalLight ) )
            elif light.has_key('position'):
                plight = PointLight('plighti_'+str(i))
                plight.setColor( Vec4( *light['color'] ) )
                plight.setAttenuation(Point3( *light['attenuation'] ))
                plnp = render.attachNewNode(plight)
                plnp.setPos( self.logic2terrain( light['position'] ) )
                render.setLight( plnp )
            else:
                ambientLight = AmbientLight( "ambientLight"+str(i) )
                ambientLight.setColor( Vec4( *light['color'] ) )
                render.setLight( render.attachNewNode( ambientLight ) )

        render.setShaderAuto()

    def showAT(self, sprite):
        self.atcontainer.reparentTo(sprite.node)

    def hideAT(self):
        self.atcontainer.detachNode()

Client()
run()
