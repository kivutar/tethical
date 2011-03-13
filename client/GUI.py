import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.DirectGui import *
from direct.task import Task
from direct.actor import Actor
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *

class Menu(object):

    displayed = False

    def __init__(self, movecommand, attackcommand, waitcommand):
    
        if not Menu.displayed:

            texture = loader.loadTexture('textures/gui/gui.png')
            texture.setMagfilter(Texture.FTNearest)
            texture.setMinfilter(Texture.FTNearest)

            #create a frame
            self.frame = DirectFrame(
                frameTexture = texture,
                frameSize    = ( -.25, .25, -.25, .25 ),
                )
            self.frame.setTransparency(True)

            moveBtn = DirectButton(
                text  = ("Move", "Move", "Move", "disabled"), 
                scale = 0.05,
                command = lambda: self.commandanddestroy(movecommand)
                )
            moveBtn.reparentTo( self.frame )
            moveBtn.setPos(0, 0, 0.1)

            attackBtn = DirectButton(
                text  = ("Attack", "Attack", "Attack", "disabled"), 
                scale = 0.05,
                command = lambda: self.commandanddestroy(attackcommand),
                )
            attackBtn.reparentTo( self.frame )
            attackBtn.setPos(0, 0, 0.0)

            waitBtn = DirectButton(
                text  = ("Wait", "Wait", "Wait", "disabled"), 
                scale = 0.05,
                command = lambda: self.commandanddestroy(waitcommand),
                )
            waitBtn.reparentTo( self.frame )
            waitBtn.setPos(0, 0, -0.1)

            cancelBtn = DirectButton(
                text  = ("Cancel", "Cancel", "Cancel", "disabled"), 
                scale = 0.05,
                command = self.destroy
                )
            cancelBtn.reparentTo( self.frame )
            cancelBtn.setPos(0, 0, -0.2)

            self.frame.setPos(0.5, 0, 0)

            Menu.displayed = True

    def destroy(self):
        self.frame.destroy()
        Menu.displayed = False

    def commandanddestroy(self, command):
        command()
        self.destroy()

