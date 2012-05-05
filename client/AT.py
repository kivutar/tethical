from Config import *

# Displays the Active Time flag on a sprite
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