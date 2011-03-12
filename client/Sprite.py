from panda3d.core import NodePath
import Sprite2d

class Sprite:

    def __init__(self, sheet, realdir=1):
    
        self.realdir = realdir
        self.camdir = 1
        self.displaydir = 1
        self.status = 'walk'
    
        self.sprite2d = Sprite2d.Sprite2d(sheet, cols=14, rows=4, scale=2.25, anchorX='Center')

        self.node = NodePath("dummy")
        self.node.setBillboardPointEye()
        self.sprite2d.node.reparentTo( self.node )
        self.sprite2d.node.setPos( 0, -0.65, -0.65 )
        
        self.sprite2d.createAnim('walk1', ( 1, 2, 3, 4, 5, 4, 3, 2), fps=10)
        self.sprite2d.createAnim('walk2', (15,16,17,18,19,18,17,16), fps=10)
        self.sprite2d.createAnim('walk3', (29,30,31,32,33,32,31,30), fps=10)
        self.sprite2d.createAnim('walk4', (43,44,45,46,47,46,45,44), fps=10)
        
        self.sprite2d.createAnim('hit1', ( 6, 6), fps=1)
        self.sprite2d.createAnim('hit2', (20,20), fps=1)
        self.sprite2d.createAnim('hit3', (34,34), fps=1)
        self.sprite2d.createAnim('hit4', (48,48), fps=1)
        
        self.sprite2d.createAnim('weak1', ( 7, 7), fps=1)
        self.sprite2d.createAnim('weak2', (21,21), fps=1)
        self.sprite2d.createAnim('weak3', (35,35), fps=1)
        self.sprite2d.createAnim('weak4', (49,49), fps=1)
        
        self.sprite2d.createAnim('dead1', ( 8, 8), fps=1)
        self.sprite2d.createAnim('dead2', (22,22), fps=1)
        self.sprite2d.createAnim('dead3', (36,36), fps=1)
        self.sprite2d.createAnim('dead4', (50,50), fps=1)
        
        self.sprite2d.createAnim('attack1', ( 9,10, 9,13,11,12,11,13), fps=8)
        self.sprite2d.createAnim('attack2', (23,24,23,27,25,26,25,27), fps=8)
        self.sprite2d.createAnim('attack3', (37,38,37,41,39,40,39,41), fps=8)
        self.sprite2d.createAnim('attack4', (51,52,51,55,53,54,53,55), fps=8)

    def setRealDir(self, direction):
        self.realdir = int(direction)

    def updateDisplayDir(self, h, force=False):
        h = self.normalizeh(h)
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
            self.sprite2d.playAnim( self.status+str(tmpdir), loop=True)
            self.displaydir = tmpdir

    def normalizeh(self, h):
        while h > 180:
            h -= 360
        while h < -180:
            h += 360
        return h

