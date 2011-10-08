from Config import *
from pandac.PandaModules import PandaNode,NodePath,Camera,TextNode,GeomTristrips,Geom,GeomVertexFormat,GeomVertexData,GeomVertexWriter,GeomNode,TransformState,OrthographicLens,TextureStage,TexGenAttrib,PNMImage,Texture,ColorBlendAttrib,CardMaker,TransparencyAttrib
from direct.interval.IntervalGlobal import *
import xml.etree.cElementTree as etree
import math

def transparencyKey(filename):
    image = PNMImage(GAME+'/textures/effects/'+filename)
    image.addAlpha()
    backgroundColor = None
    for y in range(image.getYSize()):
        for x in range(image.getXSize()):
            if backgroundColor == None:
                backgroundColor = Color(image.getRedVal(x, y), image.getGreenVal(x, y), image.getGreenVal(x, y), 0)
            if image.getRedVal(x, y) == backgroundColor.R and \
                image.getGreenVal(x, y) == backgroundColor.G and \
                image.getGreenVal(x, y) == backgroundColor.B:
                # Transparent
                image.setAlpha(x, y, 0.0)
            else:
                # Opaque
                image.setAlpha(x, y, 1.0) 
    return image

class Point:
    X = 0
    Y = 0
    Z = 0
    def __init__(self, x, y, z):
        self.X = x
        self.Y = y
        self.Z = z

class Line:
    Start = Point(0,0,0)
    End = Point(0,0,0)
    distanceLeadingUpToLine = 0
    distance = 0
    def __init__(self, start, end, distanceLeadingUpToLine):
        self.Start = start
        self.End = end
        self.distanceLeadingUpToLine = distanceLeadingUpToLine
        self.distance = ((self.End.X-self.Start.X)**2 + (self.End.Y-self.Start.Y)**2)**(1/2)
    def Distance(self, distanceOnLine):
        angleOfLineInRadians = atan2(self.End.Y - self.Start.Y, self.End.X - self.Start.X)
        return Point(self.Start.X + (distanceOnLine * cos(angleOfLineInRadians)), self.Start.Y + (distanceOnLine * sin(angleOfLineInRadians)))

class Tween:
    lineSegments = []
    colorList = []
    frameLength = 0
    advancementFunction = "linear"
    def __init__(self, frameLength, advancementFunction, points, colors):
        if points != None and points != []:
            if len(points) > 1:
                runningDistanceTotal = 0
                for i in range(1, len(points), 1):
                    line = Line(points[i - 1], points[i], runningDistanceTotal);
                    self.lineSegments.append(line)
                    runningDistanceTotal = runningDistanceTotal + line.distance
                    pass
                pass
            pass
        self.colorList = colors
        self.frameLength = frameLength
        self.advancementFunction = advancementFunction

    def hasColorComponent(self):
        if len(self.colorList) > 0:
            return True
        return False

    def colorFromFrame(self, frame):
        if frame < 1:
            return Color(1,1,1,1)
        elif frame == 1 or len(self.colorList) == 1:
            return self.colorList[0]
        elif frame >= self.frameLength:
            return self.colorList[len(colorList)-1]
        else:
            zeroToOneIndex = float(frame) / float(self.frameLength)
            startIndex = 0
            endIndex = 0
            zeroToOneStartIndex = 0
            zeroToOneEndIndex = 1.0
            for i in range(0, len(self.colorList)-1, 1):
                thisZeroToOneIndex = float(i+1) / float(len(self.colorList))
                if thisZeroToOneIndex == zeroToOneIndex:
                    startIndex = i
                    endIndex = i
                    zeroToOneStartIndex = zeroToOneIndex
                    zeroToOneEndIndex = zeroToOneIndex
                elif thisZeroToOneIndex >= zeroToOneIndex:
                    endIndex = i;
                    zeroToOneEndIndex = thisZeroToOneIndex
                    break # Exit after finding suitable data
                else:
                    startIndex = i
                    zeroToOneStartIndex = thisZeroToOneIndex
            if len(self.colorList) > 0 and float(zeroToOneEndIndex - zeroToOneStartIndex) > 0:
                transitionPercent = float(zeroToOneIndex - zeroToOneStartIndex) / float(zeroToOneEndIndex - zeroToOneStartIndex)
                return Color((1-transitionPercent) * self.colorList[startIndex].R + transitionPercent * self.colorList[endIndex].R, (1-transitionPercent) * self.colorList[startIndex].G + transitionPercent * self.colorList[endIndex].G, (1-transitionPercent) * self.colorList[startIndex].B + transitionPercent * self.colorList[endIndex].B, (1-transitionPercent) * self.colorList[startIndex].A + transitionPercent * self.colorList[endIndex].A)
            else:
                return Color(1,1,1,1)
    def lengthOfLineSegments(self):
        if len(self.lineSegments) > 0:
            return self.lineSegments[len(self.lineSegments)-1].distanceLeadingUpToLine + self.lineSegments[len(self.lineSegments)-1].distance;
        else:
            return 0
    def XYFromFrame(self, frame):
        if frame < 1:
            return Point(0, 0, 0)
        else:
            fullLength = self.lengthOfLineSegments()
            distance = float(frame-1)*fullLength/float(self.frameLength)
            if frame <= self.frameLength:
                lineThatContainsPoint = None
                for i in range(0, len(self.lineSegments)-1, 1):
                    if self.lineSegments[i].distanceLeadingUpToLine <= distance and (self.lineSegments[i].distanceLeadingUpToLine + self.lineSegments[i].distance) >= distance:
                        lineThatContainsPoints = self.lineSegments[i]
                        break
                if lineThatContainsPoint != None:
                    return lineThatContainsPoint.Distance(distance - lineThatContainsPoint.distanceLeadingUpToLine)
                else:
                    return Point(0,0,0)
            else:
                if len(self.lineSegments)>0:
                    return self.lineSegments[len(self.lineSegments)-1].End
                else:
                    return Point(0,0,0)

class Bound:
    X = 0
    Y = 0
    Width = 0
    Height = 0
    def __init__(self, x, y, width, height):
        self.X = x
        self.Y = y
        self.Width = width
        self.Height = height

class Color:
    R = 0
    G = 0
    B = 0
    A = 1
    def __init__(self, R, G, B, A):
        self.R = R
        self.G = G
        self.B = B
        self.A = A
    def printAsString(self):
        print str(self.R)+", "+str(self.G)+", "+str(self.B)+", "+str(self.A)
class Frame:
    bound = Bound(0, 0, 0, 0)
    s = 0
    t = 0
    S = 1
    T = 1
    blendMode = "overwrite"
    scaleX = 1
    scaleY = 1
    color = Color(1,1,1,1)
    rotationZ = 0
    def __init__(self, bound, s, t, S, T, blendMode, scaleX, scaleY, color, rotationZ):
        self.bound = bound
        self.s = s
        self.t = t
        self.S = S
        self.T = T
        self.blendMode = blendMode
        self.scaleX = scaleX
        self.scaleY = scaleY
        if color != None:
            self.color = color
        else: # TODO: Find logic error in color from frame.
            self.color = Color(1,1,1,1)
        self.rotationZ = rotationZ
    def printAsString(self):
        print "["+str(self)+"]::"
        print "   Bound: ["+str(self.bound.X)+", "+str(self.bound.Y)+"; "+str(self.bound.Width)+"x"+str(self.bound.Height)+"],"
        print "   (s, t; S, T): ["+str(self.s)+", "+str(self.t)+"; "+str(self.S)+", "+str(self.T)+"]," 
        print "   Blend: '"+self.blendMode+"'," 
        print "   Scale(x, y): ["+str(self.scaleX)+", "+str(self.scaleY)+"]," 
        print "   Color(R, G, B, A): ["+str(self.color.R)+", "+str(self.color.G)+", "+str(self.color.B)+", "+str(self.color.A)+"]," 
        print "   Rotation-Z: "+str(self.rotationZ)

class Effect:
    baseWidth = 0
    baseHeight = 0
    effectWidth = 1
    effectHeight = 1
    effectTargetMS = 143
    noSampling = False
    tex = None
    loadedFormat = None
    # Animation variables
    internalFrameIndex = 1
    startIndex = 1
    endIndex = 1
    loopEffect = False
    # XML variables
    tree = None
    frames = None
    colors = None
    tweens = None
    compositeFrames = None
    # Nodes
    consumedNodesList = None
    # Accessible object (nodePath)
    effectCameraNodePath = None
    effectCardNodePath = None
    # Constant value; Unit comparison for card size; basis is from cure, which is [140x110]
    cardDimensionBasis = [-5.0, 5.0, 0.0, 10.0, 140.0, 110.0]
    pixelScaleX = cardDimensionBasis[4]/(cardDimensionBasis[1]-cardDimensionBasis[0])
    pixelScaleZ = cardDimensionBasis[5]/(cardDimensionBasis[3]-cardDimensionBasis[2])
    effectIsCentered = True
    effectAdjustment = [0, 0, 0]
    def __init__(self, effectFileName, parent=None, loop=False, effectIsCentered=True, effectAdjustment=[0, 0, 0]):
        self.effectAdjustment = effectAdjustment
        self.loopEffect = loop
        self.effectIsCentered = effectIsCentered
        self.loadedFormat = None
        if effectFileName != None:
            effectFileNameSplit = effectFileName.split('.')
            self.loadedFormat = effectFileNameSplit[len(effectFileNameSplit)-2] # Get value at penultimate index
            if self.loadedFormat == effectFileNameSplit[0]:
                self.loadedFormat = None # Get rid of bad format name.
            pass
            
        # Load texture; supply alpha channel if it doesn't exist.
        p = transparencyKey(effectFileName)
        self.tex = Texture()
        self.tex.setup2dTexture(p.getXSize(), p.getYSize(), Texture.TUnsignedByte, Texture.FRgba)
        self.tex.load(p)
        if self.loadedFormat != None:
            try:
                self.tree = etree.parse("./"+GAME+"/effects/"+self.loadedFormat+"/sprite.xml")
            except IOError:
                self.loadedFormat = None
            pass
        if self.loadedFormat != None: 
            root = self.tree.getroot()
            self.frames = root.find('.//frames')
            self.colors = root.find('.//colors')
            self.tweens = root.find('.//motion-tweens')
            self.compositeFrames = root.find('.//composite-frames')
            self.baseWidth = 0 if root.attrib.get("base-width") == None else float(root.attrib.get("base-width"))
            self.baseHeight = 0 if root.attrib.get("base-height") == None else float(root.attrib.get("base-height"))
            self.effectWidth = 1 if root.attrib.get("frame-width") == None else float(root.attrib.get("frame-width"))
            self.effectHeight = 1 if root.attrib.get("frame-height") == None else float(root.attrib.get("frame-height"))
            self.effectTargetMS = 143 if root.attrib.get("target-ms") == None else float(root.attrib.get("target-ms"))
            self.startIndex = 1 if root.attrib.get("target-start") == None else int(root.attrib.get("target-start"))
            self.endIndex = 1 if root.attrib.get("target-end") == None else int(root.attrib.get("target-end"))
            self.noSampling = False if root.attrib.get("no-sampling") == None else bool(root.attrib.get("no-sampling"))
            if self.noSampling==True:
                self.tex.setMagfilter(Texture.FTNearest)
                self.tex.setMinfilter(Texture.FTNearest)
            cm = CardMaker('card-'+effectFileName)
            cardDeltaX = self.effectWidth / self.pixelScaleX
            cardDeltaZ = self.effectHeight / self.pixelScaleZ
            if self.effectIsCentered == True:
                cm.setFrame(0, 0, 0, 0)
                deltaX = (cardDeltaX/2.0) - (-cardDeltaX/2.0)
                deltaY = 0
                deltaZ = (cardDeltaZ/2.0) - (-cardDeltaZ/2.0)
                #occluder = OccluderNode('effect-parent-occluder', Point3((-cardDeltaX/2.0), 0, (-cardDeltaZ/2.0)), Point3((-cardDeltaX/2.0), 0, (cardDeltaZ/2.0)), Point3((cardDeltaX/2.0), 0, (cardDeltaZ/2.0)), Point3((cardDeltaX/2.0), 0, (-cardDeltaZ/2.0)))
            else:
                cm.setFrame(0, 0, 0, 0)
                deltaX = (cardDeltaX/2.0) - (-cardDeltaX/2.0)
                deltaY = 0
                deltaZ = cardDeltaZ - 0
                #occluder = OccluderNode('effect-parent-occluder', Point3((-cardDeltaX/2.0), 0, 0), Point3((-cardDeltaX/2.0), 0, cardDeltaZ), Point3((cardDeltaX/2.0), 0, cardDeltaZ), Point3((cardDeltaX/2.0), 0, 0))
            self.effectCardNodePath = render.attachNewNode(cm.generate())            
            self.effectCardNodePath.setBillboardPointEye()
            self.effectCardNodePath.reparentTo(parent)
            #occluder_nodepath = self.effectCardNodePath.attachNewNode(occluder)
            #self.effectCardNodePath.setOccluder(occluder_nodepath)
            emptyNode = NodePath('effect-parent-translator')
            emptyNode.reparentTo(self.effectCardNodePath)
            if effectIsCentered == True:
                emptyNode.setPos(-deltaX/2.0+self.effectAdjustment[0], 0+self.effectAdjustment[1], deltaZ/2.0+self.effectAdjustment[2])
            else:
                emptyNode.setPos(-deltaX/2.0+self.effectAdjustment[0], 0+self.effectAdjustment[1], deltaZ+self.effectAdjustment[2])
            #emptyNode.place()
            emptyNode.setSx(float(deltaX)/self.effectWidth)
            emptyNode.setSz(float(deltaZ)/self.effectHeight)
            self.effectCameraNodePath = emptyNode                        
            if parent != None:
                self.effectCardNodePath.reparentTo(parent)
            else:
                self.effectCardNodePath.reparentTo(render)
            #self.effectCardNodePath.place()
            self.effectCardNodePath.setBin("fixed", 40)
            self.effectCardNodePath.setDepthTest(False)
            self.effectCardNodePath.setDepthWrite(False)
        pass
    def getSequence(self):
        sequence = Sequence()
        for x in range(self.startIndex, self.endIndex, 1):
            sequence.append(Func(self.pandaRender))
            sequence.append(Func(self.advanceFrame))
            sequence.append(Wait(self.effectTargetMS * 0.001))
        sequence.append(Func(self.clearNodesForDrawing))
        sequence.append(Func(self.advanceFrame))
        sequence.append(Wait(self.effectTargetMS * 0.001))
        return sequence
        pass
    def hasEffectFinished(self):
        if self.internalFrameIndex > self.endIndex and self.loopEffect == False:
            return True
        else:
            return False
        pass
    def advanceFrame(self):
        if self.internalFrameIndex < self.endIndex:
            self.internalFrameIndex += 1
        elif self.internalFrameIndex == self.endIndex and self.loopEffect == True:
            self.internalFrameIndex = self.startIndex
        else:
            self.internalFrameIndex = self.endIndex + 1
            self.clearNodesForDrawing()
        pass
    def clearNodesForDrawing(self):
        if False:
            self.effectCameraNodePath.analyze()
        if self.consumedNodesList != None and self.consumedNodesList != []:
            for consumedNode in self.consumedNodesList:
                consumedNode.removeNode()
        self.consumedNodesList = []
        pass
    def pandaRender(self):
        frameList = []
        for node in self.compositeFrames.getiterator('composite-frame'):
            if node.tag == "composite-frame" and node.attrib.get("id") == str(self.internalFrameIndex):
                for frameCallNode in node:
                    for frameNode in self.frames.getiterator('frame'):
                        if frameNode.tag == "frame" and frameNode.attrib.get("id") == frameCallNode.attrib.get("id"):
                            offsetX = 0 if frameCallNode.attrib.get("offset-x") == None else float(frameCallNode.attrib.get("offset-x"))
                            offsetY = 0 if frameCallNode.attrib.get("offset-y") == None else float(frameCallNode.attrib.get("offset-y"))
                            tweenId = frameCallNode.attrib.get("tween")
                            frameInTween = 0 if frameCallNode.attrib.get("frame-in-tween") == None else int(frameCallNode.attrib.get("frame-in-tween"))
                            addWidth = 0 if frameNode.attrib.get("w") == None else float(frameNode.attrib.get("w"))
                            addHeight = 0 if frameNode.attrib.get("h") == None else float(frameNode.attrib.get("h"))
                            sInPixels = 0 if frameNode.attrib.get("s") == None else float(frameNode.attrib.get("s"))
                            tInPixels = 0 if frameNode.attrib.get("t") == None else float(frameNode.attrib.get("t"))
                            swInPixels = sInPixels + addWidth
                            thInPixels = tInPixels + addHeight
                            s = (sInPixels / self.baseWidth)
                            t = 1 - (tInPixels / self.baseHeight) # Complemented to deal with loading image upside down.
                            S = (swInPixels / self.baseWidth)
                            T = 1 - (thInPixels / self.baseHeight) # Complemented to deal with loading image upside down.
                            blend = "overwrite" if frameCallNode.attrib.get("blend") == None else frameCallNode.attrib.get("blend")
                            scaleX = 1 if frameCallNode.attrib.get("scale-x") == None else float(frameCallNode.attrib.get("scale-x"))
                            scaleY = 1 if frameCallNode.attrib.get("scale-y") == None else float(frameCallNode.attrib.get("scale-y"))
                            color = Color(1,1,1,1)
                            tweenHasColor = False
                            frameCallHasColor = False
                            frameCallColorName = frameCallNode.attrib.get("color-name")
                            if frameCallColorName != None:
                                # Get color at frame call as first resort.
                                frameCallHasColor = True
                                for colorNode in self.colors.getiterator('color'):
                                    if colorNode.tag == 'color' and colorNode.attrib.get("name") == frameCallColorName:
                                        R = 1 if colorNode.attrib.get("r") == None else float(colorNode.attrib.get("r"))
                                        G = 1 if colorNode.attrib.get("g") == None else float(colorNode.attrib.get("g"))
                                        B = 1 if colorNode.attrib.get("b") == None else float(colorNode.attrib.get("b"))
                                        A = 1 if colorNode.attrib.get("a") == None else float(colorNode.attrib.get("a"))
                                        color = Color(R, G, B, A)
                                        break # leave for loop when we find the correct color
                                pass

                            if tweenId != None and tweenId != "0":
                                # Get color at tween frame as second resort.
                                thisTween = None
                                frameLength = 1
                                advancementFunction = "linear"
                                foundTween = False
                                pointList = []
                                colorList = []
                                for tweenNode in self.tweens.getiterator('motion-tween'):
                                    if tweenNode.tag == "motion-tween" and tweenNode.attrib.get("id") == tweenId:
                                        foundTween = True
                                        frameLength = 1 if tweenNode.attrib.get("length-in-frames") == None else tweenNode.attrib.get("length-in-frames")
                                        advancementFunction = "linear" if tweenNode.attrib.get("advancement-function") == None else tweenNode.attrib.get("advancement-function")
                                        for pointOrColorNode in tweenNode.getiterator():
                                            if pointOrColorNode.tag == "point":
                                                pX = 0 if pointOrColorNode.attrib.get("x") == None else float(pointOrColorNode.attrib.get("x"))
                                                pY = 0 if pointOrColorNode.attrib.get("y") == None else float(pointOrColorNode.attrib.get("y"))
                                                pointList.append(Point(pX, pY, 0))
                                            elif pointOrColorNode.tag == "color-state":
                                                colorName = "white" if pointOrColorNode.attrib.get("name") == None else pointOrColorNode.attrib.get("name")
                                                for colorNode in self.colors.getiterator('color'):
                                                    if colorNode.tag == 'color' and colorNode.attrib.get("name") == colorName:
                                                        R = 1 if colorNode.attrib.get("r") == None else float(colorNode.attrib.get("r"))
                                                        G = 1 if colorNode.attrib.get("g") == None else float(colorNode.attrib.get("g"))
                                                        B = 1 if colorNode.attrib.get("b") == None else float(colorNode.attrib.get("b"))
                                                        A = 1 if colorNode.attrib.get("a") == None else float(colorNode.attrib.get("a"))
                                                        colorList.append(Color(R, G, B, A))
                                                        break # leave for loop when we find the correct color reference
                                            pass # Run through all child nodes of selected tween
                                        break # Exit after finding correct tween
                                pass
                                if foundTween:
                                    thisTween = Tween(frameLength, advancementFunction, pointList, colorList)
                                    offset = thisTween.XYFromFrame(frameInTween);
                                    offsetFromTweenX = int(offset.X);
                                    offsetFromTweenY = int(offset.Y);
                                    offsetX += int(offset.X);
                                    offsetY += int(offset.Y);
                                    if thisTween.hasColorComponent():
                                        tweenHasColor = True;
                                        if frameCallHasColor == False:
                                            color = thisTween.colorFromFrame(frameInTween);
                                    pass
                            if frameNode.attrib.get("color-name") != None and frameCallHasColor == False and tweenHasColor == False:
                                # Get color at frame definition as last resort.
                                for colorNode in colors.getiterator('color'):
                                    if colorNode.tag == 'color' and colorNode.attrib.get("name") == frameNode.attrib.get("color-name"):
                                        R = 1 if colorNode.attrib.get("r") == None else float(colorNode.attrib.get("r"))
                                        G = 1 if colorNode.attrib.get("g") == None else float(colorNode.attrib.get("g"))
                                        B = 1 if colorNode.attrib.get("b") == None else float(colorNode.attrib.get("b"))
                                        A = 1 if colorNode.attrib.get("a") == None else float(colorNode.attrib.get("a"))
                                        color = Color(R, G, B, A)
                                        break # leave for loop when we find the correct color
                                pass
                            rotationZ = 0 if frameCallNode.attrib.get("rotation-z") == None else float(frameCallNode.attrib.get("rotation-z"))
                            frameList.append(Frame(Bound(offsetX, offsetY, addWidth, addHeight), s, t, S, T, blend, scaleX, scaleY, color, rotationZ))
                    pass 
                break # Leave once we've found the appropriate frame

        # Prepare tracking list of consumed nodes.
        self.clearNodesForDrawing()
        # Make an identifier to tack onto primitive names in Panda3d's scene graph.
        frameIndexForName = 1
                
        # Loop through loaded frames that make up composite frame.
        for loadedFrame in frameList:              
            # For debugging purposes, print the object.
            if False:
                loadedFrame.printAsString()
            
            # Set up place to store primitive 3d object; note: requires vertex data made by GeomVertexData
            squareMadeByTriangleStrips = GeomTristrips(Geom.UHDynamic)
              
            # Set up place to hold 3d data and for the following coordinates:
            #   square's points (V3: x, y, z), 
            #   the colors at each point of the square (c4: r, g, b, a), and
            #   for the UV texture coordinates at each point of the square     (t2: S, T).
            vertexData = GeomVertexData('square-'+str(frameIndexForName), GeomVertexFormat.getV3c4t2(), Geom.UHDynamic)
            vertex = GeomVertexWriter(vertexData, 'vertex')
            color = GeomVertexWriter(vertexData, 'color')
            texcoord = GeomVertexWriter(vertexData, 'texcoord') 
              
            # Add the square's data
            # Upper-Left corner of square
            vertex.addData3f(-loadedFrame.bound.Width / 2.0, 0, -loadedFrame.bound.Height / 2.0)
            color.addData4f(loadedFrame.color.R,loadedFrame.color.G,loadedFrame.color.B,loadedFrame.color.A)
            texcoord.addData2f(loadedFrame.s, loadedFrame.T)

            # Upper-Right corner of square
            vertex.addData3f(loadedFrame.bound.Width / 2.0, 0, -loadedFrame.bound.Height / 2.0)
            color.addData4f(loadedFrame.color.R,loadedFrame.color.G,loadedFrame.color.B,loadedFrame.color.A)
            texcoord.addData2f(loadedFrame.S, loadedFrame.T)
            
            # Lower-Left corner of square
            vertex.addData3f(-loadedFrame.bound.Width / 2.0, 0, loadedFrame.bound.Height / 2.0)
            color.addData4f(loadedFrame.color.R,loadedFrame.color.G,loadedFrame.color.B,loadedFrame.color.A)
            texcoord.addData2f(loadedFrame.s, loadedFrame.t)
            
            # Lower-Right corner of square
            vertex.addData3f(loadedFrame.bound.Width / 2.0, 0, loadedFrame.bound.Height / 2.0)
            color.addData4f(loadedFrame.color.R,loadedFrame.color.G,loadedFrame.color.B,loadedFrame.color.A)
            texcoord.addData2f(loadedFrame.S, loadedFrame.t)

            # Pass data to primitive
            squareMadeByTriangleStrips.addNextVertices(4)
            squareMadeByTriangleStrips.closePrimitive()
            square = Geom(vertexData)
            square.addPrimitive(squareMadeByTriangleStrips)
            # Pass primtive to drawing node
            drawPrimitiveNode=GeomNode('square-'+str(frameIndexForName))    
            drawPrimitiveNode.addGeom(square)
            # Pass node to scene (effect camera)
            nodePath = self.effectCameraNodePath.attachNewNode(drawPrimitiveNode)
            # Linear dodge:
            if loadedFrame.blendMode == "darken":
                nodePath.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OOneMinusFbufferColor, ColorBlendAttrib.OOneMinusIncomingColor))
                pass
            elif loadedFrame.blendMode == "multiply":
                nodePath.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OFbufferColor, ColorBlendAttrib.OZero))
                pass
            elif loadedFrame.blendMode == "color-burn":
                nodePath.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OZero, ColorBlendAttrib.OOneMinusIncomingColor))
                pass
            elif loadedFrame.blendMode == "linear-burn":
                nodePath.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OZero, ColorBlendAttrib.OIncomingColor))
                pass
            elif loadedFrame.blendMode == "lighten":
                nodePath.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MMax, ColorBlendAttrib.OIncomingColor, ColorBlendAttrib.OFbufferColor))
                pass
            elif loadedFrame.blendMode == "color-dodge":
                nodePath.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OOne, ColorBlendAttrib.OOne))
                pass
            elif loadedFrame.blendMode == "linear-dodge":
                nodePath.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OOne, ColorBlendAttrib.OOneMinusIncomingColor))
                pass
            else: # Overwrite:
                nodePath.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOneMinusIncomingAlpha))
                pass
            nodePath.setDepthTest(False)
            # Apply texture
            nodePath.setTexture(self.tex)
            # Apply translation, then rotation, then scaling to node.
            nodePath.setPos((loadedFrame.bound.X + loadedFrame.bound.Width / 2.0, 1, -loadedFrame.bound.Y - loadedFrame.bound.Height / 2.0))
            nodePath.setR(loadedFrame.rotationZ)
            nodePath.setScale(loadedFrame.scaleX, 1, loadedFrame.scaleY)
            nodePath.setTwoSided(True)
            self.consumedNodesList.append(nodePath)
            frameIndexForName = frameIndexForName + 1
        # Loop continues on through each frame called in the composite frame.
        pass
