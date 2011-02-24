import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.DirectGui import *
from direct.task import Task
from direct.actor import Actor
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *

class Menu:

    def __init__(self):
    
        texture = loader.loadTexture('textures/gui/gui.png')
        texture.setMagfilter(Texture.FTNearest)
        texture.setMinfilter(Texture.FTNearest)

        #create a frame
        frame = DirectFrame(
            frameTexture = texture,
            frameSize    = ( -.25, .25, -.25, .25 ),
            )
        frame.setTransparency(True)

        moveBtn = DirectButton(
            text  = ("Move", "Move", "Move", "disabled"), 
            scale = 0.05
            )
        moveBtn.reparentTo( frame )
        moveBtn.setPos(0, 0, 0)

        frame.setPos(0.5, 0, 0)

