from Config import *
import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from pandac.PandaModules import PandaNode,NodePath,Camera,TextNode,GeomTristrips,Geom,GeomVertexFormat,GeomVertexData,GeomVertexWriter,GeomNode,TransformState,OrthographicLens,TextureStage,TexGenAttrib,PNMImage,Texture,ColorBlendAttrib
from panda3d.core import *
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.task import Task
import Effect
import Sprite
from CameraHandler import CameraHandler

camhandler = CameraHandler()

terrain = render.attachNewNode('terrain')

tile1 = loader.loadModel(GAME+"/models/slopes/flat" )
tile1.setScale(3.0)
tile1.reparentTo(terrain)
tile1.setColor(0, 0, 1, 1)
tile1.setPos(9, 0, 0)
sprite1 = Sprite.Sprite(GAME+'/textures/sprites/4C_F_1.png', 3)
sprite1.node.reparentTo(terrain)
sprite1.node.setPos(9, 0, 0)

tile2 = loader.loadModel(GAME+"/models/slopes/flat" )
tile2.setScale(3.0)
tile2.reparentTo(terrain)
tile2.setColor(0, 0, 1, 1)
tile2.setPos(-9, 0, 0)
sprite2 = Sprite.Sprite(GAME+'/textures/sprites/4C_F_1.png', 1)
sprite2.node.reparentTo(terrain)
sprite2.node.setPos(-9, 0, 0)

def rotationTask(task):
    h = task.time * 30
    camhandler.container.setHpr(h,0,0)
    return Task.cont

def characterDirectionTask(task):
    h = camhandler.container.getH()
    sprite1.updateDisplayDir(h)
    sprite2.updateDisplayDir(h)
    return Task.cont

def updateSpriteAnimation(sprite, animation):
    sprite.animation = animation
    h = camhandler.container.getH()
    sprite.updateDisplayDir( h, True )

class Effect:

	def __init__(self, filename, parent):

		tex = loader.loadTexture(filename)
		tex.setMagfilter(Texture.FTNearest)
		tex.setMinfilter(Texture.FTNearest)

		cm = CardMaker('card')
		cm.setFrame(-2, 2, -4, 4)
		self.card = render.attachNewNode(cm.generate())
		self.card.setTexture(tex)
		self.card.setTransparency(True)
		self.card.setBillboardPointEye()
		self.card.reparentTo(parent)
		self.card.setColor(1,1,1,0)
		self.card.setScale(256.0/240.0)
	
	def getSequence(self):
		return Sequence(
			Parallel(
				LerpScaleInterval(self.card, 1.0, 1        , 0.1      ),
				LerpColorInterval(self.card, 1.0, (1,1,1,1), (1,1,1,0)),
				LerpPosInterval(  self.card, 1.0, (0,0,0)  , (0,0,10) ),
			),
			Parallel(
				LerpScaleInterval(self.card, 0.5, 10       , 1        ),
				LerpColorInterval(self.card, 0.5, (1,1,1,0), (1,1,1,1)),
			)
		)

taskMgr.add(rotationTask, 'rotationTask')
taskMgr.add(characterDirectionTask, 'characterDirectionTask')

Sequence(
	Func(updateSpriteAnimation, sprite1, 'attack'),
	Func(updateSpriteAnimation, sprite2, 'hit'),
	Effect('test.png', sprite2.node).getSequence(),
	Func(updateSpriteAnimation, sprite2, 'attack'),
	Func(updateSpriteAnimation, sprite1, 'hit'),
	Effect('test.png', sprite1.node).getSequence(),
).loop()

run()