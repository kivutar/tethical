from panda3d.core import loadPrcFile
from pandac.PandaModules import *
loadPrcFile("../config.prc")
GAME = ConfigVariableString('game', 'fft').getValue()
loadPrcFile(game+"/config.prc")
scale = float( ConfigVariableString('spritescale', '2').getValue() )

from panda3d.core import NodePath, TransparencyAttrib
from pandac.PandaModules import Texture, TextureStage
import Sprite2d

class Sprite:

    def __init__(self, sheet, realdir=1):
    
        self.realdir    = realdir
        self.camdir     = 1
        self.displaydir = 1
        self.animation  = 'walk'
    
        self.sprite2d = Sprite2d.Sprite2d(sheet, cols=14, rows=4, scale=scale*0.7*256.0/240.0, anchorX='Center')

        # the main container
        self.node = NodePath("dummy1")

        # the billboard container
        self.node2 = NodePath("dummy2")
        self.node2.setBillboardPointEye()
        self.node2.reparentTo( self.node )
        self.sprite2d.node.reparentTo( self.node2 )
        self.sprite2d.node.setPos( 0, -1.5, -1.5 )
        
        # shadow
        self.shadow = loader.loadModel(GAME+'/models/slopes/flat')
        self.shadow.setZ(0.075)
        self.shadow.setScale(3.7)
        self.shadow.setTransparency(TransparencyAttrib.MAlpha)
        self.shadowtexture = loader.loadTexture(GAME+'/textures/shadow.png')
        self.shadowtexture.setMagfilter(Texture.FTNearest)
        self.shadowtexture.setMinfilter(Texture.FTNearest)
        self.shadowtexture.setWrapU(Texture.WMRepeat)
        self.shadowtexture.setWrapV(Texture.WMClamp)
        self.shadow.setTexture( self.shadowtexture )
        self.shadow.reparentTo( self.node )

        # animations
        self.sprite2d.createAnim('stand1', ( 0, 0), fps=10)
        self.sprite2d.createAnim('stand2', (14,14), fps=10)
        self.sprite2d.createAnim('stand3', (28,28), fps=10)
        self.sprite2d.createAnim('stand4', (42,42), fps=10)

        self.sprite2d.createAnim('smalljump1', ( 1, 1), fps=10)
        self.sprite2d.createAnim('smalljump2', (15,15), fps=10)
        self.sprite2d.createAnim('smalljump3', (29,29), fps=10)
        self.sprite2d.createAnim('smalljump4', (43,43), fps=10)

        self.sprite2d.createAnim('walk1', ( 1, 2, 3, 4, 5, 4, 3, 2), fps=10)
        self.sprite2d.createAnim('walk2', (15,16,17,18,19,18,17,16), fps=10)
        self.sprite2d.createAnim('walk3', (29,30,31,32,33,32,31,30), fps=10)
        self.sprite2d.createAnim('walk4', (43,44,45,46,47,46,45,44), fps=10)

        self.sprite2d.createAnim('run1', ( 1, 2, 3, 4, 5, 4, 3, 2), fps=15)
        self.sprite2d.createAnim('run2', (15,16,17,18,19,18,17,16), fps=15)
        self.sprite2d.createAnim('run3', (29,30,31,32,33,32,31,30), fps=15)
        self.sprite2d.createAnim('run4', (43,44,45,46,47,46,45,44), fps=15)
        
        self.sprite2d.createAnim('hit1', ( 6, 6), fps=10)
        self.sprite2d.createAnim('hit2', (20,20), fps=10)
        self.sprite2d.createAnim('hit3', (34,34), fps=10)
        self.sprite2d.createAnim('hit4', (48,48), fps=10)
        
        self.sprite2d.createAnim('weak1', ( 7, 7), fps=10)
        self.sprite2d.createAnim('weak2', (21,21), fps=10)
        self.sprite2d.createAnim('weak3', (35,35), fps=10)
        self.sprite2d.createAnim('weak4', (49,49), fps=10)
        
        self.sprite2d.createAnim('dead1', ( 8, 8), fps=10)
        self.sprite2d.createAnim('dead2', (22,22), fps=10)
        self.sprite2d.createAnim('dead3', (36,36), fps=10)
        self.sprite2d.createAnim('dead4', (50,50), fps=10)
        
        self.sprite2d.createAnim('attack1', ( 9,10, 9,13,11,12,11,13), fps=8)
        self.sprite2d.createAnim('attack2', (23,24,23,27,25,26,25,27), fps=8)
        self.sprite2d.createAnim('attack3', (37,38,37,41,39,40,39,41), fps=8)
        self.sprite2d.createAnim('attack4', (51,52,51,55,53,54,53,55), fps=8)

    def setRealDir(self, direction):
        self.realdir = int(direction)

    def updateDisplayDir(self, h, force=False):
        h = self.normalizeH(h)
        if h >=    0 and h <  90:
            self.camdir = 2
        if h >=  -90 and h <   0:
            self.camdir = 3
        if h >= -180 and h < -90:
            self.camdir = 4
        if h >=   90 and h < 180:
            self.camdir = 1
        
        tmpdir = self.realdir + self.camdir
        if tmpdir > 4:
            tmpdir -= 4
        if tmpdir != self.displaydir or force:
            self.sprite2d.playAnim( self.animation+str(tmpdir), loop=True)
            self.displaydir = tmpdir

    def normalizeH(self, h):
        while h > 180:
            h -= 360
        while h < -180:
            h += 360
        return h

