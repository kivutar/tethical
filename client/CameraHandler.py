from direct.directbase import DirectStart
from direct.showbase import DirectObject
from panda3d.core import OrthographicLens
from pandac.PandaModules import Vec3
from direct.interval.IntervalGlobal import LerpPosInterval, LerpScaleInterval, LerpHprInterval, Sequence
import math

class CameraHandler(DirectObject.DirectObject):

    def __init__(self):

        base.disableMouse()

        lens = OrthographicLens()
        lens.setFilmSize(40, 30)
        lens.setNear(10)
        lens.setFar(100)
        base.cam.node().setLens(lens)

        self.container = render.attachNewNode('camContainer')
        base.camera.reparentTo( self.container )
        base.camera.setPos( -20, 0, 24 )
        base.camera.lookAt(0, 0, 0)
        self.container.setHpr(45, 0, 0)

        self.zoomed = False
        self.r      = False

        self.accept("e",            self.toggleZoom  )
        self.accept("r",            self.toggleR     )
        self.accept("a",    lambda: self.turn( 90)   )
        self.accept("z",    lambda: self.turn(-90)   )
        self.accept('window-event', self.windowEvent )

    def toggleZoom(self):
        if self.container.getScale()[0] in (0.5, 1.0):
            if self.zoomed:
                i = LerpScaleInterval(self.container, 0.5, 1.0, 0.5)
            else:
                i = LerpScaleInterval(self.container, 0.5, 0.5, 1.0)
            s = Sequence(i)
            s.start()
            self.zoomed = not self.zoomed

    def toggleR(self):
        (h, p, r) = self.container.getHpr()
        if r in (0.0, -25.0):
            if self.r:
                i = LerpHprInterval(self.container, 0.5, (h, p, r+25), (h, p, r))
            else:
                i = LerpHprInterval(self.container, 0.5, (h, p, r-25), (h, p, r))
            s = Sequence(i)
            s.start()
            self.r = not self.r

    def turn(self, delta):
        (h, p, r) = self.container.getHpr()
        if (h-45)%90 == 0.0:
            i = LerpHprInterval(self.container, 0.5, (h+delta, p, r), (h, p, r))
            s = Sequence(i)
            s.start()

    def move(self, dest):
        orig = self.container.getPos()
        i = LerpPosInterval(self.container, 0.5, dest, startPos=orig)
        s = Sequence(i)
        s.start()

    def windowEvent(self, window):
        ratio = float(window.getXSize()) / float(window.getYSize())
        base.cam.node().getLens().setAspectRatio( ratio )

