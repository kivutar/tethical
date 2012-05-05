from Config import *
from panda3d.core import TransparencyAttrib, Texture, CardMaker

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