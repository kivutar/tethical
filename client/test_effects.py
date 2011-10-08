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

taskMgr.add(rotationTask, 'rotationTask')
taskMgr.add(characterDirectionTask, 'characterDirectionTask')

Sequence(
    Func(updateSpriteAnimation, sprite1, 'attack'),
    Func(updateSpriteAnimation, sprite2, 'hit'),
    #Effect.Effect('cure.fft-E001.bmp', sprite2.node, True).getSequence(),
    Effect.Effect('ice.fft-E024.bmp', sprite2.node, True, False, [0,0,-2]).getSequence(),
    #Effect.Effect('bizen-boat.fft-E135.bmp', sprite2.node, True).getSequence(),
    #Effect.Effect('death.fft-E030-color.bmp', sprite2.node, True).getSequence(),
    #Effect.Effect('dark-blade.fft-E172.bmp', sprite2.node, True, True, [0,0,3]).getSequence(),
    #Effect.Effect('dark-blade.fft-E172-color.bmp', sprite2.node, True, True, [0,0,3]).getSequence(),
    Func(updateSpriteAnimation, sprite2, 'attack'),
    Func(updateSpriteAnimation, sprite1, 'hit'),
    Effect.Effect('cure.fft-E001.bmp', sprite1.node, True).getSequence()
    #Effect.Effect('night-sword.fft-E173.bmp', sprite1.node, True, False, [0,0,-2]).getSequence()
    #Effect.Effect('cure-it-with-fire.fft-E001.png', sprite1.node, True).getSequence()
    #Effect.Effect('ice.fft-E024.bmp', sprite1.node, True, False, [0,0,-2]).getSequence()
).loop()

run()