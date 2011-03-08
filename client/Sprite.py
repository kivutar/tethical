from panda3d.core import NodePath
import Sprite2d

class Sprite:

    def __init__(self, sheet, realdir=1):
    
        self.realdir = realdir
        self.camdir = 1
        self.displaydir = 1
        self.status = 'walk'
    
        self.sprite2d = Sprite2d.Sprite2d(sheet, cols=6, rows=4, scale=2, anchorX='Center')

        self.node = NodePath("dummy")
        self.node.setBillboardPointEye()
        self.sprite2d.node.reparentTo( self.node )
        self.sprite2d.node.setPos( 0, -0.65, -0.65 )
        
        self.sprite2d.createAnim('walk1', ( 1, 2, 3, 4, 5, 4, 3, 2), fps=10)
        self.sprite2d.createAnim('walk2', ( 7, 8, 9,10,11,10, 9, 8), fps=10)
        self.sprite2d.createAnim('walk3', (13,14,15,16,17,16,15,14), fps=10)
        self.sprite2d.createAnim('walk4', (19,20,21,22,23,22,21,20), fps=10)

    def setRealDir(self, direction):
        self.realdir = int(direction)

    def updateDisplayDir(self, h):
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
        if tmpdir != self.displaydir:
            self.sprite2d.playAnim( self.status+str(tmpdir), loop=True)
            self.displaydir = tmpdir

    def normalizeh(self, h):
        while h > 180:
            h -= 360
        while h < -180:
            h += 360
        return h

