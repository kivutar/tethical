from direct.directbase import DirectStart
from direct.showbase import DirectObject
from panda3d.core import OrthographicLens
from pandac.PandaModules import Vec3
import math

class CameraHandler(DirectObject.DirectObject):

    def __init__(self):

        base.disableMouse()
        base.camera.lookAt(0, 0, 0)
        
        lens = OrthographicLens()
        lens.setFilmSize(30, 20)
        #lens.setNear(-32768)
        #lens.setFar(131072)
        base.cam.node().setLens(lens)
        
        camera.setPosHpr(-20, -20, 24, -45, -35, 0)
        
        self.rotating = False
        self.moving = False
        self.target = Vec3()
        self.camDist = 40
        self.mx, self.my = 0, 0 
        self.setTarget(0, 0, 0)
        self.turnCameraAroundPoint(0, 0, self.target, self.camDist)
        
        self.accept("mouse3",     self.startRotate)
        self.accept("mouse3-up",  self.stopRotate)
        #self.accept("mouse1",     self.startMove)
        #self.accept("mouse1-up",  self.stopMove)
        self.accept("wheel_up",   self.zoomIn)
        self.accept("wheel_down", self.zoomOut)
        
        taskMgr.add(self.rotateTask, 'rotateTask')
        taskMgr.add(self.moveTask,   'moveTask'  )

    def turnCameraAroundPoint(self, tx, ty, p, dist):
        newCamHpr=Vec3()         
        camHpr=base.camera.getHpr()
        newCamHpr.setX(camHpr.getX()+tx)
        newCamHpr.setY(camHpr.getY()-ty)
        base.camera.setHpr(newCamHpr)
        angleradiansX = newCamHpr.getX() * (math.pi / 180.0)
        angleradiansY = newCamHpr.getY() * (math.pi / 180.0)
        base.camera.setPos( dist*math.sin(angleradiansX)*math.cos(angleradiansY)+p.getX(),
                           -dist*math.cos(angleradiansX)*math.cos(angleradiansY)+p.getY(),
                           24.0 )
        base.camera.lookAt(0, 0, 0)

    def setTarget(self, x, y, z):
        self.target.setX(x)
        self.target.setY(y)
        self.target.setZ(z)

    def startRotate(self):
        self.rotating=True

    def stopRotate(self):
        self.rotating=False

    def startMove(self):
        self.moving=True

    def stopMove(self):
        self.moving=False

    def zoomIn(self):
        if base.mouseWatcherNode.hasMouse():
            lens = base.cam.node().getLens()
            size = lens.getFilmSize()
            lens.setFilmSize(size / 1.1)

    def zoomOut(self):
        if base.mouseWatcherNode.hasMouse():
            lens = base.cam.node().getLens()
            size = lens.getFilmSize()
            lens.setFilmSize(size * 1.1)

    def rotateTask(self, task):
        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse() 
            if self.rotating:
                self.turnCameraAroundPoint(
                    (self.mx-mpos.getX())*100,
                    0,
                    self.target,self.camDist)
            self.mx=mpos.getX()
            self.my=mpos.getY()                               
        return task.cont

    def moveTask(self, task):
        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse() 
            if self.moving:
                newCamHpr=Vec3()
                camHpr=base.camera.getHpr()
                #newCamHpr.setZ(mpos.getY())
                base.camera.setHpr(newCamHpr)
                base.camera.lookAt(0, 0, 0)                           
        return task.cont

