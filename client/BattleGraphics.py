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

