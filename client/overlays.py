from pandac.PandaModules import *

class GeomMaker(object):
    """
    A utility to create complex and editable 'card' geometry. Multiple 'cards' 
    can be written to a single geometry node, texcoords and vertices can be 
    re-written, and line borders can be created and edited. This class is used
    to create and resize overlay geometry.    
    """
    DEFAULT = 'default'
    LINES = 'lines'
    TEXTURE = 'texture'
    
    def startGeom(self, mode=DEFAULT, texture=None, 
                  writer=None, hasColor=False):
        """ 
        Prepares the geom maker. The mode can be one of DEFAULT (for generating or
        editing cards), TEXTURE (for editing texcoords) or LINES (for generating or
        editing lines). Specify a ``writer`` to edit its geometry, otherwise a new 
        geometry will be created. 
        
        If ``hasColor`` is ``False``, the geometry will be written without any colour
        data.
        """
        self.mode = mode
        self.texture = texture
        self.writer = writer
        self.hasColor = hasColor
        self.n = 0
        if self.writer is None:
            lines = mode == GeomMaker.LINES
            format = GeomVertexFormat.getV3c4t2() if hasColor else GeomVertexFormat.getV3t2()
            self.vdata = GeomVertexData('quad', format, Geom.UHStatic)
            self.vertex = GeomVertexWriter(self.vdata, 'vertex')
            self.pigment = None if not hasColor else GeomVertexWriter(self.vdata, 'color')
            self.uv = GeomVertexWriter(self.vdata, 'texcoord') if not lines else None
            self.prim = GeomTriangles(Geom.UHStatic) if not lines else GeomLines(Geom.UHStatic)
        
    def next(self, x, y, xs, ys, uvdata=None, color=None):
        """
        Adds a sub-card (a quad) to the current geometry. The positions are
        screen coordinates; however, it's highly recommended that the initial (X, Y)
        positions (i.e. that of the top left card in the geometry) should be at (0, 0).
        That way, node.setPos can be used for easy and efficient repositioning of the
        geometry.

        Once all sub-cards have been created, use :func:``endGeom`` to create the node.
        
        .. note::
            When in LINES mode, ``(x, y)`` is the start point and ``(xs, ys)``
            is the end point.
        """
        
        generating = self.writer is None
        
        #don't do any of this if we're working with texcoords only
        if self.mode != GeomMaker.TEXTURE:
            z = 0
            #first draw the vertex positions
            vertex = self.writer or self.vertex
            if self.mode == GeomMaker.LINES:
                vertex.addData3f(Vec3(x, z, y))
                vertex.addData3f(Vec3(xs, z, ys))
            else:
                vertex.addData3f(Vec3(x, z, y))
                vertex.addData3f(Vec3(x+xs, z, y))
                vertex.addData3f(Vec3(x+xs, z, y+ys))
                vertex.addData3f(Vec3(x, z, y+ys))
            #if we are generating for the first time,
            #draw the colour if needed
            if generating:
                if self.hasColor and color is None:
                    color = Vec4(1,1,1,1)
                if self.hasColor:
                    self.pigment.addData4f(color)
                    self.pigment.addData4f(color)
                    if self.mode != GeomMaker.LINES:
                        self.pigment.addData4f(color)
                        self.pigment.addData4f(color)
        
        #if we are generating/editing texcoords...
        if (generating and self.uv is not None) or self.mode == GeomMaker.TEXTURE:
            uvw = self.writer or self.uv
            u, v, us, vs = 0, -0, 1, -1
            if uvdata is not None and self.texture is not None:
                #1,1  0,1  0,0  1,0
                tx = float(self.texture.getXSize())
                ty = float(self.texture.getYSize())
                u, v, us, vs = uvdata
                u, v, us, vs = (u)/tx, 1-(v)/ty, (us+1)/tx, 1-(vs+1)/ty
            uvw.addData2f(u,v)
            uvw.addData2f(us,v)
            uvw.addData2f(us,vs)
            uvw.addData2f(u,vs)
        
        if generating:
            if self.mode == GeomMaker.LINES:
                self.prim.addVertices(self.n, self.n+1)
                self.prim.closePrimitive()
                self.n += 2
            else:
                self.prim.addVertices(self.n, self.n+1, self.n+2)
                self.prim.addVertices(self.n+2, self.n+3, self.n)
                self.prim.closePrimitive()
                self.n += 4
            
    def endGeom(self, nodeName):
        """
        Finishes creating the geometry and returns a node.
        """
        if self.writer is not None:
            #if we were just editing...
            return None
        else:
            geom = Geom(self.vdata)
            geom.addPrimitive(self.prim)
            
            node = GeomNode("gui_geom")
            node.addGeom(geom)
            
            nodepath = NodePath(nodeName)
            nodepath.attachNewNode(node)
            if self.texture is not None:
                nodepath.setTexture(self.texture)
            nodepath.setTransparency(True)
            nodepath.setDepthWrite(False)
            nodepath.setDepthTest(False)
            nodepath.setTwoSided(True)
            nodepath.setAttrib(LightAttrib.makeAllOff())
            nodepath.setBin('fixed', 0)
            
            #clear some vars
            self.uv = None
            self.vertex = None
            self.pigment = None
            self.vdata = None
            
            return nodepath

class OverlayContainer(object):
    """ 
    The base class for all overlays, but can also act as a container
    for other overlays (i.e. a panel).
    
    If an overlay name is not specified, it will be generated using
    the class name and a unique identifier, such as::
        
        OverlayContainer241222
    
    You can create your own overlays by extending ``OverlayContainer``
    and passing ``noNode`` as ``True`` (which allows you to create the node).
    After you call this constructor, you can use ``self.name`` to retrieve
    the potentially generated name.
    """
    def __init__(self, name=None, noNode=False, flip=False):
    
        if name is None:
            name = '%s%i' % (self.__class__.__name__, id(self))
        self.name = name
        self.node = None if noNode else NodePath(self.name)
        self.x, self.y = 0, 0
        self.zIndex = 0
        self.xScale, self.yScale = 1, 1
        self.flip = flip
        self.yMult = -1 if flip else 1
        if self.node is not None:
            self.node.setScale(self.xScale, 1, self.yScale*self.yMult)
            self.node.setBin('fixed', self.zIndex)
    
    def setZIndex(self, zIndex):
        """ Sets the z-Index (depth) of this overlay. Higher numbers brings an
        item closer to the front.
        
        .. note:: 
            This will have no effect on an OverlayContainer. Under the hood, this 
            simply calls ``setBin('fixed', zIndex)`` on the node. 
        """
        self.zIndex = zIndex
        if self.node is not None:
            self.node.setBin('fixed', zIndex)
    
    def getZIndex(self):
        """ Returns the z-Index (depth) of this overlay. """
        return self.zIndex

    def destroy(self):
        """ Destroys this overlay and removes its node. Any further calls to setPos
        or other node-related methods will raise exceptions. """
        if self.node is not None:
            self.node.removeNode()
            self.node = None
    
    def setPos(self, x, y):
        """
        Sets the position of this overlay in pixels, where (0, 0) 
        is the upper left.
        
        .. note:: 
            Under the hood, this simply calls ``setPos(x, 0, y)`` on the 
            node. Reparenting this to :class:`PixelNode`
            allows us to set its position in screen-space coordinates.
        """
        self.x = x
        self.y = y
        if self.node is not None: 
            self.node.setPos(x, 0, y)
    
    def getPos(self):
        """ Returns the position of this overlay as a tuple of ``(x, y)``,
        in pixels. """
        return self.x, self.y
    
    def reparentTo(self, parent):
        """ Moves this overlay under the given parent node or overlay. """
        if self.node is not None:
            if isinstance(parent, OverlayContainer): 
                self.node.reparentTo(parent.node)
            else:
                self.node.reparentTo(parent)
    
    def setScale(self, xScale, yScale):
        """
        Applies the given scale to the overlay, where (1, 1) is 100% x 
        and y scale (default).
        """
        self.xScale = xScale
        self.yScale = yScale
        self.node.setScale(xScale, 1, yScale*self.yMult)
    
    def getScale(self):
        """ Returns the scale of the overlay. """
        return self.xScale, self.yScale
    
class PixelNode(NodePath, OverlayContainer):
    """
    PixelNode is the root node for all overlays (and 2D elements in general). 
    Overlays should be reparented to this node.

    If ``name`` is not specified, one will be generated. If ``parent`` is not
    specified, Panda's ``render2d`` node will be used.

    .. note::
        Under the hood, PixelNode is a NodePath that is positioned in the upper
        left corner (-1, 0, 1) and scaled to enable pixel positioning (its size
        is 2.0/windowXSize by -2.0/windowYSize). 
    """
    
    def __init__(self, name=None, parent=None):
        OverlayContainer.__init__(self, name)
        NodePath.__init__(self, self.name)
        if parent is None:
            parent = render2d
        self.node = self
        self.reparentTo(parent)
        self.setPos(-1,0,1) #the upper left corner
        self.aspectRatioChanged()

    def aspectRatioChanged(self, winX=None, winY=None):
        """
        Called to notify the node that the aspect ratio has been changed. This
        is generally used like so::
            base.accept('aspectRatioChanged', pixelNode.aspectRatioChanged)
        
        Alternatively, you can not use base.accept and instead handle aspect ratio
        changes manually (i.e. if you know when it will change). You can pass a
        ``winX`` and ``winY`` to resize the overlays to fit a different resolution. 
        """
        if winX is None:
            winX = base.win.getXSize()
        if winY is None:
            winY = base.win.getYSize()
        self.setScale(2.0/winX, 1, -2.0/winY)
            
class Overlay(OverlayContainer):
    """
    Creates a geometry overlay with the given options. If ``texcoords`` or 
    ``atlas`` is not specified, the geometry's vertices will not be 
    generated with UV data from 0 to 1, so that the texture fills to 
    the overlay size.
    
    As with other overlays, if ``name`` is not specified, it will be generated.
    The ``size`` of the overlay can be included at creation to avoid the need to 
    re-write the vertices later. If ``color`` is specified, it will be set on the
    resulting NodePath. 
    
    The ``texcoords`` parameter is a tuple of texture coordinates given in pixels,
    see the tutorials for further details.
    """
        
    geomMaker = GeomMaker()
        
    def __init__(self, name=None, size=(0, 0), texture=None, 
                 texcoords=None, color=None):
        OverlayContainer.__init__(self, name)
        self.border = None
        self.borderPadding = 0
        self.texture = texture
        self.texcoords = texcoords
        self.width, self.height = size  
        self.node = self.draw(self.width, self.height, texcoords)
        self.geom = self.node.getChildren()[0]
        if color is not None:
            self.node.setColor(color)
    
    def draw(self, width, height, texcoords=None, 
              mode=GeomMaker.DEFAULT, writer=None):
        Overlay.geomMaker.startGeom(mode=mode, hasColor=False, 
                                    texture=self.texture, writer=writer)
        Overlay.geomMaker.next(0, 0, width, height, texcoords)
        return Overlay.geomMaker.endGeom(self.name)
    
    def setBorder(self, border, padding=0):
        """ Helper method to quickly set a 'border' overlay which is 
        resized, rescaled and repositioned whenever this overlay is changed. 
        
        The ``padding`` can be specified to add spacing between. You can also
        use a negative padding. 
        
        Borders are generally not supported by ``OverlayContainers``, but by
        classes which inherit from it. """
        self.border = border
        self.borderPadding = padding
        if self.border is not None:
            self.updateBorder()
    
    def updateBorder(self):
        self.border.setPos(-self.borderPadding, -self.borderPadding)
        xs, ys = self.getScale()
        self.border.setScale(xs, ys)
        w, h = self.getSize()
        self.border.setSize(w+self.borderPadding*2, h+self.borderPadding*2)
    
    def setTexcoords(self, x1, y1, x2, y2):
        """ Adjusts the texcoords (in pixels) for this geometry by 
        modifying the vertex data. """
        self.texcoords = x1, y1, x2, y2
        vdata = self.geom.node().modifyGeom(0).modifyVertexData()
        writer = GeomVertexWriter(vdata, 'texcoord')
        writer.setRow(0)
        self.draw(self.width, self.height, mode=GeomMaker.TEXTURE, 
                  texcoords=self.texcoords, writer=writer)
    
    def getTexcoords(self):
        return self.texcoords
    
    def setSize(self, width, height):
        """ Sets the size of this overlay in pixels. """ 
        if self.width != width or self.height != height:
            vdata = self.geom.node().modifyGeom(0).modifyVertexData()
            writer = GeomVertexWriter(vdata, 'vertex')
            writer.setRow(0)
            self.width = width
            self.height = height
            self.draw(width, height, writer=writer)
        if self.border is not None:
            self.updateBorder()
        
    def getSize(self):
        """ Returns the size of this overlay in pixels, as a tuple of width, height. """
        return self.width, self.height
    
    def setPos(self, x, y):
        OverlayContainer.setPos(self, x, y)
        if self.border is not None:
            self.updateBorder()
    
    def setScale(self, xScale, yScale):
        OverlayContainer.setScale(self, xScale, yScale)
        if self.border is not None:
            self.updateBorder()
    
class OverlaySlice3(Overlay):
    """
    Creates a sliced overlay with the given options, for scaling
    along one axis without quality loss.
    
    Sliced overlays are a single geometry with multiple parts. 3-sliced
    geometries use 3 parts: the center and its two edges. This overlay is useful
    for elements such as scrollbars and sliders.
     
    The ``texcoords`` argument is a tuple of the upper-left and lower-right pixels
    to slice. The default width/height of the ``edges`` is 5, and it's assumed
    that there are no gaps between parts. The actual texture coordinates of each
    part will be determined based on the given ``edges`` and ``texcoords`` values, and
    whether or not the result should be ``horizontal``.
    """
    
    def __init__(self, name=None, size=(0, 0), texture=None, 
                 edges=5, texcoords=None, horizontal=True,
                 color1=Vec4(1, 1, 1, 1), color2=Vec4(.75, .75, .75, 1)):
        self.edges = edges
        self.horizontal = horizontal
        self.color1 = color1
        self.color2 = color2
        Overlay.__init__(self, name, size, texture, texcoords)
    
    def draw(self, width, height, texcoords=None, 
              mode=GeomMaker.DEFAULT, writer=None):
        uv1, uv2, uv3 = None, None, None
        hasTex = texcoords is not None and self.texture is not None
        if hasTex:
            x1, y1, x2, y2 = texcoords
            #TODO: support tuple of edgess for greater flexibility
            if self.horizontal:
                uv1 = (x1, y1, x1+self.edges-1, y2)
                uv2 = (x1+self.edges, y1, x2-self.edges, y2)
                uv3 = (x2-self.edges+1, y1, x2, y2)
            else:
                uv1 = (x1, y1, x2, y1+self.edges-1)
                uv2 = (x1, y1+self.edges, x2, y2-self.edges)
                uv3 = (x1, y2-self.edges+1, x2, y2)
        #helpful for debugging
        colr1 = None if hasTex else self.color1
        colr2 = None if hasTex else self.color2 
        
        geom = Overlay.geomMaker
        geom.startGeom(mode=mode, hasColor=not hasTex, 
                       texture=self.texture, writer=writer)
        if self.horizontal:
            geom.next(0, 0, self.edges, height, uv1, colr1)
            geom.next(self.edges, 0, width-self.edges*2, height, 
                      uv2, colr2)
            geom.next(width-self.edges, 0, self.edges, height, 
                      uv3, colr1)
        else:
            geom.next(0, 0, width, self.edges, uv1, colr1)
            geom.next(0, self.edges, width, height-self.edges*2, 
                      uv2, colr2)
            geom.next(0, height-self.edges, width, self.edges, 
                      uv3, colr1)
        return geom.endGeom(self.name)
    
class OverlaySlice9(Overlay):
    """
    Creates a sliced overlay with the given options, for scaling
    along X and Y axis without quality loss.
    
    Sliced overlays are a single geometry with multiple parts. 9-sliced
    geometries use 9 parts: four corners, the center and the surrounding edges. 
    This overlay is useful for elements such as dialogs, buttons and decorated panels.
     
    The ``texcoords`` argument is a tuple of the upper-left and lower-right pixels
    to slice. The default size of each edge is 5, and it's assumed
    that there are no gaps between parts. The actual texture coordinates of each
    part will be determined based on the given ``edges`` and ``texcoords`` values.
    
    Unlike 3-sliced overlays, 9-slicing uses more flexible ``edges`` to support
    different sizes. It expects a tuple of ``(top, left, bottom, right)`` edges,
    or a single number to use for all edges.
    """
    
    def __init__(self, name=None, size=(0, 0), texture=None, 
                 edges=5, texcoords=None,
                 color1=Vec4(1, 1, 1, 1), 
                 color2=Vec4(.75, .75, .75, 1)):
        self.color1 = color1
        self.color2 = color2
        if not isinstance(edges, tuple):
            edges = edges, edges, edges, edges
        self.top, self.left, self.bottom, self.right = edges
        Overlay.__init__(self, name, size, texture, texcoords)
    
    def draw(self, width, height, texcoords=None, 
              mode=GeomMaker.DEFAULT, writer=None):
        uvtl, uvtop, uvtr = None, None, None
        uvleft, uvcenter, uvright = None, None, None
        uvbl, uvbottom, uvbr = None, None, None
        
        hasTex = texcoords is not None and self.texture is not None
        if hasTex:
            x1, y1, x2, y2 = texcoords
            uvtl = (x1, y1, x1+self.left-1, y1+self.top-1)
            uvtop = (x1+self.left, y1, x2-self.right, y1+self.top-1)
            uvtr = (x2-self.right+1, y1, x2, y1+self.top-1)
            
            uvleft = (x1, y1+self.top, x1+self.left-1, y2-self.bottom-1)
            uvcenter = (x1+self.left, y1+self.top, x2-self.right, y2-self.bottom-1)
            uvright = (x2-self.right+1, y1+self.top, x2, y2-self.bottom-1)
            
            uvbl = (x1, y2-self.bottom, x1+self.left-1, y2)
            uvbottom = (x1+self.left, y2-self.bottom, x2-self.right, y2)
            uvbr = (x2-self.right+1, y2-self.bottom+1, x2, y2)
        
        #helpful for debugging
        colr1 = None if hasTex else self.color1
        colr2 = None if hasTex else self.color2 
        
        w, h = width, height
        
        geom = Overlay.geomMaker
        geom.startGeom(mode=mode, hasColor=not hasTex, 
                       texture=self.texture, writer=writer)
        #top
        geom.next(self.left, 0, w-self.left-self.right, self.top, uvtop, 
                  colr2)
        geom.next(0, 0, self.left, self.top, uvtl, colr1)
        geom.next(w-self.right, 0, self.right, self.top, uvtr,
                   colr1)
        #mid
        midh = h-self.bottom-self.top
        geom.next(0, self.top, self.left, midh, uvleft, colr2)
        geom.next(self.left, self.top, w-self.left-self.right, midh, uvcenter, 
                  colr1)
        geom.next(w-self.right, self.top, self.right, midh, uvright, 
                  colr2)
        #bottom
        by = h-self.bottom
        geom.next(0, by, self.left, self.bottom, uvbl, colr1)
        geom.next(self.left, by, w-self.left-self.right, self.bottom, 
                  uvbottom, colr2)
        geom.next(w-self.right, by, self.right, self.bottom, uvbr, 
                  colr1)
        return geom.endGeom(self.name)

class LineBorder(Overlay):
    """
    A rectangle drawn with the given colour, to make a line border.
    """
    
    def __init__(self, name=None, size=(0, 0), color=Vec4(0, 0, 0, 1)):
        Overlay.__init__(self, name, size, color=color)
        
    def draw(self, w, h, texcoords=None, mode=GeomMaker.LINES, writer=None):
        geom = Overlay.geomMaker
        geom.startGeom(mode=mode, hasColor=False, writer=writer)
        w -= 1
        geom.next(0, 1, w+1, 1)
        geom.next(w, 1, w, h)
        geom.next(w, h, 0, h)
        geom.next(0, 0, 0, h)            
        return geom.endGeom(self.name)

class TextOverlay(OverlayContainer):
    """ 
    TextOverlay provides a simple manner of displaying crisp text as an overlay.
    Each text overlay contains ``node``, a NodePath generated from the TextNode. 
    
    Overlays use pixelsPerUnit and scaling to generate crisp text. For the best 
    results, you should set the overlay's text size (i.e. text scale) to match 
    the pixelsPerUnit of your font. You can use :const:`AUTO_SIZE` (the default
    text size) to scale the generated text to its pixels per unit -- or 30 if the
    font is not dynamic. Manually setting the size with :func:`setTextSize` 
    is more useful for static fonts, or when you wish to scale the font 
    regardless of its pixels per unit. 
    
    A font height of 1.0 is a Panda standard, and using different values 
    (such as using font.setPointSize, which adjusts the height internally) may
    create undesired results with TextOverlay.
        
    If no ``textNode`` is specified, one will be created. Likewise, if ``font`` is not 
    specified, the ``defaultFont`` will be used if it has been set, otherwise 
    ``textNode``'s default font will be used. The ``color`` is the color for the text
    node, as is ``align`` and ``wordwrap``.
    
    .. note::
        Wordwrap is given in pixels, and it is assumed to be the desired width
        of the overlay. Using :func:`getSize` with wordwrapping will return the
        wordwrapping, not the frame of the text.
        
    The ``lineHeight`` of a font is initially trimmed, as to remove the extra space 
    above most fonts. Set ``trimHeight`` to ``False`` if you're having problems
    with text y-offset.
    """
    
    @staticmethod
    def loadFont(ref, size=15, spaceAdvance=None, 
                 lineHeight=None, scaleFactor=1, 
                 textureMargin=2, minFilter=Texture.FTNearest,
                 magFilter=Texture.FTNearest, 
                 renderMode=None):
        """ 
        This function simply calls loadFont with the above parameters -- it is included
        for convenience. 
        
        Note that ``size`` is actually the pixelsPerUnit (for dynamic fonts). See 
        main description for details.
        """
        return loader.loadFont(ref, spaceAdvance=spaceAdvance,
                                    lineHeight=lineHeight, 
                                    pixelsPerUnit=size,
                                    scaleFactor=scaleFactor,
                                    textureMargin=textureMargin,
                                    minFilter=minFilter, magFilter=magFilter)
        
    @staticmethod
    def setFontSize(font, size):
        """
        A convenience function to set the pixelsPerUnit of a dynamic font, if 
        necessary. This function will do nothing if the font is static.
        
        .. note:: 
            This method uses ``Font.clear()`` which wastes memory in Panda 1.6.2
            and early; use it scarcely or not at all. Newer versions of Panda should
            include an easy way to copy fonts for caching, as well as a fix to ensure
            that no associations to the old font pages stay around. 
        """
        if isinstance(font, DynamicTextFont):
            ppu = font.getPixelsPerUnit()
            if ppu != size:
                font.clear()
                font.setPixelsPerUnit(size)
    
    defaultFont = None
    """ Newly created TextOverlays will use this if no font is specified. """
    
    AUTO_SIZE = 'auto'
    """ The text overlay will attempt to set the text size to the pixelsPerUnit
    of the current font. If the current font is not dynamic, it will set
    the text size to 30 (which is the default from egg-mkfont).
    """
    
    def __init__(self, name=None, msg=None, textSize=AUTO_SIZE,
                 textNode=None, font=None, color=Vec4(0, 0, 0, 1), 
                 align=TextNode.ALeft, wordwrap=None, trimHeight=True):
        OverlayContainer.__init__(self, name, noNode=True, flip=True)
                
        tnn = '%s_text' % self.name
        self.textNode = textNode or TextNode(tnn)
        self.textNode.setName(tnn)
        
        self.trimHeight = trimHeight
        self.wordwrap = None
        
        font = TextOverlay.defaultFont if font is None else font
        if font is not None:
            self.textNode.setFont(font)
        if msg is not None:
            self.textNode.setText(msg)
        self.textNode.setAlign(align)
        self.textNode.setTextColor(color)
        self.node = NodePath(self.textNode)
        self.node.setDepthWrite(False)
        self.node.setDepthTest(False)
        self.node.setTwoSided(True)
        self.node.setAttrib(LightAttrib.makeAllOff())
        self.node.setBin('fixed', self.getZIndex())
        self.updateTexOffset()
        self.setTextSize(textSize)
        if wordwrap is not None:
            self.setWordwrap(wordwrap)
    
    def updateTexOffset(self):
        """ 
        Forces the text to update its texture offsets; this fixes a bug in
        Panda 1.6.2.
        """
        f = self.textNode.getFont()
        if isinstance(f, DynamicTextFont):
            tw = f.getPageXSize()
            th = f.getPageYSize()
            self.node.clearTexTransform()
            self.node.setTexOffset(TextureStage.getDefault(), 0.4/tw, -0.4/th)
    
    def setText(self, msg):
        """
        Sets the text and repositions the node according to its new height.
        """
        self.textNode.setText(msg)
        self.textChanged()
    
    def getText(self):
        """ Calls ``textNode.getText()``. """
        return self.textNode.getText()
    
    def setFont(self, font):
        """ Sets a new font for this overlay, updates this overlay's scale, 
        updates the node position, and updates the texture offsets. """
        self.textNode.setFont(font)
        scale = float(self.getTextSize())
        self.setScale(scale, scale)
        self.textChanged()
        self.updateTexOffset()
    
    def getFont(self):
        """ Calls ``textNode.getFont()``. """
        return self.textNode.getFont()
        
    def textChanged(self):
        """ The text has changed -- reposition it for the parent overlay. """
        x, y = self.getPos()
        self.setPos(x, y)
        
    def setWordwrap(self, wordwrap):
        """ Sets the wordwrap, in pixels. """
        self.wordwrap = wordwrap
        if wordwrap is None:
            self.textNode.clearWordwrap()
        else: 
            self.textNode.setWordwrap(wordwrap / float(self.xScale))
        self.textChanged()
            
    def getWordwrap(self):
        """ Returns the wordwrap, in pixels. """
        return self.wordwrap
    
    def setAlign(self, align):
        self.textNode.setAlign(align)
        self.textChanged()
    
    def getAlign(self):
        return self.textNode.getAlign()
    
    def setTextSize(self, size):
        """ 
        Sets the scale of the text node and repositions it vertically to 
        fit the new size.
        
        If size is :const:`AUTO_SIZE`, it will attempt to resize the text
        to the current font's pixels per units (or default to size 30 
        for static fonts).
        """
        self.textSize = size
        
        scale = float(self.getTextSize()) #gets the scale
        self.setScale(scale, scale)
        self.textChanged()
            
    def getTextSize(self):
        """ Returns the text size, or attempts to find it if
        :func:`isAutoSize` returns ``True``. """
        if self.isAutoSize():
            f = self.textNode.getFont()
            if isinstance(f, DynamicTextFont):
                return f.getPixelsPerUnit()
            else:
                return 30
        else:
            return self.textSize
        
    def isAutoSize(self):
        """ Returns ``True`` if :data:`AUTO_SIZE` is on. """
        return self.textSize == TextOverlay.AUTO_SIZE
        
    def setPos(self, x, y):
        """ 
        Sets the position of the text.
        
        .. note::
            The actual node position is different from the x, y values
            used with ``setPos`` and ``getPos``. Based on the height, y-offset
            and x-alignment, the text is positioned so that ``setPos(0, 0)``
            will place it nicely in the upper left corner.
        """
        xoff = round(self.getAlignOffset())
        yoff = 0
        if self.trimHeight:
            yoff = self.lineHeightExtra()
        yoff = round(self.textNode.getTop() * self.yScale - yoff)
        OverlayContainer.setPos(self, x+xoff, y+yoff)
        self.x = x
        self.y = y
    
    def getAlignOffset(self):
        """ Returns the amount to offset the text's x-position due to 
        its alignment. """
        if self.textNode.hasAlign():
            a = self.textNode.getAlign()
            if a == TextNode.ACenter:
                return self.getSize()[0] / 2.0
            elif a == TextNode.ARight:
                return self.getSize()[0]
            else:
                return 0
    
    def lineHeightExtra(self):
        """ Returns the line height minus 1.0 (standard Panda text height) in pixels. """
        f = self.textNode.getFont()
        return (f.getLineHeight() - 1.0) * self.yScale
    
    def destroy(self):
        """ Destroys this overlay. """
        self.textNode = None
        OverlayContainer.destroy(self)
    
    def setSize(self, width, height):
        """ Deprecated; does nothing. """
        pass
    
    def getSize(self):
        """ Returns the size of the text node, in pixels. If
        word-wrapping is set on the textGen, it will be assumed to be the
        desired width.        
        
        Note that no setSize function exists -- use 
        setScale() if you wish to scale the overlay, setTextScale() to set
        point size, or use word-wrapping to set the text box width in pixels 
        (and the height will be computed accordingly). """
        if self.getText() == '':
            return 0, 0
        xs, ys = self.xScale, self.yScale
        ppu = self.getTextSize()
        h = self.textNode.getHeight() * ys
        if self.textNode.hasWordwrap():
            w = self.textNode.getWordwrap() * xs
        else:
            w = self.textNode.getWidth() * xs
        yoff = self.lineHeightExtra()
        #HACK: add a little for the bottom bit (below baseline) so that
        #the font won't spill out of the returned height
        # For now we will use the 'extra line height', which seems to work
        #well, but if the user requested trimHeight be turned off, then we
        #can simply ignore this
        if not self.trimHeight:
            yoff = 0
        return round(w), round(h-yoff)