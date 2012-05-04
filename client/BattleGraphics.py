from Config import *
from panda3d.core import *
from panda3d.physics import BaseParticleEmitter,BaseParticleRenderer
from panda3d.physics import PointParticleFactory,SpriteParticleRenderer
from panda3d.physics import LinearNoiseForce,DiscEmitter
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from direct.particles.ForceGroup import ForceGroup

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

    # Draw the gradient background representing the sky during a battle
    def createSky(self):
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
        color.addData4f(VBase4(*self.mp['backgroundcolor1']))
        color.addData4f(VBase4(*self.mp['backgroundcolor1']))
        color.addData4f(VBase4(*self.mp['backgroundcolor2']))
        color.addData4f(VBase4(*self.mp['backgroundcolor2']))
        primitive.addNextVertices(4)
        primitive.closePrimitive()
        geom = Geom(vdata)
        geom.addPrimitive(primitive)
        sky = GeomNode('sky')
        sky.addGeom(geom)
        base.camera.attachNewNode(sky)

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