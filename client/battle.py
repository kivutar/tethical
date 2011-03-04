import direct.directbase.DirectStart
from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay
from panda3d.core import AmbientLight, DirectionalLight, LightAttrib
from panda3d.core import TransparencyAttrib
from panda3d.core import TextNode
from panda3d.core import Point3, Vec3, Vec4, BitMask32
from direct.interval.IntervalGlobal import LerpPosInterval, Sequence, Func
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from direct.gui.OnscreenText import OnscreenText
import sys
import Sprite
import CameraHandler
import GUI
import json
from pandac.PandaModules import GeomVertexFormat, GeomVertexData, GeomVertexWriter, Geom, GeomTristrips, GeomLines, GeomNode, VBase4, TransparencyAttrib
import urllib2
from urllib import urlencode

class Battle(DirectObject):

    def __init__(self, cookies):
    
        self.cookies = cookies
    
        try:
            opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1), urllib2.HTTPCookieProcessor(self.cookies))
            urllib2.install_opener(opener)
            rsp = opener.open('http://localhost:3000/battle')
        except IOError:
            print 'fail'
        else:
            self.party = json.loads(rsp.read())
            rsp.close()

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

        # Light the scene
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
        
        # Display the terrain
        terrain = loader.loadModel( 'models/maps/'+self.party['map']['model']+'.egg' )
        terrain.reparentTo( render )
        terrain.setScale( 0.5 )
        
        # Play the background music
        #music = base.loader.loadSfx('music/'+self.party['map']['music']+'.mp3')
        #music.play()
        
        # Place highlightable tiles on the map
        self.tileRoot = render.attachNewNode( "tileRoot" )
        self.tiles = [ [ [ None for z in range(self.party['map']['z']) ] for y in range(self.party['map']['y']) ] for x in range(self.party['map']['x']) ]
        self.chars = []
        
        for x,xs in enumerate(self.party['map']['tiles']):
            for y,ys in enumerate(xs):
                for z,zs in enumerate(ys):
                    if not self.party['map']['tiles'][x][y][z] is None:
                        slope = self.party['map']['tiles'][x][y][z]['slope']
                        
                        self.tiles[x][y][z] = loader.loadModel( "models/slopes/"+slope )
                        self.tiles[x][y][z].reparentTo( self.tileRoot )
                        self.tiles[x][y][z].setPos(self.logic2terrain( (x, y, z+0.05) ))
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
                            char['x'] = x
                            char['y'] = y
                            char['z'] = z
                            sprite = Sprite.Sprite('textures/sprites/misty.png', int(char['direction']))
                            sprite.node.setPos(self.logic2terrain((x,y,z)))
                            sprite.node.reparentTo( render )
                            char['sprite'] = sprite
                            self.tiles[x][y][z].find("**/polygon").node().setTag('char', str(charid))
                            self.chars.append(char)
                            
        self.coords = OnscreenText(text = '', pos = (0.9, 0.9), scale = 0.1)
        
        self.drawBackground()

        # Events
        self.hightlightTileTask = taskMgr.add(self.hightlightTileTask, 'hightlightTileTask')
        self.characterDirectionTask = taskMgr.add(self.characterDirectionTask, 'characterDirectionTask')

        self.accept("mouse1", self.clicked)
        self.accept("b",      self.testmove) # tmp event to test character moves
        self.accept('escape', sys.exit)

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

    # This task highlights the tile on mouse over
    def hightlightTileTask(self, task):

        if self.hix is not False:
            walkable = self.tiles[self.hix][self.hiy][self.hiz].find("**/polygon").node().getTag('walkable')
            if walkable == '1':
                self.tiles[self.hix][self.hiy][self.hiz].setColor(0.0, 0.0, 1.0, 0.75)
            else:
                self.tiles[self.hix][self.hiy][self.hiz].setColor(0, 0, 0, 0)
            self.coords.setText('')
            self.hix = False
            self.hiy = False
            self.hiz = False

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
                self.coords.setText(str(x)+','+str(y)+','+str(z/2.0))
                self.hix = x
                self.hiy = y
                self.hiz = z

        return Task.cont

    # You clicked on a tile
    def clicked(self):
        if self.hix is not False:
            walkable = self.tiles[self.hix][self.hiy][self.hiz].find("**/polygon").node().getTag('walkable')
            if not walkable or walkable != '1':
                for x,xs in enumerate(self.party['map']['tiles']):
                    for y,ys in enumerate(xs):
                        for z,zs in enumerate(ys):
                            if not self.party['map']['tiles'][x][y][z] is None:
                                self.tiles[x][y][z].setColor(0, 0, 0, 0)
                                self.tiles[x][y][z].find("**/polygon").node().setTag('walkable', '0')
        
            charid = self.pq.getEntry(0).getIntoNode().getTag('char')
            if charid != '0':
                if self.party['chars'][charid]['active']:
                    print 'active'
                else:
                    try:
                        opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1), urllib2.HTTPCookieProcessor(self.cookies))
                        urllib2.install_opener(opener)
                        rsp = opener.open('http://localhost:3000/char/'+charid+'/walkables')
                    except IOError, e:
                        print e.code
                        print e.read()
                    else:
                        walkables = json.loads(rsp.read())
                        rsp.close()
                        self.drawWalkables(walkables)

    def drawWalkables(self, walkables):
        for tile in walkables:
            (x, y, z) = tile
            self.tiles[x][y][z].setColor(0.0, 0.0, 1.0, 0.75)
            self.tiles[x][y][z].find("**/polygon").node().setTag('walkable', '1')

    # Updates the displayed direction of a character according to the camera angle
    def characterDirectionTask(self, task):
        h = self.camhandler.container.getH()
        for char in self.chars:
            char['sprite'].updateDisplayDir( h );
        return Task.cont

    def testmove(self):
        path = [ ( 3, 0, 6)
        
               , ( 3, 1, 6)
               , ( 3, 2, 6)
               , ( 3, 3, 6)

               , ( 4, 3, 6)

               , ( 4, 4, 6)
               , ( 4, 5, 6)
               , ( 4, 6, 6)

               , ( 4, 7, 8)
               , ( 4, 8,10)
               , ( 4, 9,12)

               , ( 3, 9,12)
               , ( 2, 9,12)

               , ( 2, 8,12)
               , ( 2, 7,12)
               , ( 2, 6,12)

               , ( 1, 6,12)
               , ( 0, 6,12)

               , ( 0, 5,12)
               , ( 0, 4,12)
               
               , ( 0, 3,10)
               
               , ( 1, 3, 6)

               ]
        self.charmove(self.chars[0], path)
    
    def logic2terrain(self, tile):
        (x, y, z) = tile
        return Point3(x-4, y-5, z/4.0)
    
    # Move a character along a path
    def charmove(self, char, path):
        s1 = Sequence()
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
                s1.append(i1)
            
                i2 = LerpPosInterval(
                    char['sprite'].node, 
                    1, 
                    self.logic2terrain(destination), 
                    startPos=self.logic2terrain(origin)
                )
                s1.append(i2)
            origin = destination
        s1.start()

