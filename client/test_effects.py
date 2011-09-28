from Config import *
import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from pandac.PandaModules import PandaNode,NodePath,Camera,TextNode,GeomTristrips,Geom,GeomVertexFormat,GeomVertexData,GeomVertexWriter,GeomNode,TransformState,OrthographicLens,TextureStage,TexGenAttrib,PNMImage,Texture,ColorBlendAttrib
from panda3d.core import *
from direct.gui.DirectGui import *
from direct.task import Task
import Effect
import Sprite
from CameraHandler import CameraHandler

camhandler = CameraHandler()

tile = loader.loadModel(GAME+"/models/slopes/flat" )
tile.setScale(3.0)
tile.reparentTo( render )
tile.setColor(0, 0, 1, 1)
sprite = Sprite.Sprite(GAME+'/textures/sprites/4C_F_1.png', 1)
sprite.node.reparentTo( render )

tile2 = loader.loadModel(GAME+"/models/slopes/flat" )
tile2.setScale(3.0)
tile2.reparentTo( render )
tile2.setColor(0, 0, 1, 1)
tile2.setPos(-9, 0, 0)
sprite2 = Sprite.Sprite(GAME+'/textures/sprites/4C_F_1.png', 1)
sprite2.node.reparentTo(render)
sprite2.node.setPos(-9, 0, 0)

class Effect:

	def __init__(self, filename, pos):
		tex = loader.loadTexture(filename)
		tex.setMagfilter(Texture.FTNearest)
		tex.setMinfilter(Texture.FTNearest)

		cm = CardMaker('card')
		cm.setFrame(-2, 2, -4, 4)
		card = render.attachNewNode(cm.generate())
		card.setTexture(tex)
		card.setTransparency(True)
		card.setBillboardPointEye()
		card.reparentTo(render)
		card.setPos(*pos)
		card.setColor(1,1,1,.75)
		card.setScale(256.0/240.0)

ef = Effect('test.png', (0,0,4))
ef2 = Effect('test.png', (-9,0,4))

run()