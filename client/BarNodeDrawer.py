from Config import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
import GUI
import os
import os.path
from operator import itemgetter, attrgetter

#THEME
class Bar:
    textureList = []
    frameCard = None
    barCard = None
    container = None
    width = 0
    height = 0
    bar = 'bar-3'
    path = GAME+'/textures/gui/'+THEME+'/'+bar+'/'
    # Force following textures to not be power-of-2 scaled (up or down); setting is probably global.
    texture = Texture()
    texture.setTexturesPower2(ATSNone)
    def __init__(self, bar='bar-3', parent=None):
        self.bar = bar
        self.path = GAME+'/textures/gui/'+THEME+'/'+self.bar+'/'
        self.container = NodePath("container")
        if parent != None:
            self.container.reparentTo(parent)
        dirList=os.listdir(self.path)
        for fname in dirList:
            fileWithoutExtension = os.path.splitext(fname)[0]
            if str(fileWithoutExtension) == 'frame' or (int(fileWithoutExtension) >= 0 and int(fileWithoutExtension) <= 100):
                texture = loader.loadTexture(self.path+fname)
                texture.setMagfilter(Texture.FTNearest)
                texture.setMinfilter(Texture.FTNearest)
                texture.setAnisotropicDegree(0)
                texture.setWrapU(Texture.WMClamp)
                texture.setWrapV(Texture.WMClamp)
                self.textureList.append((str(fileWithoutExtension), texture))
                if str(fileWithoutExtension) == 'frame':
                    self.width = texture.getOrigFileXSize()
                    self.height = texture.getOrigFileYSize()
                    # Create background card from frame.
                    cm = CardMaker('bar-frame-'+bar+'-background')
                    cm.setFrame(0, self.width, 0, self.height)
                    card = self.container.attachNewNode(cm.generate())
                    card.setTexture(texture)
                    card.setScale(GUI.v)
                    card.setTransparency(True)
                    self.frameCard = card
                    # Create foreground card from frame dimensions.
                    cm = CardMaker('bar-frame-'+bar+'-foreground')
                    cm.setFrame(0, self.width, 0, self.height)
                    card = self.container.attachNewNode(cm.generate())
                    card.setScale(GUI.v)
                    card.setTexture(texture)
                    card.setTransparency(True)
                    self.barCard = card
            # Sort list for future comparison to value numbers.
            self.textureList = sorted(self.textureList, cmp=self.orderByNumber)
            pass

    def orderByNumber(self, x, y):
        if str(x[0]) == 'frame':
            return 1
        if str(y[0]) == 'frame':
            return -1
        return int(x[0]) - int(y[0])
        pass

    def updateTo(self, value):
        index = 0
        for i in range(0, len(self.textureList),1):
            if str(self.textureList[i][0]) != 'frame':
                if int(self.textureList[i][0]) > value:
                    self.barCard.setTexture(self.textureList[index][1])
                    return
                elif int(self.textureList[i][0]) == value:
                    index = i
                    self.barCard.setTexture(self.textureList[index][1])
                    return
                index = i
                pass
        pass

    def getFrameSize(self):
        return (0, GUI.v*self.width, 0, GUI.v*self.height)
        pass
