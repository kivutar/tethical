import direct.directbase.DirectStart
from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay
from panda3d.core import AmbientLight, DirectionalLight, LightAttrib
from panda3d.core import TransparencyAttrib
from panda3d.core import TextNode
from panda3d.core import Point3, Vec3, Vec4, BitMask32
from direct.interval.IntervalGlobal import LerpPosInterval, Sequence, Func, Wait
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from direct.gui.OnscreenText import OnscreenText
import sys, time
import Sprite
import CameraHandler
import GUI
from pandac.PandaModules import GeomVertexFormat, GeomVertexData, GeomVertexWriter, Geom, GeomTristrips, GeomLines, GeomNode, VBase4, TransparencyAttrib
import Network

class Battle(DirectObject):

    def __init__(self, con, party):
    
        self.con = con
        self.party = party

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
        self.chars = {}
        
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
                            sprite = Sprite.Sprite('textures/sprites/misty.png', int(char['direction']))
                            sprite.node.setPos(self.logic2terrain((x,y,z)))
                            sprite.node.reparentTo( render )
                            char['sprite'] = sprite
                            self.tiles[x][y][z].find("**/polygon").node().setTag('char', str(charid))
                            self.chars[charid] = char
                            
        self.coords = OnscreenText(text = '', pos = (0.9, 0.8), scale = 0.2, fg = (0.82,1,055,1), shadow = (0,0,0.08,1) )
        
        self.drawBackground()

        # Tasks
        self.hightlightTileTask     = taskMgr.add(self.hightlightTileTask    , 'hightlightTileTask'    )
        self.characterDirectionTask = taskMgr.add(self.characterDirectionTask, 'characterDirectionTask')
        self.otherPlayersTask       = taskMgr.add(self.otherPlayersTask      , 'otherPlayersTask'      )

        # Inputs
        self.accept("mouse1", self.onTileClicked)
        self.accept('escape', sys.exit)
        self.accept('t'     , self.turn)

        self.turn()

    # The main dispatcher
    def turn(self):
        party = self.con.Send('battle')
        if party:
            self.party = party
            
            for x,xs in enumerate(self.party['map']['tiles']):
                for y,ys in enumerate(xs):
                    for z,zs in enumerate(ys):
                        if not self.party['map']['tiles'][x][y][z] is None:
                            if self.party['map']['tiles'][x][y][z].has_key('char') and self.party['map']['tiles'][x][y][z]['char'] != 0:
                                charid = self.party['map']['tiles'][x][y][z]['char']
                                char = self.party['chars'][charid]
                                
                                if char['active']:
                                    self.camhandler.move(self.logic2terrain((x, y, z)))
                                    #if self.party['yourturn']:
                                    #    menu = GUI.Menu( lambda: self.onMoveClicked(charid), 
                                    #                     lambda: self.onAttackClicked(charid),
                                    #                     lambda: self.onWaitClicked(charid) )

    # Get the path from the server, and makes the character walk on it
    def path(self, charid, dest):
        (x, y, z) = dest
        path = self.con.Send('char/'+charid+'/path/'+str(x)+'/'+str(y)+'/'+str(z))
        if path:
            seq = Sequence()
            seq.append( Func(self.updateSpriteAnimation, charid, 'walk') )
            seq.append( self.getCharacterMoveSequence(charid, path) )
            seq.append( Func(self.clearWalkables) )
            seq.append( Func(self.updateSpriteAnimation, charid) )
            seq.start()
            # ask confirmation
            self.moveCharacterTo(charid, dest)

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
            self.playAttackAnimation(charid, targetid)
            self.turn()

    # Makes a character look at another one
    def characterLookAt(self, charid, targetid):
        (x1, y1, z1) = self.getCharacterCoords(charid)
        (x2, y2, z2) = self.getCharacterCoords(targetid)
        if x1 > x2:
            self.chars[charid]['sprite'].setRealDir(3)
        if x1 < x2:
            self.chars[charid]['sprite'].setRealDir(1)
        if y1 > y2:
            self.chars[charid]['sprite'].setRealDir(4)
        if y1 < y2:
            self.chars[charid]['sprite'].setRealDir(2)

    # Plays the attack animation
    def playAttackAnimation(self, charid, targetid):
        seq = Sequence()
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
        seq.start()

    # Update the status (animation) of a sprite after something happened
    def updateSpriteAnimation(self, charid, animation=False):
        if animation:
            self.chars[charid]['sprite'].animation = animation
        else:
            stats = self.con.Send('char/'+charid)
            if stats:
                if stats['hp'] >= (stats['hpmax']/2):
                    self.chars[charid]['sprite'].animation = 'walk'
                if stats['hp'] < (stats['hpmax']/2):
                    self.chars[charid]['sprite'].animation = 'weak'
                if stats['hp'] == 0:
                    self.chars[charid]['sprite'].animation = 'dead'
                    self.die_snd.play()
        h = self.camhandler.container.getH()
        self.chars[charid]['sprite'].updateDisplayDir( h, True );

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
        char = self.chars[charid]
        seq = Sequence()
        origin = False
        for destination in path:
            if origin:
            
                (x1, y1, z1) = origin
                (x2, y2, z2) = destination
                if x2 > x1:
                    i1 = Func(char['sprite'].setRealDir, 1)
                elif x2 < x1:
                    i1 = Func(char['sprite'].setRealDir, 3)
                elif y2 > y1:
                    i1 = Func(char['sprite'].setRealDir, 2)
                elif y2 < y1:
                    i1 = Func(char['sprite'].setRealDir, 4)
                seq.append(i1)
            
                i2 = LerpPosInterval(
                    char['sprite'].node, 
                    1, 
                    self.logic2terrain(destination), 
                    startPos=self.logic2terrain(origin)
                )
                seq.append(i2)
            origin = destination
        return seq

### Events

    # You clicked on a tile, this can mean different things, so this is a dispatcher
    def onTileClicked(self):
        if self.hix is not False and self.party['yourturn']:
        
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
                    menu = GUI.Menu( lambda: self.onMoveClicked(charid), 
                                     lambda: self.onAttackClicked(charid),
                                     lambda: self.onWaitClicked(charid) )
                
                # we clicked on a random character, let's draw its walkable zone
                else:
                    walkables = self.con.Send('char/'+charid+'/walkables')
                    if walkables:
                        self.drawWalkables(walkables)
                        self.tagWalkables(charid, walkables, False)

    # Move button clicked
    def onMoveClicked(self, charid):
        walkables = self.con.Send('char/'+charid+'/walkables')
        if walkables:
            self.drawWalkables(walkables)
            self.tagWalkables(charid, walkables, True)

    # Attack button clicked
    def onAttackClicked(self, charid):
        attackables = self.con.Send('char/'+charid+'/attackables')
        if attackables:
            self.drawAndTagAttackables(charid, attackables)

    # Wait button clicked
    def onWaitClicked(self, charid):
        res = self.con.Send('char/'+charid+'/wait/1')
        if res:
            self.chars[charid]['sprite'].setRealDir(1)
            self.turn()

### Tasks

    # Updates the displayed direction of a character according to the camera angle
    def characterDirectionTask(self, task):
        h = self.camhandler.container.getH()
        for charid in self.chars:
            self.chars[charid]['sprite'].updateDisplayDir( h );
        return Task.cont

    # This task is responsible of rendering the other player's actions
    def otherPlayersTask(self, task):
        if not self.party['yourturn']:
            log = self.con.Send('otherplayers')
            if log:
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
                    seq.append( Func(self.updateSpriteAnimation, charid, 'walk') )
                    seq.append( self.getCharacterMoveSequence(charid, path) )
                    seq.append( Wait(0.5) )
                    seq.append( Func(self.updateSpriteAnimation, charid) )
                    seq.append( Func(self.clearWalkables) )                    
                    seq.start()
                if log['act'] == 'attack':
                    charid      = log['charid']
                    targetid    = log['targetid']
                    damages     = log['targetid']
                    attackables = log['attackables']
                    self.drawAndTagAttackables(charid, attackables)
                    self.playAttackAnimation(charid, targetid)
                if log['act'] == 'wait':
                    self.chars[log['charid']]['sprite'].setRealDir(log['direction'])
                    self.turn()
        return Task.cont

    # This task highlights the tile on mouse over
    def hightlightTileTask(self, task):

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

