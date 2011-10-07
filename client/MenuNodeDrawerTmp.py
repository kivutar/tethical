import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from Config import *

v = 1.0/120.0

class MenuNodeDrawer:

    def __init__(self, w, h):

        self.w = w
        self.h = h

    def getNodePath(self):        
   
        textureI = loader.loadTexture(GAME+'/textures/gui/default/menu/body/middle-middle.png',)
        textureI.setMagfilter(Texture.FTNearest)
        textureI.setMinfilter(Texture.FTNearest)
        textureI.setWrapU(Texture.WMRepeat)
        textureI.setWrapV(Texture.WMRepeat)
        
        # container = NodePath('bar')

        # card = CardMaker('foo')
        # nodeWidth = self.w
        # nodeHeight = self.h
        textureWidth = textureI.getOrigFileXSize()
        textureHeight = textureI.getOrigFileYSize()

        # #{'left': textureE.getOrigFileXSize(), 'right': width-textureF.getOrigFileXSize(), 'bottom': textureH.getOrigFileYSize(), 'top': height-textureG.getOrigFileYSize()}

        # #card.setFrame(coordinates[i]["left"], coordinates[i]["right"], coordinates[i]["bottom"], coordinates[i]["top"])
        # card.setUvRange((0,0), (nodeWidth/textureWidth, nodeHeight/textureHeight))
        # container.attachNewNode(card.generate())
        # container.setTexture(textureI)

        cm = CardMaker('card')
        #cm.setFrame(-self.w/2.0, self.w/2.0, -self.h/2.0, self.h/2.0)
        cm.setFrame(
            -v*(self.w-4)/2,
             v*(self.w-4)/2,
            -v*(self.h-4)/2,
             v*(self.h-4)/2,
        )
        cm.setUvRange((0,0), (self.w/textureWidth*2, self.h/textureHeight*2))
        card = render.attachNewNode(cm.generate())
        card.setTexture(textureI)
        card.setTransparency(True)
        card.setBillboardPointEye()
        card.setPos((0,0,0))

        return card
