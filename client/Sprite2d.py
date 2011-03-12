from pandac.PandaModules import NodePath, PNMImageHeader, PNMImage, Filename, CardMaker, TextureStage, Texture, TransparencyAttrib
from math import log, modf

class Sprite2d:

    class Cell:
        def __init__(self, col, row):
            self.col = col
            self.row = row
       
        def __str__(self):
            return "Cell - Col %d, Row %d" % (self.col, self.row)
       
    class Animation:
        def __init__(self, cells, fps):
            self.cells = cells
            self.fps = fps
            self.playhead = 0

    ALIGN_CENTER = "Center"
    ALIGN_LEFT = "Left"
    ALIGN_RIGHT = "Right"
    ALIGN_BOTTOM = "Bottom"
    ALIGN_TOP = "Top"
   
    TRANS_ALPHA = TransparencyAttrib.MAlpha
    TRANS_DUAL = TransparencyAttrib.MDual
    # One pixel is divided by this much. If you load a 100x50 image with PIXEL_SCALE of 10.0
    # you get a card that is 1 unit wide, 0.5 units high
    PIXEL_SCALE = 10.0

    def __init__(self, image_path, name=None,\
                  rows=1, cols=1, scale=1.0,\
                  twoSided=True, alpha=TRANS_ALPHA,\
                  repeatX=1, repeatY=1,\
                  anchorX=ALIGN_LEFT, anchorY=ALIGN_BOTTOM):
        """
        Create a card textured with an image. The card is sized so that the ratio between the
        card and image is the same.
        """
       
        scale *= self.PIXEL_SCALE
       
        self.animations = {}
       
        self.scale = scale
        self.repeatX = repeatX
        self.repeatY = repeatY
        self.flip = {'x':False,'y':False}
        self.rows = rows
        self.cols = cols
       
        self.currentFrame = 0
        self.currentAnim = None
        self.loopAnim = False
        self.frameInterrupt = True
       
        # Create the NodePath
        if name:
            self.node = NodePath("Sprite2d:%s" % name)
        else:
            self.node = NodePath("Sprite2d:%s" % image_path)
       
        # Set the attribute for transparency/twosided
        self.node.node().setAttrib(TransparencyAttrib.make(alpha))
        if twoSided:
            self.node.setTwoSided(True)
       
        # Make a filepath
        self.imgFile = Filename(image_path)
        if self.imgFile.empty():
            raise IOError, "File not found"
       
        # Instead of loading it outright, check with the PNMImageHeader if we can open
        # the file.
        imgHead = PNMImageHeader()
        if not imgHead.readHeader(self.imgFile):
            raise IOError, "PNMImageHeader could not read file. Try using absolute filepaths"
       
        # Load the image with a PNMImage
        image = PNMImage()
        image.read(self.imgFile)
       
        self.sizeX = image.getXSize()
        self.sizeY = image.getYSize()
       
        self.frames = []
        for rowIdx in xrange(self.rows):
            for colIdx in xrange(self.cols):
                self.frames.append(Sprite2d.Cell(colIdx, rowIdx))
       
        # We need to find the power of two size for the another PNMImage
        # so that the texture thats loaded on the geometry won't have artifacts
        textureSizeX = self.nextsize(self.sizeX)
        textureSizeY = self.nextsize(self.sizeY)
       
        # The actual size of the texture in memory
        self.realSizeX = textureSizeX
        self.realSizeY = textureSizeY
       
        self.paddedImg = PNMImage(textureSizeX, textureSizeY)
        if image.hasAlpha():
            self.paddedImg.alphaFill(0)
        # Copy the source image to the image we're actually using
        self.paddedImg.blendSubImage(image, 0, 0)
        # We're done with source image, clear it
        image.clear()
       
        # The pixel sizes for each cell
        self.colSize = self.sizeX/self.cols
        self.rowSize = self.sizeY/self.rows
       
        # How much padding the texture has
        self.paddingX = textureSizeX - self.sizeX
        self.paddingY = textureSizeY - self.sizeY
       
        # Set UV padding
        self.uPad = float(self.paddingX)/textureSizeX
        self.vPad = float(self.paddingY)/textureSizeY
       
        # The UV dimensions for each cell
        self.uSize = (1.0 - self.uPad) / self.cols
        self.vSize = (1.0 - self.vPad) / self.rows
       
        card = CardMaker("Sprite2d-Geom")

        # The positions to create the card at
        if anchorX == self.ALIGN_LEFT:
            posLeft = 0
            posRight = (self.colSize/scale)*repeatX
        elif anchorX == self.ALIGN_CENTER:
            posLeft = -(self.colSize/2.0/scale)*repeatX
            posRight = (self.colSize/2.0/scale)*repeatX
        elif anchorX == self.ALIGN_RIGHT:
            posLeft = -(self.colSize/scale)*repeatX
            posRight = 0
       
        if anchorY == self.ALIGN_BOTTOM:
            posTop = 0
            posBottom = (self.rowSize/scale)*repeatY
        elif anchorY == self.ALIGN_CENTER:
            posTop = -(self.rowSize/2.0/scale)*repeatY
            posBottom = (self.rowSize/2.0/scale)*repeatY
        elif anchorY == self.ALIGN_TOP:
            posTop = -(self.rowSize/scale)*repeatY
            posBottom = 0
       
        card.setFrame(posLeft, posRight, posTop, posBottom)
        card.setHasUvs(True)
        self.card = self.node.attachNewNode(card.generate())
       
        # Since the texture is padded, we need to set up offsets and scales to make
        # the texture fit the whole card
        self.offsetX = (float(self.colSize)/textureSizeX)
        self.offsetY = (float(self.rowSize)/textureSizeY)
       
        self.node.setTexScale(TextureStage.getDefault(), self.offsetX * repeatX, self.offsetY * repeatY)
        self.node.setTexOffset(TextureStage.getDefault(), 0, 1-self.offsetY)
       
        self.texture = Texture()
       
        self.texture.setXSize(textureSizeX)
        self.texture.setYSize(textureSizeY)
        self.texture.setZSize(1)
       
        # Load the padded PNMImage to the texture
        self.texture.load(self.paddedImg)

        self.texture.setMagfilter(Texture.FTNearest)
        self.texture.setMinfilter(Texture.FTNearest)
       
        #Set up texture clamps according to repeats
        if repeatX > 1:
            self.texture.setWrapU(Texture.WMRepeat)
        else:
            self.texture.setWrapU(Texture.WMClamp)
        if repeatY > 1:
            self.texture.setWrapV(Texture.WMRepeat)
        else:
            self.texture.setWrapV(Texture.WMClamp)
       
        self.node.setTexture(self.texture)
    
    def nextsize(self, num):
        """ Finds the next power of two size for the given integer. """
        p2x=max(1,log(num,2))
        notP2X=modf(p2x)[0]>0
        return 2**int(notP2X+p2x)
   
    def setFrame(self, frame=0):
        """ Sets the current sprite to the given frame """
        self.frameInterrupt = True # A flag to tell the animation task to shut it up ur face
        self.currentFrame = frame
        self.flipTexture()
   
    def playAnim(self, animName, loop=False):
        """ Sets the sprite to animate the given named animation. Booleon to loop animation"""
        if hasattr(self, "task"):
            #if not self.task.isRemoved():
            taskMgr.remove(self.task)
        self.frameInterrupt = False # Clear any previous interrupt flags
        self.loopAnim = loop
        self.currentAnim = self.animations[animName]
        self.currentAnim.playhead = 0
        self.task = taskMgr.doMethodLater(1.0/self.currentAnim.fps,self.animPlayer, "Animate sprite")
   
    def createAnim(self, animName, frames, fps=12):
        """ Create a named animation. Takes the animation name and a tuple of frame numbers """
        self.animations[animName] = Sprite2d.Animation(frames, fps)
        return self.animations[animName]
   
    def flipX(self, val=None):
        """ Flip the sprite on X. If no value given, it will invert the current flipping."""
        if val:
            self.flip['x'] = val
        else:
            if self.flip['x']:
                self.flip['x'] = False
            else:
                self.flip['x'] = True
        self.flipTexture()
        return self.flip['x']
       
    def flipY(self, val=None):
        """ See flipX """
        if val:
            self.flip['y'] = val
        else:
            if self.flip['y']:
                self.flip['y'] = False
            else:
                self.flip['y'] = True
        self.flipTexture()
        return self.flip['y']

    def flipTexture(self):
        """ Sets the texture coordinates of the texture to the current frame"""
        sU = self.offsetX * self.repeatX
        sV = self.offsetY * self.repeatY
        oU = 0 + self.frames[self.currentFrame].col * self.uSize
        oV = 1 - self.frames[self.currentFrame].row * self.vSize - self.offsetY
        if self.flip['x']:
            sU *= -1
            oU = self.uSize + self.frames[self.currentFrame].col * self.uSize
        if self.flip['y']:
            sV *= -1
            oV = 1 - self.frames[self.currentFrame].row * self.vSize
        self.node.setTexScale(TextureStage.getDefault(), sU, sV)
        self.node.setTexOffset(TextureStage.getDefault(), oU, oV)
   
    def clear(self):
        """ Free up the texture memory being used """
        self.texture.clear()
        self.paddedImg.clear()
        self.node.removeNode()
   
    def animPlayer(self, task):
        if self.frameInterrupt:
            return task.done
        #print "Playing",self.currentAnim.cells[self.currentAnim.playhead]
        self.currentFrame = self.currentAnim.cells[self.currentAnim.playhead]
        self.flipTexture()
        if self.currentAnim.playhead+1 < len(self.currentAnim.cells):
            self.currentAnim.playhead += 1
            return task.again
        if self.loopAnim:
            self.currentAnim.playhead = 0
            return task.again
