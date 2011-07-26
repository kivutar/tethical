from pandac.PandaModules import *
from direct.showbase import DirectObject
from panda3d.core import CollisionTraverser, CollisionNode, CollisionHandlerQueue, CollisionRay, BitMask32, CardMaker, NodePath, Texture, TextureStage
from direct.task.Task import Task

GAME = 'lijj'

class Chooser(DirectObject.DirectObject):
    
    def __init__(self, charid, sprite, camhandler, callback, cancelcallback):
        print game
    
        self.charid = charid
        self.sprite = sprite
        self.camhandler = camhandler
        self.callback = callback
        self.cancelcallback = cancelcallback
        self.initdir  = self.sprite.realdir
        self.hidir = None

        # Textures
        self.tex = [ 0 for i in range(4) ]
        for i in range(4):
            self.tex[i] = loader.loadTexture(GAME+'/textures/gui/direction'+str(i)+'.png')
            self.tex[i].setMagfilter(Texture.FTNearest)
            self.tex[i].setMinfilter(Texture.FTNearest)

        # Sounds
        self.hover_snd   = base.loader.loadSfx(GAME+"/sounds/hover.ogg")
        self.clicked_snd = base.loader.loadSfx(GAME+"/sounds/clicked.ogg")
        self.cancel_snd  = base.loader.loadSfx(GAME+"/sounds/cancel.ogg")

        # Buttons container
        self.directionRoot = sprite.node.attachNewNode( "directionRoot" )

        cm = CardMaker('card')
        cm.setFrame(-2, 2, -2, 2) 
        self.card = render.attachNewNode(cm.generate())
        self.card.setTexture(self.tex[self.initdir-1])
        self.card.setTransparency(True)
        self.card.setBillboardPointEye()
        self.card.reparentTo(self.directionRoot)
        self.card.setPos(0,0,6)
        self.card.setScale(256.0/240.0)

        self.accept("b", self.onCircleClicked)
        self.accept("space", self.onCrossClicked)
        self.accept("arrow_up", lambda: self.onArrowClicked('up'))
        self.accept("arrow_down", lambda: self.onArrowClicked('down'))
        self.accept("arrow_left", lambda: self.onArrowClicked('left'))
        self.accept("arrow_right", lambda: self.onArrowClicked('right'))

    def onCircleClicked(self):
        self.directionRoot.removeNode()
        self.ignoreAll()
        self.clicked_snd.play()
        self.callback(self.charid, self.hidir)

    def onCrossClicked(self):
        self.directionRoot.removeNode()
        self.ignoreAll()
        self.cancel_snd.play()
        self.sprite.setRealDir(self.initdir)
        self.cancelcallback()

    def onArrowClicked(self, direction):

        self.hover_snd.play()

        h = self.camhandler.container.getH()
        while h > 180:
            h -= 360
        while h < -180:
            h += 360

        if direction == 'up':
            if h >=    0 and h <  90:
                self.hidir = '1'
                self.card.setTexture(self.tex[0])
            if h >=  -90 and h <   0:
                self.hidir = '4'
                self.card.setTexture(self.tex[3])
            if h >= -180 and h < -90:
                self.hidir = '3'
                self.card.setTexture(self.tex[2])
            if h >=   90 and h < 180:
                self.hidir = '2'
                self.card.setTexture(self.tex[1])
        elif direction == 'down':
            if h >=    0 and h <  90:
                self.hidir = '3'
                self.card.setTexture(self.tex[2])
            if h >=  -90 and h <   0:
                self.hidir = '2'
                self.card.setTexture(self.tex[1])
            if h >= -180 and h < -90:
                self.hidir = '1'
                self.card.setTexture(self.tex[0])
            if h >=   90 and h < 180:
                self.hidir = '4'
                self.card.setTexture(self.tex[3])
        elif direction == 'left':
            if h >=    0 and h <  90:
                self.hidir = '2'
                self.card.setTexture(self.tex[1])
            if h >=  -90 and h <   0:
                self.hidir = '1'
                self.card.setTexture(self.tex[0])
            if h >= -180 and h < -90:
                self.hidir = '4'
                self.card.setTexture(self.tex[3])
            if h >=   90 and h < 180:
                self.hidir = '3'
                self.card.setTexture(self.tex[2])
        elif direction == 'right':
            if h >=    0 and h <  90:
                self.hidir = '4'
                self.card.setTexture(self.tex[3])
            if h >=  -90 and h <   0:
                self.hidir = '3'
                self.card.setTexture(self.tex[2])
            if h >= -180 and h < -90:
                self.hidir = '2'
                self.card.setTexture(self.tex[1])
            if h >=   90 and h < 180:
                self.hidir = '1'
                self.card.setTexture(self.tex[0])

        self.sprite.setRealDir(self.hidir)

