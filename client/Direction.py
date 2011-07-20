from panda3d.core import loadPrcFile
loadPrcFile("../config.prc")
from pandac.PandaModules import *
from direct.showbase import DirectObject
from panda3d.core import CollisionTraverser, CollisionNode, CollisionHandlerQueue, CollisionRay, BitMask32, CardMaker, NodePath, Texture, TextureStage
from direct.task.Task import Task

game = ConfigVariableString('game', 'fft').getValue()

class Chooser(DirectObject.DirectObject):
    
    def __init__(self, charid, sprite, camhandler, callback, cancelcallback):
    
        self.charid = charid
        self.sprite = sprite
        self.camhandler = camhandler
        self.callback = callback
        self.cancelcallback = cancelcallback
        self.initdir  = self.sprite.realdir
        self.hidir = None

        # Textures
        self.readytex = loader.loadTexture(game+'/textures/gui/direction.png')
        self.readytex.setMagfilter(Texture.FTNearest)
        self.readytex.setMinfilter(Texture.FTNearest)
        self.hovertex = loader.loadTexture(game+'/textures/gui/direction_hover.png')
        self.hovertex.setMagfilter(Texture.FTNearest)
        self.hovertex.setMinfilter(Texture.FTNearest)

        # Sounds
        self.hover_snd   = base.loader.loadSfx(game+"/sounds/hover.ogg")
        self.clicked_snd = base.loader.loadSfx(game+"/sounds/clicked.ogg")
        self.cancel_snd  = base.loader.loadSfx(game+"/sounds/cancel.ogg")

        # Buttons list
        self.directionbuttons = []

        # Buttons container
        self.directionRoot = sprite.node.attachNewNode( "directionRoot" )

        directionsdata = [
            { 'direction': '1', 'pos': ( 1.45, 0.0, 5) },
            { 'direction': '2', 'pos': ( 0.0, 1.45, 5) },
            { 'direction': '3', 'pos': (-1.45, 0.0, 5) },
            { 'direction': '4', 'pos': ( 0.0,-1.45, 5) }
        ]
        for directiondata in directionsdata:
            cm = CardMaker('card')
            cm.setFrame(-.5, .5, -.5, .5) 
            card = render.attachNewNode(cm.generate())
            card.setTexture(self.readytex)
            card.setTransparency(True)
            card.setBillboardPointEye()
            card.reparentTo(self.directionRoot)
            card.setPos(directiondata['pos'])
            card.setScale(256.0/240.0)

            self.directionbuttons.append(card)

            if int(directiondata['direction']) == int(self.initdir):
                self.hidir = directiondata['direction']
                card.setTexture(self.hovertex)

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

        for directionbutton in self.directionbuttons:
            directionbutton.setTexture(self.readytex)

        h = self.camhandler.container.getH()
        while h > 180:
            h -= 360
        while h < -180:
            h += 360

        if direction == 'up':
            if h >=    0 and h <  90:
                self.directionbuttons[0].setTexture(self.hovertex)
                self.hidir = '1'
            if h >=  -90 and h <   0:
                self.directionbuttons[3].setTexture(self.hovertex)
                self.hidir = '4'
            if h >= -180 and h < -90:
                self.directionbuttons[2].setTexture(self.hovertex)
                self.hidir = '3'
            if h >=   90 and h < 180:
                self.directionbuttons[1].setTexture(self.hovertex)
                self.hidir = '2'
        elif direction == 'down':
            if h >=    0 and h <  90:
                self.directionbuttons[2].setTexture(self.hovertex)
                self.hidir = '3'
            if h >=  -90 and h <   0:
                self.directionbuttons[1].setTexture(self.hovertex)
                self.hidir = '2'
            if h >= -180 and h < -90:
                self.directionbuttons[0].setTexture(self.hovertex)
                self.hidir = '1'
            if h >=   90 and h < 180:
                self.directionbuttons[3].setTexture(self.hovertex)
                self.hidir = '4'
        elif direction == 'left':
            if h >=    0 and h <  90:
                self.directionbuttons[1].setTexture(self.hovertex)
                self.hidir = '2'
            if h >=  -90 and h <   0:
                self.directionbuttons[0].setTexture(self.hovertex)
                self.hidir = '1'
            if h >= -180 and h < -90:
                self.directionbuttons[3].setTexture(self.hovertex)
                self.hidir = '4'
            if h >=   90 and h < 180:
                self.directionbuttons[2].setTexture(self.hovertex)
                self.hidir = '3'
        elif direction == 'right':
            if h >=    0 and h <  90:
                self.directionbuttons[3].setTexture(self.hovertex)
                self.hidir = '4'
            if h >=  -90 and h <   0:
                self.directionbuttons[2].setTexture(self.hovertex)
                self.hidir = '3'
            if h >= -180 and h < -90:
                self.directionbuttons[1].setTexture(self.hovertex)
                self.hidir = '2'
            if h >=   90 and h < 180:
                self.directionbuttons[0].setTexture(self.hovertex)
                self.hidir = '1'

        self.sprite.setRealDir(self.hidir)

