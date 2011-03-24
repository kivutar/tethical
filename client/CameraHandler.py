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
        lens.setFilmSize(34.2007, 25.6505)
        lens.setNear(1)
        lens.setFar(100)
        base.cam.node().setLens(lens)

        self.container = render.attachNewNode('camContainer')
        base.camera.reparentTo( self.container )
        base.camera.setPos( -40, 0, 20 )
        base.camera.lookAt(0, 0, 0)
        self.container.setHpr(45, 0, 0)

        self.zoomed = True
        self.r      = False
        
        # Load sounds
        self.toggle_r_snd = base.loader.loadSfx("sounds/camera_toggle_r.ogg")
        self.rotate_snd   = base.loader.loadSfx("sounds/camera_rotate.ogg")

        self.accept("e",            self.toggleZoom  )
        self.accept("r",            self.toggleR     )
        self.accept("a",    lambda: self.rotate( 90) )
        self.accept("z",    lambda: self.rotate(-90) )
        self.accept('window-event', self.windowEvent )

    def toggleZoom(self):
        if round(self.container.getScale()[0]*10) in (10, 14):
            self.toggle_r_snd.play()
            if self.zoomed:
                i = LerpScaleInterval(self.container, 0.25, 1.4, 1.0)
            else:
                i = LerpScaleInterval(self.container, 0.25, 1.0, 1.4)
            s = Sequence(i)
            s.start()
            self.zoomed = not self.zoomed

    def toggleR(self):
        (h, p, r) = self.container.getHpr()
        if r in (0.0, 15.0):
            self.toggle_r_snd.play()
            if self.r:
                i = LerpHprInterval(self.container, 0.25, (h, p, r-15), (h, p, r))
            else:
                i = LerpHprInterval(self.container, 0.25, (h, p, r+15), (h, p, r))
            s = Sequence(i)
            s.start()
            self.r = not self.r

    def rotate(self, delta):
        (h, p, r) = self.container.getHpr()
        if (h-45)%90 == 0.0:
            self.rotate_snd.play()
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

