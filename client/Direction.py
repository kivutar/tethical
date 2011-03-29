from direct.showbase import DirectObject
from panda3d.core import CollisionTraverser, CollisionNode, CollisionHandlerQueue, CollisionRay, BitMask32, CardMaker, NodePath, Texture, TextureStage
from direct.task.Task import Task

class Chooser(DirectObject.DirectObject):
    
    def __init__(self, charid, sprite, callback, cancelcallback):
    
        self.charid   = charid
        self.sprite   = sprite
        self.callback = callback
        self.cancelcallback = cancelcallback
        self.initdir  = self.sprite.realdir

        # Collision stuff
        self.picker = CollisionTraverser()
        self.pq     = CollisionHandlerQueue()
        pickerNode = CollisionNode('mouseRay')
        pickerNP = camera.attachNewNode(pickerNode)
        pickerNode.setFromCollideMask(BitMask32.bit(1))
        self.pickerRay = CollisionRay()
        pickerNode.addSolid(self.pickerRay)
        self.picker.addCollider(pickerNP, self.pq)
        self.hidir = None
        self.odir = False

        # Textures
        self.readytex = loader.loadTexture('textures/gui/direction.png')
        self.readytex.setMagfilter(Texture.FTNearest)
        self.readytex.setMinfilter(Texture.FTNearest)
        self.hovertex = loader.loadTexture('textures/gui/direction_hover.png')
        self.hovertex.setMagfilter(Texture.FTNearest)
        self.hovertex.setMinfilter(Texture.FTNearest)

        # Sounds
        self.hover_snd   = base.loader.loadSfx("sounds/hover.ogg")
        self.clicked_snd = base.loader.loadSfx("sounds/clicked.ogg")
        self.cancel_snd  = base.loader.loadSfx("sounds/cancel.ogg")

        # Buttons list
        self.directionbuttons = []

        # Buttons container
        self.directionRoot = sprite.node.attachNewNode( "directionRoot" )
        #self.directionRoot.setPos(-.5,0,0)

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
            card.setScale(.8)
            card.node().setIntoCollideMask( BitMask32.bit(1) )
            card.node().setTag('direction', directiondata['direction'])
            self.directionbuttons.append(card)

        self.directiontask = taskMgr.add( self.hightlightDirectionTask, 'hightlightDirectionTask' )
        self.accept("mouse1", self.clicked)

    def clicked(self):
        self.directiontask.remove()
        self.directionRoot.removeNode()
        self.ignoreAll()
        if self.hidir:
            self.clicked_snd.play()
            self.callback(self.charid, self.hidir)
        else:
            self.cancel_snd.play()
            self.sprite.setRealDir(self.initdir)
            self.cancelcallback()

    def hightlightDirectionTask(self, task):
        for directionbutton in self.directionbuttons:
            directionbutton.setTexture(self.readytex)
        self.hidir = None

        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse()
            self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())
            self.picker.traverse(self.directionRoot)

            if self.pq.getNumEntries() > 0:
                self.pq.sortEntries()
                NodePath(self.pq.getEntry(0).getIntoNode()).setTexture(self.hovertex)
                self.hidir = self.pq.getEntry(0).getIntoNode().getTag('direction')
                if not self.odir:
                    self.hover_snd.play()
                    self.sprite.setRealDir(self.hidir)
                    self.odir = True
            else:
                self.odir = False

        return Task.cont

