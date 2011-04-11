import direct.directbase.DirectStart
from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay
from panda3d.core import AmbientLight, DirectionalLight, LightAttrib
from panda3d.core import TransparencyAttrib
from panda3d.core import TextNode
from panda3d.core import Point3, Vec3, Vec4, BitMask32
from direct.interval.IntervalGlobal import LerpPosInterval, LerpColorInterval, LerpHprInterval, Sequence, Func, Wait, Parallel
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from direct.gui.OnscreenText import OnscreenText
import sys, time
import Sprite
import CameraHandler
import GUI
from pandac.PandaModules import GeomVertexFormat, GeomVertexData, GeomVertexWriter, Geom, GeomTristrips, GeomLines, GeomNode, VBase4, TransparencyAttrib
import Network
import Direction

class Battle(DirectObject):

    def __init__(self, con, party, transitionframe):
    
        self.con = con
        self.party = party
        self.phase = None
        self.queue = []

        self.camhandler = CameraHandler.CameraHandler()

        # Collision stuff
        self.picker = CollisionTraverser()
        self.pq     = CollisionHandlerQueue()
        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = camera.attachNewNode(self.pickerNode)
        self.pickerNode.setFromCollideMask(BitMask32.bit(1))
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)
        self.picker.addCollider(self.pickerNP, self.pq)
        self.hix = False
        self.hiy = False
        self.hiz = False
        self.ox = False
        self.oy = False
        self.oz = False
        
        self.lightScene()
        
        # Display the terrain
        terrain = loader.loadModel( 'models/maps/'+self.party['map']['model']+'.egg' )
        terrain.reparentTo( render )
        terrain.setScale( 1.5 )
        
        # Play the background music
        music = base.loader.loadSfx('music/'+self.party['map']['music']+'.ogg')
        music.setLoop(True)
        music.play()
        
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
                        
                        self.tiles[x][y][z] = loader.loadModel( "models/slopes/"+slope )
                        self.tiles[x][y][z].reparentTo( self.tileRoot )
                        self.tiles[x][y][z].setPos(self.logic2terrain( (x, y, z+0.05) ))
                        self.tiles[x][y][z].setScale(3.0)
                        self.tiles[x][y][z].setTransparency(TransparencyAttrib.MAlpha)
                        self.tiles[x][y][z].setColor( 0, 0, 0, 0 )
                        
                        # Collision stuff
                        self.tiles[x][y][z].find("**/polygon").node().setIntoCollideMask( BitMask32.bit(1) )
                        self.tiles[x][y][z].find("**/polygon").node().setTag('x', str(x))
                        self.tiles[x][y][z].find("**/polygon").node().setTag('y', str(y))
                        self.tiles[x][y][z].find("**/polygon").node().setTag('z', str(z))
                        self.tiles[x][y][z].find("**/polygon").node().setTag('char', '0')            

                        if self.party['map']['tiles'][x][y][z].has_key('char'):
                            charid = self.party['map']['tiles'][x][y][z]['char']
                            char = self.party['chars'][charid]
                            sprite = Sprite.Sprite('textures/sprites/'+char['sprite']+'.png', int(char['direction']))
                            sprite.node.setPos(self.logic2terrain((x,y,z)))
                            sprite.node.reparentTo( render )
                            self.sprites[charid] = sprite
                            self.tiles[x][y][z].find("**/polygon").node().setTag('char', str(charid))
                            
                            
        self.coords = OnscreenText(text = '', pos = (0.9, 0.8), scale = 0.2, fg = (0.82,1,055,1), shadow = (0,0,0.08,1) )
        
        self.atcontainer = render.attachNewNode("atcontainer")
        self.atcontainer.setPos(0,0,3.5)
        self.atcontainer.setBillboardPointEye()
        at = loader.loadModel('models/gui/AT.egg')
        at.setTransparency(True)
        at.reparentTo(self.atcontainer)
        at.setPos(.75,0,0)
        at.setScale(1.75)
        self.hideAT()
        
        self.charcard = None
        self.charcard2 = None

        self.drawBackground()

        # Tasks
        self.hightlightTileTask     = taskMgr.add(self.hightlightTileTask    , 'hightlightTileTask'    )
        self.characterDirectionTask = taskMgr.add(self.characterDirectionTask, 'characterDirectionTask')
        self.otherPlayersTask       = taskMgr.add(self.otherPlayersTask      , 'otherPlayersTask'      )
        self.dequeue                = taskMgr.add(self.dequeue               , 'dequeue'      )

        # Inputs
        self.accept("mouse1", self.onTileClicked)
        self.accept('escape', sys.exit)

        seq = Sequence()
        i1 = LerpColorInterval(transitionframe, 5, (0,0,0,0), startColor=(0,0,0,1))
        (cx, cy, cz) = self.camhandler.container.getPos()
        i2 = LerpPosInterval(self.camhandler.container, 5, (cx,cy,cz+5), startPos=(cx,cy,cz+50))
        (ch, cp, cr) = self.camhandler.container.getHpr()
        i3 = LerpHprInterval(self.camhandler.container, 5, (ch+90, cp, cr), (ch-180, cp, cr))
        p1 = Parallel(i1,i2,i3)
        seq.append(p1)
        seq.append(Func(transitionframe.destroy))
        seq.append(Func(self.turn))
        seq.start()

    # The main dispatcher
    def turn(self):
        self.updateParty()

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

                                if self.charcard:
                                    self.charcard.hide()
                                self.charcard = GUI.CharCard(char)

                                if self.charcard2:
                                    self.charcard2.hide()
                                self.charcard2 = GUI.CharCard2(char)

                                if self.party['yourturn']:
                                    if char['canmove'] or char['canact']:
                                        self.showMenu(charid)
                                    else:
                                        self.onWaitClicked(charid)

    def updateParty(self):
        party = self.con.Send('battle')
        if party:
            self.party = party

    def showMenu(self, charid):
        self.phase = 'gui'
        self.camhandler.phase = 'gui'
        menu = GUI.Menu( self.party['chars'][charid],
            lambda: self.onMoveClicked(charid),
            lambda: self.onAttackClicked(charid),
            lambda: self.onWaitClicked(charid),
            lambda: self.onCancelClicked(charid) )

    # Get the path from the server, and makes the character walk on it
    def path(self, charid, dest):
        (x, y, z) = dest
        path = self.con.Send('char/'+charid+'/path/'+str(x)+'/'+str(y)+'/'+str(z))
        if path:
            seq = Sequence()
            seq.append( Func(self.hideAT) )
            seq.append( Func(self.updateSpriteAnimation, charid, 'walk') )
            seq.append( self.getCharacterMoveSequence(charid, path) )
            seq.append( Func(self.clearWalkables) )
            seq.append( Func(self.updateSpriteAnimation, charid) )
            seq.append( Func(self.moveCharacterTo, charid, dest) )
            seq.start()
            # TODO: ask confirmation

    # Send the moveto packet and update the map tags with new char coords
    def moveCharacterTo(self, charid, dest):
        (x1, y1, z1) = self.getCharacterCoords(charid)
        (x2, y2, z2) = dest
        res = self.con.Send('char/'+charid+'/moveto/'+str(x2)+'/'+str(y2)+'/'+str(z2))
        if res:
            self.tiles[x1][y1][z1].find("**/polygon").node().setTag('char', '0')
            self.tiles[x2][y2][z2].find("**/polygon").node().setTag('char', str(charid))
            self.turn()

    # Send the attack packet, get the returned damages and display the attack animation
    def attack(self, charid, targetid):
        damages = self.con.Send('char/'+charid+'/attack/'+targetid)
        if damages:
            print damages
            seq = Sequence()
            seq.append( self.getCharacterAttackSequence(charid, targetid) )
            seq.append( Func(self.turn) )
            seq.start()

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
        seq.append( Func(self.clearAttackables) )
        return seq

    # Update the status (animation) of a sprite after something happened
    def updateSpriteAnimation(self, charid, animation=False):
        if animation:
            self.sprites[charid].animation = animation
        else:
            stats = self.con.Send('char/'+charid)
            if stats:
                if stats['hp'] >= (stats['hpmax']/2):
                    self.sprites[charid].animation = 'walk'
                if stats['hp'] < (stats['hpmax']/2):
                    self.sprites[charid].animation = 'weak'
                if stats['hp'] == 0:
                    self.sprites[charid].animation = 'dead'
                    self.die_snd.play()
        h = self.camhandler.container.getH()
        self.sprites[charid].updateDisplayDir( h, True );

    # Draw blue tile zone
    def drawWalkables(self, walkables):
        for tile in walkables:
            (x, y, z) = tile
            self.tiles[x][y][z].setColor(0.0, 0.0, 1.0, 0.75)

    # Tag a zone as walkable or active-walkable
    def tagWalkables(self, charid, walkables, active=False):
        for tile in walkables:
            (x, y, z) = tile
            self.tiles[x][y][z].find("**/polygon").node().setTag('walkable', '1')
            if active:
                self.tiles[x][y][z].find("**/polygon").node().setTag('active', charid)

    # Draw and tag the red tile zone
    def drawAndTagAttackables(self, charid, attackables):
        for tile in attackables:
            (x, y, z) = tile
            self.tiles[x][y][z].setColor(1.0, 0.0, 0.0, 0.75)
            self.tiles[x][y][z].find("**/polygon").node().setTag('attackable', charid)

    # Clear walkable tile zone
    def clearWalkables(self):
        for x,xs in enumerate(self.party['map']['tiles']):
            for y,ys in enumerate(xs):
                for z,zs in enumerate(ys):
                    if not self.party['map']['tiles'][x][y][z] is None:
                        walkable = self.tiles[x][y][z].find("**/polygon").node().getTag('walkable')
                        if walkable and walkable != '0':
                            self.tiles[x][y][z].setColor(0, 0, 0, 0)
                            self.tiles[x][y][z].find("**/polygon").node().setTag('walkable', '0')
                            self.tiles[x][y][z].find("**/polygon").node().setTag('active',   '0')

    # Clear attackable tile zone
    def clearAttackables(self):
        for x,xs in enumerate(self.party['map']['tiles']):
            for y,ys in enumerate(xs):
                for z,zs in enumerate(ys):
                    if not self.party['map']['tiles'][x][y][z] is None:
                        attackable = self.tiles[x][y][z].find("**/polygon").node().getTag('attackable')
                        if attackable and attackable != '0':
                            self.tiles[x][y][z].setColor(0, 0, 0, 0)
                            self.tiles[x][y][z].find("**/polygon").node().setTag('attackable', '0')

    # Returns a sequence showing the character moving through a path
    def getCharacterMoveSequence(self, charid, path):
        sprite = self.sprites[charid]
        seq = Sequence()
        origin = False
        for destination in path:
            if origin:
            
                (x1, y1, z1) = origin
                (x2, y2, z2) = destination
                if x2 > x1:
                    i1 = Func(sprite.setRealDir, 1)
                elif x2 < x1:
                    i1 = Func(sprite.setRealDir, 3)
                elif y2 > y1:
                    i1 = Func(sprite.setRealDir, 2)
                elif y2 < y1:
                    i1 = Func(sprite.setRealDir, 4)
                seq.append(i1)
            
                i2 = LerpPosInterval(
                    sprite.node, 
                    0.5, 
                    self.logic2terrain(destination), 
                    startPos=self.logic2terrain(origin)
                )
                seq.append(i2)
            origin = destination
        return seq

### Events

    # You clicked on a tile, this can mean different things, so this is a dispatcher
    def onTileClicked(self):
        if self.phase == 'tile' and self.hix is not False and self.party['yourturn']:

            if self.charcard2:
                self.charcard2.hide()

            charid = self.pq.getEntry(0).getIntoNode().getTag('char')
        
            # focus the camera on the selected tile
            self.camhandler.move(self.logic2terrain((self.hix, self.hiy, self.hiz)))

            # we clicked an active walkable tile, let's move the character
            active = self.tiles[self.hix][self.hiy][self.hiz].find("**/polygon").node().getTag('active')
            if active and active != '0':
                self.clicked_snd.play()
                dest = (self.hix, self.hiy, self.hiz)
                self.path(active, dest)
                return

            # cancel walkable
            walkable = self.tiles[self.hix][self.hiy][self.hiz].find("**/polygon").node().getTag('walkable')
            if not walkable or walkable != '1':
                self.clearWalkables()
                if charid == '0':
                    self.cancel_snd.play()

            # cancel attackable
            attackable = self.tiles[self.hix][self.hiy][self.hiz].find("**/polygon").node().getTag('attackable')
            if not attackable or attackable == '0':
                self.clearAttackables()
                if charid == '0':
                    self.cancel_snd.play()

            # we clicked on a character
            if charid != '0':
                self.clicked_snd.play()

                # we clicked on a target, let's attack it!
                if attackable and attackable != '0':
                    self.attack(attackable, charid)
            
                # we clicked on the currently active character, let's display the menu
                elif self.party['chars'][charid]['active'] and self.party['yourturn']:
                    self.turn()
                
                # we clicked on a random character, let's draw its walkable zone
                else:
                    self.charcard2 = GUI.CharCard2(None)
                    walkables = self.con.Send('char/'+charid+'/walkables')
                    if walkables:
                        self.drawWalkables(walkables)
                        self.tagWalkables(charid, walkables, False)

    # Move button clicked
    def onMoveClicked(self, charid):
        walkables = self.con.Send('char/'+charid+'/walkables')
        if walkables:
            GUI.Help(
                'move_help',
                lambda: self.setupTileChooser(charid, walkables)
            )
    
    def setupTileChooser(self, charid, walkables):
        self.phase = 'tile'
        self.camhandler.phase = 'tile'
        self.drawWalkables(walkables)
        self.tagWalkables(charid, walkables, True)

    # Attack button clicked
    def onAttackClicked(self, charid):
        attackables = self.con.Send('char/'+charid+'/attackables')
        if attackables:
            self.phase = 'tile'
            self.camhandler.phase = 'tile'
            self.drawAndTagAttackables(charid, attackables)

    # Wait button clicked
    def onWaitClicked(self, charid):
        GUI.Help(
            'direction_help',
            lambda: self.setupDirectionChooser(charid)
        )
    
    def setupDirectionChooser(self, charid):
        self.phase = 'direction'
        self.camhandler.phase = 'direction'
        self.hideAT()
        Direction.Chooser(charid, self.sprites[charid], self.directionChosen, self.turn)

    # Cancel button clicked
    def onCancelClicked(self, charid):
        self.phase = 'tile'
        self.camhandler.phase = 'tile'

    def directionChosen(self, charid, direction):
        res = self.con.Send('char/'+charid+'/wait/'+direction)
        if res:
            self.turn()

### Tasks

    # Updates the displayed direction of a character according to the camera angle
    def characterDirectionTask(self, task):
        h = self.camhandler.container.getH()
        for charid in self.sprites:
            self.sprites[charid].updateDisplayDir( h );
        return Task.cont

    def dequeue(self, task):
        if len(self.queue) and self.phase != 'animation':
            self.updateParty()
            self.setPhase('animation')
            log = self.queue.pop(0)
            if log['act'] == 'move':
                charid    = log['charid']
                walkables = log['walkables']
                path      = log['path']
                (x1, y1, z1) = path[0]
                (x2, y2, z2) = path[-1]
                self.tiles[x1][y1][z1].find("**/polygon").node().setTag('char', '0')
                self.tiles[x2][y2][z2].find("**/polygon").node().setTag('char', str(charid))
                seq = Sequence()
                seq.append( Func(self.drawWalkables, walkables) )
                seq.append( Wait(0.5) )
                seq.append( Func(self.tagWalkables, charid, walkables, False) )
                seq.append( Func(self.hideAT) )
                seq.append( Func(self.updateSpriteAnimation, charid, 'walk') )
                seq.append( self.getCharacterMoveSequence(charid, path) )
                seq.append( Wait(0.5) )
                seq.append( Func(self.updateSpriteAnimation, charid) )
                seq.append( Func(self.clearWalkables) )
                seq.append( Func(self.showAT, self.sprites[charid]) )
                seq.append( Func(self.setPhase, 'listen') )
                seq.start()
            if log['act'] == 'attack':
                charid      = log['charid']
                targetid    = log['targetid']
                damages     = log['targetid']
                attackables = log['attackables']
                seq = Sequence()
                seq.append( Func(self.drawAndTagAttackables, charid, attackables) )
                seq.append( self.getCharacterAttackSequence(charid, targetid) )
                seq.append( Func(self.setPhase, 'listen') )
                seq.start()
            if log['act'] == 'wait':
                seq = Sequence()
                seq.append( Func(self.hideAT) )
                seq.append( Wait(0.5) )
                seq.append( Func(self.sprites[log['charid']].setRealDir, log['direction']) )
                seq.append( Wait(0.5) )
                seq.append( Func(self.setPhase, 'listen') )
                seq.append( Func(self.turn) )
                seq.start()

        return Task.cont

    # This task is responsible of rendering the other player's actions
    def otherPlayersTask(self, task):
        if not self.party['yourturn']:
            log = self.con.Send('otherplayers')
            if log:
                self.queue.append(log)

        return Task.cont

    # This task highlights the tile on mouse over
    def hightlightTileTask(self, task):

        if self.phase == 'tile':

            # unhighlight previous tile
            if self.hix is not False:
                walkable   = self.tiles[self.hix][self.hiy][self.hiz].find("**/polygon").node().getTag('walkable')
                attackable = self.tiles[self.hix][self.hiy][self.hiz].find("**/polygon").node().getTag('attackable')
                if walkable == '1':
                    self.tiles[self.hix][self.hiy][self.hiz].setColor(0.0, 0.0, 1.0, 0.75)
                elif attackable and attackable != '0':
                    self.tiles[self.hix][self.hiy][self.hiz].setColor(1.0, 0.0, 0.0, 0.75)
                else:
                    self.tiles[self.hix][self.hiy][self.hiz].setColor(0, 0, 0, 0)
                self.coords.setText('')
                self.hix = False
                self.hiy = False
                self.hiz = False

            # highlight new tile
            if base.mouseWatcherNode.hasMouse():
                mpos = base.mouseWatcherNode.getMouse()

                self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())
                self.picker.traverse(self.tileRoot)

                if self.pq.getNumEntries() > 0:

                    self.pq.sortEntries()
                    x = int(self.pq.getEntry(0).getIntoNode().getTag('x'))
                    y = int(self.pq.getEntry(0).getIntoNode().getTag('y'))
                    z = int(self.pq.getEntry(0).getIntoNode().getTag('z'))
                    charid = self.pq.getEntry(0).getIntoNode().getTag('char')
                    self.tiles[x][y][z].setColor(0.0,1.0,0.0,0.75)
                    self.coords.setText(str(z/2.0)+'h')
                    self.hix = x
                    self.hiy = y
                    self.hiz = z

                    if self.ox != x or self.oy != y or self.oz != z:
                        self.hover_snd.play()
                        self.ox = x
                        self.oy = y
                        self.oz = z
                        
                        if self.charcard:
                            self.charcard.hide()
                        
                        if charid and charid != '0':
                            char = self.party['chars'][charid]
                            self.charcard = GUI.CharCard(char)

        return Task.cont

### Utilities

    def logic2terrain(self, tile):
        (x, y, z) = tile
        return Point3((x-4)*3.0, (y-5)*3.0, (z/4.0)*3.0)

    # Used for debug purpose
    def charStats(self, charid):
        stats = self.con.Send('char/'+charid)
        if stats:
            print stats

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
        node = GeomNode('gnode')
        node.addGeom(geom)
        base.camera.attachNewNode(node)

    # Light the scene
    def lightScene(self):
        for i, light in enumerate(self.party['map']['lights']):
            if light.has_key('direction'):
                directionalLight = DirectionalLight( "directionalLight_"+str(i) )
                directionalLight.setDirection( Vec3( *light['direction'] ) )
                directionalLight.setColor( Vec4( *light['color'] ) )
                render.setLight( render.attachNewNode( directionalLight ) )
            else:
                ambientLight = AmbientLight( "ambientLight"+str(i) )
                ambientLight.setColor( Vec4( *light['color'] ) )
                render.setLight( render.attachNewNode( ambientLight ) )

    def showAT(self, sprite):
        self.atcontainer.reparentTo(sprite.node)

    def hideAT(self):
        self.atcontainer.detachNode()

