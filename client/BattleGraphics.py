from Config import *
from panda3d.core import *
from panda3d.physics import BaseParticleEmitter,BaseParticleRenderer
from panda3d.physics import PointParticleFactory,SpriteParticleRenderer
from panda3d.physics import LinearNoiseForce,DiscEmitter
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from direct.particles.ForceGroup import ForceGroup
import Sprite

class BattleGraphics(object):

    def __init__(self, mp):
        self.mp = mp

    # Converts logic coordinates to panda3d coordinates
    def logic2terrain(self, tile):
        (x, y, z) = tile
        return Point3(
            (x+self.mp['offset'][0]+0.5) * 3.7,
            (y+self.mp['offset'][1]+0.5) * 3.7,
            (z+self.mp['offset'][2]+0.0) * 3.7/4.0*6.0/7.0,
        )

    # Load the terrain model, scale it and attach it to render
    def displayTerrain(self):
        self.terrain = loader.loadModel(GAME+'/models/maps/'+self.mp['model'])
        self.terrain.reparentTo( render )
        self.terrain.setScale( *self.mp['scale'] )

    # Loop over the lights defined in a map, and light the scene
    def lightScene(self):
        for i, light in enumerate(self.mp['lights']):
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

    # Add special effects to the scene
    def addEffects(self):
        if self.mp.has_key('effects'):
            base.enableParticles()
            for effect in self.mp['effects']:
                p = ParticleEffect()
                p.loadConfig(GAME+'/particles/'+effect['file']+'.ptf') 
                p.start(render)
                p.setPos(self.logic2terrain( effect['position'] ))

    # Returns the logic coordinates of a character
    def getCharacterCoords(self, charid):
        for x,xs in enumerate(self.mp['tiles']):
            for y,ys in enumerate(xs):
                for z,zs in enumerate(ys):
                    if not self.mp['tiles'][x][y][z] is None:
                        if self.mp['tiles'][x][y][z].has_key('char') and self.mp['tiles'][x][y][z]['char'] != 0:
                            if charid == self.mp['tiles'][x][y][z]['char']:
                                return (x, y, z)

class AT(object):

    def __init__(self):
        self.atcontainer = render.attachNewNode("atcontainer")
        self.atcontainer.setPos(0,0,3.5)
        self.atcontainer.setBillboardPointEye()
        at = loader.loadModel(GAME+'/models/gui/AT')
        at.setTransparency(True)
        at.reparentTo(self.atcontainer)
        at.setPos(.75,0,0)
        at.setScale(2.0*256.0/240.0)

    def showOnSprite(self, sprite):
        self.atcontainer.reparentTo(sprite.node)

    def hide(self):
        self.atcontainer.detachNode()

# Draw the gradient background representing the sky during a battle
class Sky(object):

    def __init__(self, mp):
        vdata = GeomVertexData('name_me', GeomVertexFormat.getV3c4(), Geom.UHStatic)
        vertex = GeomVertexWriter(vdata, 'vertex')
        color = GeomVertexWriter(vdata, 'color')
        primitive = GeomTristrips(Geom.UHStatic)
        film_size = base.cam.node().getLens().getFilmSize()
        x = film_size.getX() / 2.0
        z = x * 256.0/240.0
        vertex.addData3f( x, 90,  z)
        vertex.addData3f(-x, 90,  z)
        vertex.addData3f( x, 90, -z)
        vertex.addData3f(-x, 90, -z)
        color.addData4f(VBase4(*mp['backgroundcolor1']))
        color.addData4f(VBase4(*mp['backgroundcolor1']))
        color.addData4f(VBase4(*mp['backgroundcolor2']))
        color.addData4f(VBase4(*mp['backgroundcolor2']))
        primitive.addNextVertices(4)
        primitive.closePrimitive()
        geom = Geom(vdata)
        geom.addPrimitive(primitive)
        sky = GeomNode('sky')
        sky.addGeom(geom)
        base.camera.attachNewNode(sky)

class Cursor(object):

    def __init__(self, battleGraphics, matrixContainer):
        self.battleGraphics = battleGraphics
        self.matrixContainer = matrixContainer

        self.curtex = loader.loadTexture(GAME+'/textures/cursor.png')
        self.curtex.setMagfilter(Texture.FTNearest)
        self.curtex.setMinfilter(Texture.FTNearest)

        self.x = False
        self.y = False
        self.z = False

        self.cursor = loader.loadModel(GAME+'/models/slopes/flat')
        self.cursor.reparentTo( self.matrixContainer )
        self.cursor.setScale(3.7)
        self.cursor.setTransparency(TransparencyAttrib.MAlpha)
        self.cursor.setColor( 1, 1, 1, 1 )
        self.cursor.setTexture(self.curtex)

        pointertex = loader.loadTexture(GAME+'/textures/pointer.png')
        pointertex.setMagfilter(Texture.FTNearest)
        pointertex.setMinfilter(Texture.FTNearest)
        cm = CardMaker('card')
        cm.setFrame(-2, 2, -2, 2) 
        self.pointer = render.attachNewNode(cm.generate())
        self.pointer.setTexture(pointertex)
        self.pointer.setTransparency(True)
        self.pointer.setBillboardPointEye()
        self.pointer.reparentTo(render)
        self.pointer.setScale(256.0/240.0)

    def move(self, x, y, z, tile):
        self.cursor.detachNode()
        self.cursor = loader.loadModel(GAME+"/models/slopes/"+tile['slope'])
        self.cursor.reparentTo( self.matrixContainer )
        self.cursor.setScale(3.7, 3.7, 6.0/7.0*3.7*tile['scale'])
        self.cursor.setTransparency(TransparencyAttrib.MAlpha)
        self.cursor.setTexture(self.curtex)
        self.cursor.setPos(self.battleGraphics.logic2terrain((x, y, z+tile['depth']+0.1)))
        self.pointer.setPos(self.battleGraphics.logic2terrain((x, y, z+tile['depth']+12)))

        if tile['walkable']:
            self.cursor.setColor( 1, 1, 1, .75 )
        else:
            self.cursor.setColor( 1, 0, 0, .75 )

        self.x = x
        self.y = y
        self.z = z

class Matrix(object):

    def __init__(self, battleGraphics, mp):
        self.battleGraphics = battleGraphics
        self.mp = mp
        self.container = render.attachNewNode( "matrixContainer" )

        self.tiles = [ [ [ None for z in range(self.mp['z']) ] for y in range(self.mp['y']) ] for x in range(self.mp['x']) ]

        for x,xs in enumerate(self.mp['tiles']):
            for y,ys in enumerate(xs):
                for z,zs in enumerate(ys):
                    if not self.mp['tiles'][x][y][z] is None:
                        slope = self.mp['tiles'][x][y][z]['slope']
                        scale = self.mp['tiles'][x][y][z]['scale']
                        depth = self.mp['tiles'][x][y][z]['depth']

                        self.tiles[x][y][z] = loader.loadModel(GAME+"/models/slopes/"+slope)
                        self.tiles[x][y][z].reparentTo( self.container )
                        self.tiles[x][y][z].setPos(self.battleGraphics.logic2terrain( (x, y, z+depth+0.05) ))
                        self.tiles[x][y][z].setScale(3.7, 3.7, 6.0/7.0*3.7*scale)
                        self.tiles[x][y][z].setTransparency(TransparencyAttrib.MAlpha)
                        self.tiles[x][y][z].setColor( 0, 0, 0, 0 )

    def placeChars(self, chars):
        self.chars = chars
        self.sprites = {}

        for x,xs in enumerate(self.mp['tiles']):
            for y,ys in enumerate(xs):
                for z,zs in enumerate(ys):
                    if not self.mp['tiles'][x][y][z] is None:
                        slope = self.mp['tiles'][x][y][z]['slope']
                        scale = self.mp['tiles'][x][y][z]['scale']
                        depth = self.mp['tiles'][x][y][z]['depth']

                        if self.mp['tiles'][x][y][z].has_key('char'):
                            charid = self.mp['tiles'][x][y][z]['char']
                            char = self.chars[charid]
                            sprite = Sprite.Sprite(GAME+'/textures/sprites/'+char['sprite']+'.png', int(char['direction']))
                            sprite.animation = 'stand'
                            sprite.node.setPos(self.battleGraphics.logic2terrain((x,y,z)))
                            sprite.node.reparentTo( render )
                            self.sprites[charid] = sprite