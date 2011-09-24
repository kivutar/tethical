from Config import *
import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from pandac.PandaModules import PandaNode,NodePath,Camera,TextNode,GeomTristrips,Geom,GeomVertexFormat,GeomVertexData,GeomVertexWriter,GeomNode,TransformState,OrthographicLens,TextureStage,TexGenAttrib,PNMImage,Texture,ColorBlendAttrib
from direct.gui.DirectGui import *
from direct.task import Task
import Effect
import Sprite
from CameraHandler import CameraHandler

camhandler = CameraHandler()

sprite = Sprite.Sprite(GAME+'/textures/sprites/4C_F_1.png', 1)
sprite.node.reparentTo( render )
# for debug purpose
#sprite.node.place()

tile = loader.loadModel(GAME+"/models/slopes/flat" )
tile.setScale(3.0)
tile.reparentTo( render )
tile.setColor( 0, 0, 1, 1 )

tile2 = loader.loadModel(GAME+"/models/slopes/flat" )
tile2.setScale(3.0)
tile2.reparentTo( render )
tile2.setColor( 0, 0, 1, 1 )
tile2.setPos( -9, 0, 0 )

loadedEffect = Effect.Effect(render, 'cure.fft-E001.bmp', True)
def runEffect(task):
    loadedEffect.pandaRender()
    loadedEffect.advanceFrame()
    task.delayTime = loadedEffect.effectTargetMS * 0.001
    #return task.done
    if loadedEffect.hasEffectFinished() == False:
        return task.again
    else:
        return task.done

taskMgr.doMethodLater(0, runEffect, 'run-effect')

run()