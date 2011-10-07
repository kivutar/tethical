import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.DirectGui import *
from pandac.PandaModules import *
import GUI
from Config import *

class MenuNodeDrawer:

    screenCanvasWidth = base.win.getXSize()
    screenCanvasHeight = base.win.getYSize()
    menuItemHeight = 45
    showAtMostXItems = 8
    showAtLeastXItems = 8
    menuHeadingPixels = 11
    menuEndCapPixels = 15
    menuCursorColumnWidth = 30
    menuComponentsWidth = 30
    menuPercent = 10
    menuWidth = screenCanvasWidth - 2 * (screenCanvasWidth / (menuPercent * base.getAspectRatio()))
    menuHeight = menuItemHeight*showAtLeastXItems + menuHeadingPixels + menuEndCapPixels
    startingPointX = 0
    startingPointY = 0
    positioningNode = None
    sceneBackgroundCard = None
    targetWidth = 0
    targetHeight = 0
    targetScaleX = 1.0
    targetScaleY = 1.0
    targetScaleZ = 1.0
    path = "default"
    columns = []

    def __init__(self, targetWidth=2.0, targetHeight=2.0, menuHeadingPixels=7, menuEndCapPixels=4, menuCursorColumnWidth=60, menuComponentsWidth=35, menuPercent = 10, menuItemHeight=35, columns=[], path="default"):
        self.path = path
        self.columns = columns
        self.targetWidth = targetWidth
        self.targetHeight = targetHeight        
        self.targetScaleX = float(self.targetWidth) / float(self.screenCanvasWidth)
        self.targetScaleZ = float(self.targetHeight) / float(self.screenCanvasHeight)
        self.targetScaleY = (self.targetScaleX + self.targetScaleZ) / 2.0
        self.menuItemHeight = menuItemHeight
        self.menuHeadingPixels = menuHeadingPixels
        self.menuEndCapPixels = menuEndCapPixels
        self.menuCursorColumnWidth = menuCursorColumnWidth
        self.menuComponentsWidth = menuComponentsWidth
        self.menuPercent = menuPercent
        self.menuWidth = self.screenCanvasWidth
        self.menuHeight = self.menuItemHeight*self.showAtLeastXItems #+ self.menuHeadingPixels + self.menuEndCapPixels
        # Positioning NodePath that all children belong to:
        self.positioningNode = NodePath('menu-geometry-positioning')
        self.positioningNode.setScale(self.targetScaleX, self.targetScaleY, self.targetScaleZ)        
        self.positioningNode.setPos(-targetWidth/2.0, 0.0, -targetHeight/2.0)
        # Set up background.
        self.sceneBackgroundCard = CardMaker('scene-background')        
        self.sceneBackgroundCard.setFrame(0, self.menuWidth, self.screenCanvasHeight-self.menuHeight, self.screenCanvasHeight)
        self.sceneBackground = self.positioningNode.attachNewNode(self.sceneBackgroundCard.generate())
        self.sceneBackground.setPos(0, 2, 0) # Put it into viewing distance.
        self.sceneBackground.setColor(1,1,1,.5)
        self.sceneBackground.setTransparency(True)
        # Set up end cap.
        if self.menuEndCapPixels >= 1:
            self.drawEndCap()
        # Set up body.
        self.drawBody()
        # Set up heading.
        self.drawHeading()
        if self.columns != []:
            self.parseColumnHeadings()

    def parseColumnHeadings(self):
        # Placeholder; is a sum of listed columns.
        totalColumnWidth = 0.0;
        # Ratio between totalColumnWidth versus totalAvailableColumnWidth
        translationPercentage = 1.0;
        # Remove cursor column and up/down components column widths.
        totalAvailableColumnWidth = self.menuWidth - self.menuCursorColumnWidth - self.menuComponentsWidth
        # Figure +startX value.
        columnsStartAtX = self.menuCursorColumnWidth
        for column in self.columns:
            totalColumnWidth += column["columnWidth"]
            pass
        # Compare totalColumnWidth to totalAvailableColumnWidth; yields percentage.
        translationPercentage = float(totalAvailableColumnWidth / totalColumnWidth)
        runningWidth = columnsStartAtX
        i = 0
        for column in self.columns:
            # True: put a background to identify the columns with.
            if False:
                bg = CardMaker('bg-node')
                v = float(i)/float(len(self.columns))
                print v
                bg.setFrame(runningWidth, runningWidth+translationPercentage*column["columnWidth"], 0, self.menuHeadingPixels)
                bgPath = self.headingPath.attachNewNode(bg.generate())
                bgPath.setColor(1-v,1-v,1-v,1)
                i += 1
                pass
            # Draw text.
            text = TextNode('text-node')
            text.setText(column["label"])
            text.setFont(column['font'])
            textNodePath = aspect2d.attachNewNode(text)
            textNodePath.reparentTo(self.headingPath)
            textNodePath.setScale(25.0)
            pt1, pt2 = textNodePath.getTightBounds()
            textWidth = pt2.x - pt1.x
            thisColumnWidth = translationPercentage*column["columnWidth"]
            if column["align"] == TextNode.ARight:
                textNodePath.setPos(self.headingPath, runningWidth+thisColumnWidth-textWidth, 0, 0)
                pass
            elif column["align"] == TextNode.ACenter:
                textNodePath.setPos(self.headingPath, runningWidth+(thisColumnWidth-textWidth)/2.0, 0, 0)
                pass
            else: # Left 
                textNodePath.setPos(self.headingPath, runningWidth, 0, 0)
                pass            
            runningWidth += translationPercentage*column["columnWidth"]
        pass

    # Universal 9-card drawer; constructors is laid out in upper-left -> upper-right, middle-left -> middle-right, lower-left -> lower-right
    def createNodePath(self, name, width, height, imageFileA, imageFileG,  imageFileC, imageFileE, imageFileI, imageFileF, imageFileB, imageFileH, imageFileD):        
        # A G----------> C
        # E I----------> F
        # | |            |
        # | |            |
        # B H----------> D
        textures = []
        # Load image        
        textureA = loader.loadTexture(imageFileA)
        textureA.setMagfilter(Texture.FTNearest)
        textureA.setMinfilter(Texture.FTNearest)
        textureA.setWrapU(Texture.WMRepeat)
        textureA.setWrapV(Texture.WMRepeat)
        textures.append(textureA)
        textureB = loader.loadTexture(imageFileB)
        textureB.setMagfilter(Texture.FTNearest)
        textureB.setMinfilter(Texture.FTNearest)
        textureB.setWrapU(Texture.WMRepeat)
        textureB.setWrapV(Texture.WMRepeat)
        textures.append(textureB)
        textureC = loader.loadTexture(imageFileC)
        textureC.setMagfilter(Texture.FTNearest)
        textureC.setMinfilter(Texture.FTNearest)
        textureC.setWrapU(Texture.WMRepeat)
        textureC.setWrapV(Texture.WMRepeat)
        textures.append(textureC)
        textureD = loader.loadTexture(imageFileD)
        textureD.setMagfilter(Texture.FTNearest)
        textureD.setMinfilter(Texture.FTNearest)
        textureD.setWrapU(Texture.WMRepeat)
        textureD.setWrapV(Texture.WMRepeat)
        textures.append(textureD)
        textureE = loader.loadTexture(imageFileE)
        textureE.setMagfilter(Texture.FTNearest)
        textureE.setMinfilter(Texture.FTNearest)
        textureE.setWrapU(Texture.WMRepeat)
        textureE.setWrapV(Texture.WMRepeat)
        textures.append(textureE)
        textureF = loader.loadTexture(imageFileF)
        textureF.setMagfilter(Texture.FTNearest)
        textureF.setMinfilter(Texture.FTNearest)
        textureF.setWrapU(Texture.WMRepeat)
        textureF.setWrapV(Texture.WMRepeat)
        textures.append(textureF)
        textureG = loader.loadTexture(imageFileG)
        textureG.setMagfilter(Texture.FTNearest)
        textureG.setMinfilter(Texture.FTNearest)
        textureG.setWrapU(Texture.WMRepeat)
        textureG.setWrapV(Texture.WMRepeat)
        textures.append(textureG)
        textureH = loader.loadTexture(imageFileH)
        textureH.setMagfilter(Texture.FTNearest)
        textureH.setMinfilter(Texture.FTNearest)
        textureH.setWrapU(Texture.WMRepeat)
        textureH.setWrapV(Texture.WMRepeat)
        textures.append(textureH)
        textureI = loader.loadTexture(imageFileI)
        textureI.setMagfilter(Texture.FTNearest)
        textureI.setMinfilter(Texture.FTNearest)
        textureI.setWrapU(Texture.WMRepeat)
        textureI.setWrapV(Texture.WMRepeat)
        textures.append(textureI)
        
        coordinates = [
            {'left': 0, 'right': textureA.getOrigFileXSize(), 'bottom': height-textureA.getOrigFileYSize(), 'top': height},
            {'left': 0, 'right': textureB.getOrigFileXSize(), 'bottom': 0, 'top': textureB.getOrigFileYSize()},
            {'left': width-textureC.getOrigFileXSize(), 'right': width, 'bottom': height-textureC.getOrigFileYSize(), 'top': height},
            {'left': width-textureD.getOrigFileXSize(), 'right': width, 'bottom': 0, 'top': textureD.getOrigFileYSize()},
            {'left': 0, 'right': textureE.getOrigFileXSize(), 'bottom': textureB.getOrigFileYSize(), 'top': height-textureA.getOrigFileYSize()},
            {'left': width-textureF.getOrigFileXSize(), 'right': width, 'bottom': textureD.getOrigFileYSize(), 'top': height-textureC.getOrigFileYSize()},
            {'left': textureA.getOrigFileXSize(), 'right': width-textureC.getOrigFileXSize(), 'bottom': height-textureG.getOrigFileYSize(), 'top': height},
            {'left': textureB.getOrigFileXSize(), 'right': width-textureD.getOrigFileXSize(), 'bottom': 0, 'top': textureH.getOrigFileYSize()},
            {'left': textureE.getOrigFileXSize(), 'right': width-textureF.getOrigFileXSize(), 'bottom': textureH.getOrigFileYSize(), 'top': height-textureG.getOrigFileYSize()}
        ]
        
        # Begin creating NodePath objects.
        container = NodePath(name)
        cards = []
        nodePaths = []
        for i in range(0, 9, 1):
            card = CardMaker(name+'-card-'+str(i))
            nodeWidth = coordinates[i]["right"]-coordinates[i]["left"]
            nodeHeight = coordinates[i]["top"]-coordinates[i]["bottom"]
            textureWidth = textures[i].getOrigFileXSize()
            textureHeight = textures[i].getOrigFileYSize()
            card.setFrame(coordinates[i]["left"], coordinates[i]["right"], coordinates[i]["bottom"], coordinates[i]["top"])
            card.setUvRange((0,0), (nodeWidth/textureWidth, nodeHeight/textureHeight))
            cards.append(card)
            nodePaths.append(container.attachNewNode(cards[i].generate()))
            nodePaths[i].setTexture(textures[i])    
        return container
        pass

    def drawHeading(self):
        if self.menuHeadingPixels <= 0:
            self.headingPath = NodePath('menu-heading')
            pass
        else:
            path = self.path
            component = "heading"
            self.headingPath = self.createNodePath('menu-heading', 
                                    self.menuWidth, 
                                    self.menuHeadingPixels, 
                                    GAME+'/textures/gui/'+path+'/menu/'+component+'/'+'upper-left.png',
                                    GAME+'/textures/gui/'+path+'/menu/'+component+'/'+'upper-middle.png',
                                    GAME+'/textures/gui/'+path+'/menu/'+component+'/'+'upper-right.png',
                                    GAME+'/textures/gui/'+path+'/menu/'+component+'/'+'middle-left.png',
                                    GAME+'/textures/gui/'+path+'/menu/'+component+'/'+'middle-middle.png',
                                    GAME+'/textures/gui/'+path+'/menu/'+component+'/'+'middle-right.png',
                                    GAME+'/textures/gui/'+path+'/menu/'+component+'/'+'lower-left.png',
                                    GAME+'/textures/gui/'+path+'/menu/'+component+'/'+'lower-middle.png',
                                    GAME+'/textures/gui/'+path+'/menu/'+component+'/'+'lower-right.png')
            pass
        # Parent it and position it whether it's blank or not.
        self.headingPath.reparentTo(self.positioningNode)
        # Draw above the menu height.
        self.headingPath.setPos(self.startingPointX, 0, self.screenCanvasHeight)
        pass

    def drawBody(self):
        path = self.path
        component = "body"
        self.bodyPath = self.createNodePath('menu-body', 
                                self.menuWidth, 
                                self.menuHeight, 
                                GAME+'/textures/gui/'+path+'/menu/'+component+'/'+'upper-left.png',
                                GAME+'/textures/gui/'+path+'/menu/'+component+'/'+'upper-middle.png',
                                GAME+'/textures/gui/'+path+'/menu/'+component+'/'+'upper-right.png',
                                GAME+'/textures/gui/'+path+'/menu/'+component+'/'+'middle-left.png',
                                GAME+'/textures/gui/'+path+'/menu/'+component+'/'+'middle-middle.png',
                                GAME+'/textures/gui/'+path+'/menu/'+component+'/'+'middle-right.png',
                                GAME+'/textures/gui/'+path+'/menu/'+component+'/'+'lower-left.png',
                                GAME+'/textures/gui/'+path+'/menu/'+component+'/'+'lower-middle.png',
                                GAME+'/textures/gui/'+path+'/menu/'+component+'/'+'lower-right.png')
        self.bodyPath.reparentTo(self.positioningNode)
        self.bodyPath.setPos(self.startingPointX, 0, self.screenCanvasHeight-self.menuHeight)
        pass

    def drawEndCap(self):        
        path = self.path
        component = "end-cap"
        self.endCapPath = self.createNodePath('menu-end-cap', 
                                self.menuWidth, 
                                self.menuEndCapPixels, 
                                GAME+'/textures/gui/'+path+'/menu/'+component+'/'+'upper-left.png',
                                GAME+'/textures/gui/'+path+'/menu/'+component+'/'+'upper-middle.png',
                                GAME+'/textures/gui/'+path+'/menu/'+component+'/'+'upper-right.png',
                                GAME+'/textures/gui/'+path+'/menu/'+component+'/'+'middle-left.png',
                                GAME+'/textures/gui/'+path+'/menu/'+component+'/'+'middle-middle.png',
                                GAME+'/textures/gui/'+path+'/menu/'+component+'/'+'middle-right.png',
                                GAME+'/textures/gui/'+path+'/menu/'+component+'/'+'lower-left.png',
                                GAME+'/textures/gui/'+path+'/menu/'+component+'/'+'lower-middle.png',
                                GAME+'/textures/gui/'+path+'/menu/'+component+'/'+'lower-right.png')
        self.endCapPath.reparentTo(self.positioningNode)
        # Draw below the menu height.
        self.endCapPath.setPos(self.startingPointX, 0, (self.screenCanvasHeight-self.menuHeight)-self.menuEndCapPixels)
        pass

    def getNodePath(self):
        return self.positioningNode