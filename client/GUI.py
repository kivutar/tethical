from panda3d.core import loadPrcFile
loadPrcFile("../config.prc")
import direct.directbase.DirectStart
from direct.showbase import DirectObject
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.DirectGui import *
from direct.task import Task
from direct.actor import Actor
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
import functools

GAME = ConfigVariableString('game', 'fft').getValue()

CROSS_BTN    = ConfigVariableString('cross-btn',    '0').getValue()
CIRCLE_BTN   = ConfigVariableString('circle-btn',   '3').getValue()
TRIANGLE_BTN = ConfigVariableString('triangle-btn', '2').getValue()
SQUARE_BTN   = ConfigVariableString('square-btn',   '1').getValue()
L1_BTN       = ConfigVariableString('l1-btn',       '4').getValue()
L2_BTN       = ConfigVariableString('l2-btn',       '7').getValue()
R1_BTN       = ConfigVariableString('r1-btn',       '6').getValue()
R2_BTN       = ConfigVariableString('r2-btn',       '9').getValue()
START_BTN    = ConfigVariableString('start-btn',    '8').getValue()
SELECT_BTN   = ConfigVariableString('select-btn',   '5').getValue()

u = 1.0/128.0
v = 1.0/120.0
hover_snd = base.loader.loadSfx(GAME+"/sounds/hover.ogg")
clicked_snd = base.loader.loadSfx(GAME+"/sounds/clicked.ogg")
cancel_snd = base.loader.loadSfx(GAME+"/sounds/cancel.ogg")
regularscale = 2*16.0/240.0
scale = 2*12.0/240.0
regularfont = loader.loadFont(GAME+'/fonts/fft')
font3 = loader.loadFont(GAME+'/fonts/fft3')
font4 = loader.loadFont(GAME+'/fonts/fft4')
coordsfont = loader.loadFont(GAME+'/fonts/fftcoords')

class Coords(DirectObject.DirectObject):

    def __init__(self, tile):

        self.coordstn = TextNode('tn')
        self.coordstn.setFont(coordsfont)
        self.coordstn.setAlign(self.coordstn.ARight)
        self.coordstn.setTextColor(1,1,1,1)
        self.tnp = aspect2d.attachNewNode(self.coordstn)
        self.tnp.setScale(scale)
        self.tnp.setPos(v*112, 0, v*66)

        self.update(tile)

    def update(self, tile):
        self.coordstn.setText(str(tile['z']/2).replace('.0','').replace('.5','a')+'h')

    def destroy(self):
        self.tnp.removeNode()

class Background(DirectObject.DirectObject):

    def __init__(self, command):
        
        tex = loader.loadTexture(GAME+'/textures/gui/loadingbackground.png')
        tex.setMagfilter(Texture.FTNearest)
        tex.setMinfilter(Texture.FTNearest)

        base.setBackgroundColor(.03125, .03125, .03125)

        self.frame = DirectFrame( color = (1, 1, 1, 1), frameTexture = tex, frameSize = ( -v*128, v*128, -v*128, v*128 ), scale = 10 )
        self.frame.setTransparency(True)

        seq = Sequence()
        i = LerpScaleInterval(self.frame, 0.1, 1, startScale=10 )
        seq.append(i)
        seq.append( Wait(0.5) )
        seq.append( Func(command) )
        seq.start()

class Test(DirectObject.DirectObject):

    def __init__(self, image):

        tex = loader.loadTexture(GAME+'/textures/gui/'+image+'.png')
        tex.setMagfilter(Texture.FTNearest)
        tex.setMinfilter(Texture.FTNearest)

        base.setBackgroundColor(0,0,1)

        self.frame = DirectFrame(
                color = (1, 1, 1, 1),
                frameTexture = tex,
                frameSize = ( -v*128.0, v*128.0, -v*128.0, v*128.0 ),
                scale = 1,
                sortOrder= -2,
        )
        self.frame.setTransparency(True)

class LoginWindow(DirectObject.DirectObject):

    def __init__(self, command):
        
        tex = loader.loadTexture(GAME+'/textures/gui/login_window.png')
        tex.setMagfilter(Texture.FTNearest)
        tex.setMinfilter(Texture.FTNearest)

        self.frame = DirectFrame( frameTexture = tex, color = (1, 1, 1, 1), frameSize = ( -v*64.0, v*64.0, -v*32.0, v*32.0 ), scale = 0.1 )
        self.frame.setTransparency(True)

        self.loginLabel = DirectLabel(
            text = 'Username:',
            color = (0,0,0,0),
            scale = regularscale,
            text_font = regularfont,
            text_fg = (1,1,1,1),
            text_align = TextNode.ALeft,
            parent = self.frame
        )
        self.loginLabel.setPos(-v*50, 0, v*3)

        self.loginEntry = DirectEntry(
            color = (0,0,0,0),
            scale = regularscale,
            numLines = 1,
            focus = 1,
            text_font = regularfont,
            text_fg = (1,1,1,1),
            parent = self.frame
        )
        self.loginEntry.setPos(-v*6, 0, v*3)

        self.passwordLabel = DirectLabel(
            text = 'Password:',
            color = (0,0,0,0),
            scale = regularscale,
            text_font = regularfont,
            text_fg = (1,1,1,1),
            text_align = TextNode.ALeft,
            parent = self.frame
        )
        self.passwordLabel.setPos(-v*50, 0, -v*13)

        self.passwordEntry = DirectEntry(
            color = (0,0,0,0),
            scale = regularscale,
            numLines = 1,
            text_font = regularfont,
            text_fg = (1,1,1,1),
            obscured = True,
            parent = self.frame
        )
        self.passwordEntry.setPos(-v*6, 0, -v*13)

        connectButton = DirectButton(
            scale = regularscale,
            text  = ("Connect", "Connect", "Connect", "disabled"),
            command = command,
            color = (.62, .6, .5, 1),
            text_font = regularfont,
            text_fg = (1,1,1,1),
            rolloverSound = hover_snd,
            clickSound = clicked_snd,
            pressEffect = 0,
            pad = (.15,.15),
            parent = self.frame
        )
        connectButton.setPos(v*38, 0, -v*40)

        seq = Sequence()
        i = LerpScaleInterval(self.frame, 0.1, 1, startScale=0.1 )
        seq.append(i)
        seq.start()

    def commandanddestroy(self, command):
        seq = Sequence()
        i = LerpScaleInterval(self.frame, 0.1, 0.1, startScale=1 )
        seq.append(i)
        seq.append( Func(self.frame.destroy) )
        seq.append( Wait(0.5) )
        seq.append( Func(command) )
        seq.start()

class PartyListWindow(DirectObject.DirectObject):

    def __init__(self, command, createpartycommand):

        self.command = command
        self.createpartycommand = createpartycommand

        tex = loader.loadTexture(GAME+'/textures/gui/parties_window.png')
        tex.setMagfilter(Texture.FTNearest)
        tex.setMinfilter(Texture.FTNearest)
    
        self.frame = DirectFrame( frameTexture = tex, color = (1, 1, 1, 1), frameSize = ( -v*128.0, v*128.0, -v*128.0, v*128.0 ), scale=0.1 )
        self.frame.setTransparency(True)
        
        cptexture = loader.loadTexture(GAME+'/textures/gui/create_party.png')
        cptexture.setMagfilter(Texture.FTNearest)
        cptexture.setMinfilter(Texture.FTNearest)

        self.cpframe = DirectFrame(
            frameTexture = cptexture,
            frameColor = (1, 1, 1, 1),
            frameSize = ( -v*32.0, v*32.0, -v*8.0, v*8.0 ),
            pos = (0, 0, -.8),
            scale = 1.0,
        )
        self.cpframe.setTransparency(True)
        
        Sequence(
            Parallel(
                LerpScaleInterval(self.frame, 0.1, 1, startScale=0.1 ),
                LerpPosInterval(self.cpframe, 0.25, (0, 0, -.8), (0, 0, -1.0)),
            ),
            Func( self.acceptAll ),
        ).start()

    def acceptAll(self):
        self.accept(TRIANGLE_BTN, self.onTriangleClicked)

    def onTriangleClicked(self):
        clicked_snd.play()
        self.commandAndDestroy(self.createpartycommand)

    def commandAndDestroy(self,command):
        Sequence(
            Parallel(
                LerpScaleInterval(self.frame, 0.1, 0.1, startScale=1),
                LerpPosInterval(self.cpframe, 0.25, (0, 0, -1.0), (0, 0, -0.8)),
            ),
            Func(self.ignoreAll),
            Func(self.cpframe.destroy),
            Func(self.frame.destroy),
            Func(command),
        ).start()

    def refresh(self, parties):

        for child in self.frame.getChildren():
            child.removeNode()

        buttons = {}
        commands = {}
        for i,key in enumerate(parties):
            nameLabel = DirectLabel(
                color = (0,0,0,0),
                text = parties[key]['name'],
                scale = regularscale,
                text_font = regularfont,
                text_fg = (1,1,1,1),
                text_align = TextNode.ALeft,
                parent = self.frame
            )
            nameLabel.setPos(-v*93, 0, v*49 - i*v*16)

            creatorLabel = DirectLabel(
                color = (0,0,0,0),
                text = parties[key]['creator'],
                scale = regularscale,
                text_font = regularfont,
                text_fg = (1,1,1,1),
                text_align = TextNode.ALeft,
                parent = self.frame
            )
            creatorLabel.setPos(-v*30, 0, v*49 - i*v*16)

            mapLabel = DirectLabel(
                color = (0,0,0,0),
                text = parties[key]['map']['name'],
                scale = regularscale,
                text_font = regularfont,
                text_fg = (1,1,1,1),
                text_align = TextNode.ALeft,
                parent = self.frame
            )
            mapLabel.setPos(v*20, 0, v*49 - i*v*16)
            
            commands[key] = functools.partial(self.command, key)
            commands[key].__name__ = str(key)
            buttons[key] = DirectButton(
                text  = (str(len(parties[key]['players']))+'/'+str(len(parties[key]['map']['chartiles'])), "Join", "Join", "Full"),
                command = self.commandAndDestroy,
                extraArgs = [ commands[key] ],
                scale = regularscale,
                text_font = regularfont,
                text_fg = (1,1,1,1),
                text_align = TextNode.ALeft,
                rolloverSound = hover_snd,
                clickSound = clicked_snd,
                pressEffect = 0,
                parent = self.frame
            )
            buttons[key].setPos(v*80, 0, v*49 - i*v*16)

            if len(parties[key]['players']) >= len(parties[key]['map']['chartiles']):
                buttons[key]['state'] = DGG.DISABLED

class Menu(DirectObject.DirectObject):

    def __init__(self, char, movecommand, attackcommand, waitcommand, cancelcommand):

        self.offset = 22
        self.height = 16
        self.index = 0
        self.cancelcommand = cancelcommand

        self.buttons = [
            { 'text': 'Move',   'enabled': char['canmove'], 'pos': (-v*36.5,0,v*(self.offset-self.height*0)), 'command': movecommand   },
            { 'text': 'Attack', 'enabled': char['canact' ], 'pos': (-v*36.5,0,v*(self.offset-self.height*1)), 'command': attackcommand },
            { 'text': 'Wait',   'enabled': True           , 'pos': (-v*36.5,0,v*(self.offset-self.height*2)), 'command': waitcommand   },
            { 'text': 'Status', 'enabled': False          , 'pos': (-v*36.5,0,v*(self.offset-self.height*3)), 'command': cancelcommand },
        ]

        menutexture = loader.loadTexture(GAME+'/textures/gui/menu.png')
        menutexture.setMagfilter(Texture.FTNearest)
        menutexture.setMinfilter(Texture.FTNearest)

        handtexture = loader.loadTexture(GAME+'/textures/gui/hand.png')
        handtexture.setMagfilter(Texture.FTNearest)
        handtexture.setMinfilter(Texture.FTNearest)

        self.frame = DirectFrame(
            frameTexture = menutexture,
            frameColor = (1, 1, 1, 1),
            frameSize = ( -v*32.0, v*32.0, -v*64.0, v*64.0 ),
            pos = (v*73.0, 0, v*10.0),
            scale = 0.1,
        )
        self.frame.setTransparency(True)

        self.hand = DirectFrame(
            frameTexture = handtexture,
            frameColor = (1, 1, 1, 1),
            frameSize = ( -v*8, v*8, -v*8, v*8 ),
            pos = self.buttons[0]['pos'],
            parent = self.frame
        )

        for i,button in enumerate(self.buttons):
            label = DirectLabel(
                color = (0,0,0,0),
                text = button['text'],
                scale = regularscale,
                text_font = regularfont,
                text_fg = (1,1,1,1),
                text_align = TextNode.ALeft,
                parent = self.frame,
                pos = (-v*25, 0, v*(self.offset-3-self.height*i))
            )
            if not button['enabled']:
                label['text_fg'] = (1,1,1,.5)
        
        seq = Sequence()
        seq.append(LerpScaleInterval(self.frame, 0.1, 1, startScale=0.1))
        seq.append(Func(self.acceptAll))
        seq.start()

    def acceptAll(self):
        self.accept(CROSS_BTN,  self.onCrossClicked)
        self.accept(CIRCLE_BTN, self.onCircleClicked)
        self.accept("arrow_down",        lambda: self.updateIndex( 1))
        self.accept("arrow_down-repeat", lambda: self.updateIndex( 1))
        self.accept("arrow_up",          lambda: self.updateIndex(-1))
        self.accept("arrow_up-repeat",   lambda: self.updateIndex(-1))

    def updateIndex(self, direction):
        hover_snd.play()
        next = self.index + direction
        if next == len(self.buttons):
            next = 0
        if next == -1:
            next = len(self.buttons)-1
        self.hand.setPos(self.buttons[next]['pos'])
        self.index = next

    def onCircleClicked(self):
        if self.buttons[self.index]['enabled']:
            clicked_snd.play()
            self.commandAndDestroy(self.buttons[self.index]['command'])

    def onCrossClicked(self):
        cancel_snd.play()
        self.commandAndDestroy(self.cancelcommand)

    def commandAndDestroy(self,command):
        seq = Sequence()
        seq.append(LerpScaleInterval(self.frame, 0.1, 0.1, startScale=1))
        seq.append(Func(self.ignoreAll))
        seq.append(Func(self.frame.destroy))
        seq.append(Func(command))
        seq.start()

class MoveCheck(DirectObject.DirectObject):

    def __init__(self, command, cancelcommand):

        self.offset = -10
        self.height = 16
        self.index = 0
        self.cancelcommand = cancelcommand

        self.buttons = [
            { 'text': 'Yes',   'enabled': True, 'pos': (v*45.5,0,v*(self.offset-self.height*0)), 'command': command       },
            { 'text': 'No',    'enabled': True, 'pos': (v*45.5,0,v*(self.offset-self.height*1)), 'command': cancelcommand },
        ]

        tex = loader.loadTexture(GAME+'/textures/gui/move_check.png')
        tex.setMagfilter(Texture.FTNearest)
        tex.setMinfilter(Texture.FTNearest)

        handtexture = loader.loadTexture(GAME+'/textures/gui/hand.png')
        handtexture.setMagfilter(Texture.FTNearest)
        handtexture.setMinfilter(Texture.FTNearest)

        self.frame = DirectFrame(
            frameTexture = tex,
            frameColor = (1, 1, 1, 1),
            frameSize = ( -v*128.0, v*128.0, -v*64.0, v*64.0 ),
            pos = (0, 0, 0),
            scale = 0.1,
        )
        self.frame.setTransparency(True)

        self.hand = DirectFrame(
            frameTexture = handtexture,
            frameColor = (1, 1, 1, 1),
            frameSize = ( -v*8, v*8, -v*8, v*8 ),
            pos = self.buttons[0]['pos'],
            parent = self.frame
        )

        messageLabel = DirectLabel(
            color = (0,0,0,0),
            text = 'Are you sure you want to move here?',
            scale = regularscale,
            text_font = regularfont,
            text_fg = (1,1,1,1),
            text_align = TextNode.ALeft,
            parent = self.frame,
            pos = (-v*75, 0, v*19)
        )

        for i,button in enumerate(self.buttons):
            label = DirectLabel(
                color = (0,0,0,0),
                text = button['text'],
                scale = regularscale,
                text_font = regularfont,
                text_fg = (1,1,1,1),
                text_align = TextNode.ALeft,
                parent = self.frame,
                pos = (v*57, 0, v*(self.offset-3-self.height*i))
            )
            if not button['enabled']:
                label['text_fg'] = (.375,.34375,.28125,1)

        seq = Sequence()
        seq.append(LerpScaleInterval(self.frame, 0.1, 1, startScale=0.1))
        seq.append(Func(self.acceptAll))
        seq.start()

    def acceptAll(self):
        self.accept(CROSS_BTN,  self.onCrossClicked)
        self.accept(CIRCLE_BTN, self.onCircleClicked)
        self.accept("arrow_down",        lambda: self.updateIndex( 1))
        self.accept("arrow_down-repeat", lambda: self.updateIndex( 1))
        self.accept("arrow_up",          lambda: self.updateIndex(-1))
        self.accept("arrow_up-repeat",   lambda: self.updateIndex(-1))

    def updateIndex(self, direction):
        hover_snd.play()
        next = self.index + direction
        if next == len(self.buttons):
            next = 0
        if next == -1:
            next = len(self.buttons)-1
        self.hand.setPos(self.buttons[next]['pos'])
        self.index = next

    def onCircleClicked(self):
        if self.buttons[self.index]['enabled']:
            clicked_snd.play()
            self.commandAndDestroy(self.buttons[self.index]['command'])

    def onCrossClicked(self):
        cancel_snd.play()
        self.commandAndDestroy(self.cancelcommand)

    def commandAndDestroy(self,command):
        seq = Sequence()
        seq.append(LerpScaleInterval(self.frame, 0.1, 0.1, startScale=1))
        seq.append(Func(self.ignoreAll))
        seq.append(Func(self.frame.destroy))
        seq.append(Func(command))
        seq.start()

class AttackCheck(DirectObject.DirectObject):

    def __init__(self, command, cancelcommand):

        self.offset = -18
        self.height = 16
        self.index = 0
        self.cancelcommand = cancelcommand

        self.buttons = [
            { 'text': 'Execute', 'enabled': True, 'pos': (-v*8.5,0,v*(self.offset-self.height*0)), 'command': command       },
            { 'text': 'Quit',    'enabled': True, 'pos': (-v*8.5,0,v*(self.offset-self.height*1)), 'command': cancelcommand },
        ]

        tex = loader.loadTexture(GAME+'/textures/gui/attack_check.png')
        tex.setMagfilter(Texture.FTNearest)
        tex.setMinfilter(Texture.FTNearest)

        handtexture = loader.loadTexture(GAME+'/textures/gui/hand.png')
        handtexture.setMagfilter(Texture.FTNearest)
        handtexture.setMinfilter(Texture.FTNearest)

        self.frame = DirectFrame(
            frameTexture = tex,
            frameColor = (1, 1, 1, 1),
            frameSize = ( -v*64.0, v*64.0, -v*64.0, v*64.0 ),
            pos = (-v*1.0, 0, v*10.0),
            scale = 0.1,
        )
        self.frame.setTransparency(True)

        self.hand = DirectFrame(
            frameTexture = handtexture,
            frameColor = (1, 1, 1, 1),
            frameSize = ( -v*8, v*8, -v*8, v*8 ),
            pos = self.buttons[0]['pos'],
            parent = self.frame
        )

        messageLabel = DirectLabel(
            color = (0,0,0,0),
            text = 'Executing action.\nOK?',
            scale = regularscale,
            text_font = regularfont,
            text_fg = (1,1,1,1),
            text_align = TextNode.ALeft,
            parent = self.frame,
            pos = (-v*33, 0, v*27)
        )

        for i,button in enumerate(self.buttons):
            label = DirectLabel(
                color = (0,0,0,0),
                text = button['text'],
                scale = regularscale,
                text_font = regularfont,
                text_fg = (1,1,1,1),
                text_align = TextNode.ALeft,
                parent = self.frame,
                pos = (v*3, 0, v*(self.offset-3-self.height*i))
            )
            if not button['enabled']:
                label['text_fg'] = (.375,.34375,.28125,1)

        seq = Sequence()
        seq.append(LerpScaleInterval(self.frame, 0.1, 1, startScale=0.1))
        seq.append(Func(self.acceptAll))
        seq.start()

    def acceptAll(self):
        self.accept(CROSS_BTN,  self.onCrossClicked)
        self.accept(CIRCLE_BTN, self.onCircleClicked)
        self.accept("arrow_down",        lambda: self.updateIndex( 1))
        self.accept("arrow_down-repeat", lambda: self.updateIndex( 1))
        self.accept("arrow_up",          lambda: self.updateIndex(-1))
        self.accept("arrow_up-repeat",   lambda: self.updateIndex(-1))

    def updateIndex(self, direction):
        hover_snd.play()
        next = self.index + direction
        if next == len(self.buttons):
            next = 0
        if next == -1:
            next = len(self.buttons)-1
        self.hand.setPos(self.buttons[next]['pos'])
        self.index = next

    def onCircleClicked(self):
        if self.buttons[self.index]['enabled']:
            clicked_snd.play()
            self.commandAndDestroy(self.buttons[self.index]['command'])

    def onCrossClicked(self):
        cancel_snd.play()
        self.commandAndDestroy(self.cancelcommand)

    def commandAndDestroy(self,command):
        seq = Sequence()
        seq.append(LerpScaleInterval(self.frame, 0.1, 0.1, startScale=1))
        seq.append(Func(self.ignoreAll))
        seq.append(Func(self.frame.destroy))
        seq.append(Func(command))
        seq.start()

class Help(DirectObject.DirectObject):

    def __init__(self, message, command, cancelcommand):

        self.command = command
        self.cancelcommand = cancelcommand

        tex = loader.loadTexture(GAME+'/textures/gui/'+message+'.png')
        tex.setMagfilter(Texture.FTNearest)
        tex.setMinfilter(Texture.FTNearest)

        self.frame = DirectFrame(
            frameTexture = tex,
            frameColor = (1, 1, 1, 1),
            frameSize = ( -v*128.0, v*128.0, -v*32.0, v*32.0 ),
            pos = (0, 0, .25),
            scale = 0.1,
        )
        self.frame.setTransparency(True)
        
        seq = Sequence()
        seq.append(LerpScaleInterval(self.frame, 0.1, 1, startScale=0.1))
        seq.append(Func(self.acceptAll))
        seq.start()

    def acceptAll(self):
        self.accept(CROSS_BTN,  self.onCrossClicked)
        self.accept(CIRCLE_BTN, self.onCircleClicked )

    def onCircleClicked(self):
        clicked_snd.play()
        self.commandAndDestroy(self.command)

    def onCrossClicked(self):
        cancel_snd.play()
        self.commandAndDestroy(self.cancelcommand)

    def commandAndDestroy(self, command):
        clicked_snd.play()
        seq = Sequence()
        seq.append(LerpScaleInterval(self.frame, 0.1, 0.1, startScale=1))
        seq.append(Func(self.ignoreAll))
        seq.append(Func(self.frame.destroy))
        seq.append(Func(command))
        seq.start()

class CharBarsLeft:

    def __init__(self, char):
        fbgtex = loader.loadTexture(GAME+'/textures/gui/face_background.png')
        fbgtex.setMagfilter(Texture.FTNearest)
        fbgtex.setMinfilter(Texture.FTNearest)

        self.fbgframe = DirectFrame(
            frameTexture = fbgtex, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( -v*32.0, v*32.0, -v*32.0, v*32.0 ),
        )
        self.fbgframe.setTransparency(True)
        self.fbgframe.setPos(-2, 0, -v*82)
        
        facetex = loader.loadTexture(GAME+'/textures/sprites/'+char['sprite']+'_face.png')
        facetex.setMagfilter(Texture.FTNearest)
        facetex.setMinfilter(Texture.FTNearest)
        
        self.face = DirectFrame(
            frameTexture = facetex, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( 0, v*32, 0, v*64 ),
            parent = self.fbgframe,
        )
        self.face.setPos(-v*(59-42), 0, -v*31)

        tex = loader.loadTexture(GAME+'/textures/gui/char_bars.png')
        tex.setMagfilter(Texture.FTNearest)
        tex.setMinfilter(Texture.FTNearest)
        
        self.frame = DirectFrame(
            frameTexture = tex, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( -v*64.0, v*64.0, -v*32.0, v*32.0 ),
            parent = self.fbgframe
        )
        self.frame.setPos(v*46, 0, -v*9)
        self.frame.setTransparency(True)

        infos = [
            { 'x': 16-3 , 'z':  16+9 , 'text': '%02d' % char['lv'] },
            { 'x': 48-3 , 'z':  16+9 , 'text': '%02d' % char['exp'] },
            { 'x': 18-3 , 'z':   2+9 , 'text': '%03d' % char['hp'] },
            { 'x': 37-3 , 'z':  -2+9 , 'text': '%03d' % char['hpmax'] },
            { 'x': 18-3 , 'z':  -9+9 , 'text': '%03d' % char['mp'] },
            { 'x': 37-3 , 'z': -13+9 , 'text': '%03d' % char['mpmax'] },
            { 'x': 18-3 , 'z': -20+9 , 'text': '%03d' % char['ct'] },
            { 'x': 37-3 , 'z': -24+9 , 'text': '100' },
        ]
        
        for info in infos:
            label = DirectLabel(
                text = info['text'],
                color = (1, 1, 1, 0),
                scale = scale,
                text_font = font3,
                text_fg = (1,1,1,1),
                text_align = TextNode.ALeft,
                parent = self.frame
            )
            label.setPos(v*info['x'], 0, v*info['z'])

        i1 = LerpPosInterval(self.fbgframe, 0.2, (-u*104,0,-u*82), (-2,0,-u*82))
        s = Sequence(i1)
        s.start()

    def hide(self):
        if self.fbgframe:
            i1 = LerpPosInterval(self.fbgframe, 0.2, (-2,0,-u*82), (-u*104,0,-u*82))
            i2 = Func( self.fbgframe.destroy )
            s = Sequence(i1,i2)
            s.start()

class CharBarsRight:

    def __init__(self, char):
        fbgtex = loader.loadTexture(GAME+'/textures/gui/face_background.png')
        fbgtex.setMagfilter(Texture.FTNearest)
        fbgtex.setMinfilter(Texture.FTNearest)

        self.fbgframe = DirectFrame(
            frameTexture = fbgtex, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( -v*32.0, v*32.0, -v*32.0, v*32.0 ),
        )
        self.fbgframe.setTransparency(True)
        self.fbgframe.setPos(2, 0, -v*82)
        
        facetex = loader.loadTexture(GAME+'/textures/sprites/'+char['sprite']+'_face.png')
        facetex.setMagfilter(Texture.FTNearest)
        facetex.setMinfilter(Texture.FTNearest)
        
        self.face = DirectFrame(
            frameTexture = facetex, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( 0, v*32, 0, v*64 ),
            parent = self.fbgframe,
        )
        self.face.setPos(-v*(59-42), 0, -v*31)

        tex = loader.loadTexture(GAME+'/textures/gui/char_bars.png')
        tex.setMagfilter(Texture.FTNearest)
        tex.setMinfilter(Texture.FTNearest)
        
        self.frame = DirectFrame(
            frameTexture = tex, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( -v*64.0, v*64.0, -v*32.0, v*32.0 ),
            parent = self.fbgframe
        )
        self.frame.setPos(-v*64, 0, v*7)
        self.frame.setTransparency(True)

        infos = [
            { 'x':   16 , 'z':   -29 , 'text': '%02d' % char['lv'] },
            { 'x':   48 , 'z':   -29 , 'text': '%02d' % char['exp'] },
            { 'x': 18-4 , 'z':   2+7 , 'text': '%03d' % char['hp'] },
            { 'x': 37-4 , 'z':  -2+7 , 'text': '%03d' % char['hpmax'] },
            { 'x': 18-4 , 'z':  -9+7 , 'text': '%03d' % char['mp'] },
            { 'x': 37-4 , 'z': -13+7 , 'text': '%03d' % char['mpmax'] },
            { 'x': 18-4 , 'z': -20+7 , 'text': '%03d' % char['ct'] },
            { 'x': 37-4 , 'z': -24+7 , 'text': '100' },
        ]
        
        for info in infos:
            label = DirectLabel(
                text = info['text'],
                color = (1, 1, 1, 0),
                scale = scale,
                text_font = font3,
                text_fg = (1,1,1,1),
                text_align = TextNode.ALeft,
                parent = self.frame
            )
            label.setPos(v*info['x'], 0, v*info['z'])

        i1 = LerpPosInterval(self.fbgframe, 0.2, (u*107,0,-u*82), (2,0,-u*82))
        s = Sequence(i1)
        s.start()

    def hide(self):
        if self.fbgframe:
            i1 = LerpPosInterval(self.fbgframe, 0.2, (2,0,-u*82), (u*107,0,-u*82))
            i2 = Func( self.fbgframe.destroy )
            s = Sequence(i1,i2)
            s.start()

class CharCard:

    def __init__(self, char):
        blacktex = loader.loadTexture(GAME+'/textures/gui/black.png')
        blacktex.setMagfilter(Texture.FTNearest)
        blacktex.setMinfilter(Texture.FTNearest)

        self.blackframe = DirectFrame(
                frameTexture = blacktex, 
                frameColor=(1, 1, 1, 1),
                frameSize = ( -2, 2, -v*64.0, v*64.0 ),
                sortOrder = -1,
        )
        self.blackframe.setTransparency(True)
        self.blackframe.setPos(0, 0, u*-82)

        tex = loader.loadTexture(GAME+'/textures/gui/char_card.png')
        tex.setMagfilter(Texture.FTNearest)
        tex.setMinfilter(Texture.FTNearest)

        self.frame = DirectFrame(
            frameTexture = tex, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( -v*64.0, v*64.0, -v*32.0, v*32.0 ),
        )
        self.frame.setTransparency(True)
        self.frame.setPos(2, 0, -u*85)

        self.name = DirectLabel(
            text = char['name'],
            color = (0,0,0,0),
            scale = regularscale,
            text_font = regularfont,
            text_fg = (1,1,1,1),
            text_align = TextNode.ALeft,
            parent = self.frame
        )
        self.name.setPos(-v*33, 0, v*12)

        self.name = DirectLabel(
            text = char['job'],
            color = (0,0,0,0),
            scale = regularscale,
            text_font = regularfont,
            text_fg = (1,1,1,1),
            text_align = TextNode.ALeft,
            parent = self.frame
        )
        self.name.setPos(-v*33, 0, -v*4)

        teamcolors = ['blue','red','green']
        ledtex = loader.loadTexture(GAME+'/textures/gui/led_'+teamcolors[int(char['team'])]+'.png')
        ledtex.setMagfilter(Texture.FTNearest)
        ledtex.setMinfilter(Texture.FTNearest)

        self.led = DirectFrame(
            frameTexture = ledtex, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( -.0625, .0625, -.0625, .0625 ),
            parent = self.frame
        )
        self.led.setTransparency(True)
        self.led.setPos(-v*49, 0, v*18)

        signs = ['aries','scorpio']
        signtex = loader.loadTexture(GAME+'/textures/gui/'+signs[int(char['sign'])]+'.png')
        signtex.setMagfilter(Texture.FTNearest)
        signtex.setMinfilter(Texture.FTNearest)

        self.sign = DirectFrame(
            frameTexture = signtex, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( -.125, .125, -.125, .125 ),
            parent = self.frame
        )
        self.sign.setTransparency(True)
        self.sign.setPos(-v*42, 0, -v*12)

        brlabel = DirectLabel(
            text = str(char['br']),
            color = (1, 1, 1, 0),
            scale = scale,
            text_font = font4,
            text_fg = (1,1,1,1),
            text_align = TextNode.ARight,
            parent = self.frame
        )
        brlabel.setPos(v*6, 0, -v*22)

        falabel = DirectLabel(
            text = str(char['fa']),
            color = (1, 1, 1, 0),
            scale = scale,
            text_font = font4,
            text_fg = (1,1,1,1),
            text_align = TextNode.ARight,
            parent = self.frame
        )
        falabel.setPos(v*45, 0, -v*22)

        i1 = LerpScaleInterval(self.blackframe, 0.1, (1,1,1), (1,1,0))
        i2 = LerpColorInterval(self.blackframe, 0.1, (1,1,1,1), (1,1,1,0))
        i3 = LerpPosInterval(  self.frame,      0.2, (u*67,0,-u*82), (2,0,-u*82))
        p1 = Parallel(i1,i2,i3)
        s = Sequence(p1)
        s.start()

    def hide(self):
        if self.frame:
            i1 = LerpScaleInterval(self.blackframe, 0.1, (1,1,0), (1,1,1))
            i2 = LerpColorInterval(self.blackframe, 0.1, (1,1,1,0), (1,1,1,1))
            i3 = LerpPosInterval(  self.frame,      0.2, (2,0,-u*82), (u*67,0,-u*82))
            p1 = Parallel(i1,i2,i3)
            i4 = Func( self.blackframe.destroy )
            i5 = Func( self.frame.destroy )
            s = Sequence(p1,i4,i5)
            s.start()

class ActionPreview(DirectObject.DirectObject):

    def __init__(self, char1, char2, damages, chance, command, cancelcommand):
        self.command = command
        self.cancelcommand = cancelcommand
    
        blacktex = loader.loadTexture(GAME+'/textures/gui/black.png')
        blacktex.setMagfilter(Texture.FTNearest)
        blacktex.setMinfilter(Texture.FTNearest)

        self.blackframe = DirectFrame(
                frameTexture = blacktex, 
                frameColor=(1, 1, 1, 1),
                frameSize = ( -2, 2, -v*64.0, v*64.0 ),
                sortOrder = -1,
        )
        self.blackframe.setTransparency(True)
        self.blackframe.setPos(0, 0, u*-82)
    
        fbgtex1 = loader.loadTexture(GAME+'/textures/gui/face_background.png')
        fbgtex1.setMagfilter(Texture.FTNearest)
        fbgtex1.setMinfilter(Texture.FTNearest)

        self.fbgframe1 = DirectFrame(
            frameTexture = fbgtex1, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( -v*32.0, v*32.0, -v*32.0, v*32.0 ),
        )
        self.fbgframe1.setTransparency(True)
        self.fbgframe1.setPos(-2, 0, -v*82)
        
        facetex1 = loader.loadTexture(GAME+'/textures/sprites/'+char1['sprite']+'_face.png')
        facetex1.setMagfilter(Texture.FTNearest)
        facetex1.setMinfilter(Texture.FTNearest)
        
        self.face1 = DirectFrame(
            frameTexture = facetex1, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( 0, v*32, 0, v*64 ),
            parent = self.fbgframe1,
        )
        self.face1.setPos(-v*(59-42), 0, -v*31)

        tex1 = loader.loadTexture(GAME+'/textures/gui/char_bars.png')
        tex1.setMagfilter(Texture.FTNearest)
        tex1.setMinfilter(Texture.FTNearest)
        
        self.frame1 = DirectFrame(
            frameTexture = tex1, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( -v*64.0, v*64.0, -v*32.0, v*32.0 ),
            parent = self.fbgframe1
        )
        self.frame1.setPos(v*46, 0, -v*9)
        self.frame1.setTransparency(True)

        atex = loader.loadTexture(GAME+'/textures/gui/action_preview_arrow.png')
        atex.setMagfilter(Texture.FTNearest)
        atex.setMinfilter(Texture.FTNearest)
        
        self.arrow = DirectFrame(
            frameTexture = atex, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( -v*8.0, v*8.0, -v*16.0, v*16.0 ),
            parent = self.fbgframe1
        )
        self.arrow.setPos(v*101.0, 0, v*1.0)
        self.arrow.setTransparency(True)

        infos = [
            { 'x': 16-4+15 , 'z':  16+9 , 'text': '%02d' % chance },
            { 'x': 18-4+15 , 'z':   2+9 , 'text': '%03d' % char1['hp'] },
            { 'x': 37-4+15 , 'z':  -2+9 , 'text': '%03d' % char1['hpmax'] },
            { 'x': 18-4+15 , 'z':  -9+9 , 'text': '%03d' % char1['mp'] },
            { 'x': 37-4+15 , 'z': -13+9 , 'text': '%03d' % char1['mpmax'] },
            { 'x': 18-4+15 , 'z': -20+9 , 'text': '%03d' % char1['ct'] },
            { 'x': 37-4+15 , 'z': -24+9 , 'text': '100' },
        ]
        
        for info in infos:
            label = DirectLabel(
                text = info['text'],
                color = (1, 1, 1, 0),
                scale = scale,
                text_font = font3,
                text_fg = (1,1,1,1),
                text_align = TextNode.ARight,
                parent = self.frame1
            )
            label.setPos(v*info['x'], 0, v*info['z'])

        fbgtex2 = loader.loadTexture(GAME+'/textures/gui/face_background.png')
        fbgtex2.setMagfilter(Texture.FTNearest)
        fbgtex2.setMinfilter(Texture.FTNearest)

        self.fbgframe2 = DirectFrame(
            frameTexture = fbgtex2, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( -v*32.0, v*32.0, -v*32.0, v*32.0 ),
        )
        self.fbgframe2.setTransparency(True)
        self.fbgframe2.setPos(2, 0, -v*82)

        facetex2 = loader.loadTexture(GAME+'/textures/sprites/'+char2['sprite']+'_face.png')
        facetex2.setMagfilter(Texture.FTNearest)
        facetex2.setMinfilter(Texture.FTNearest)
        
        self.face2 = DirectFrame(
            frameTexture = facetex2, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( 0, v*32, 0, v*64 ),
            parent = self.fbgframe2,
        )
        self.face2.setPos(-v*(59-42), 0, -v*31)

        tex2 = loader.loadTexture(GAME+'/textures/gui/char_bars.png')
        tex2.setMagfilter(Texture.FTNearest)
        tex2.setMinfilter(Texture.FTNearest)
        
        self.frame2 = DirectFrame(
            frameTexture = tex2, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( -v*64.0, v*64.0, -v*32.0, v*32.0 ),
            parent = self.fbgframe2
        )
        self.frame2.setPos(-v*64, 0, v*7)
        self.frame2.setTransparency(True)

        infos = [
            { 'x': 18-4 , 'z':   2+9 , 'text': '%03d' % char2['hp'] },
            { 'x': 37-4 , 'z':  -2+9 , 'text': '%03d' % char2['hpmax'] },
            { 'x': 18-4 , 'z':  -9+9 , 'text': '%03d' % char2['mp'] },
            { 'x': 37-4 , 'z': -13+9 , 'text': '%03d' % char2['mpmax'] },
            { 'x': 18-4 , 'z': -20+9 , 'text': '%03d' % char2['ct'] },
            { 'x': 37-4 , 'z': -24+9 , 'text': '100' },
        ]

        for info in infos:
            label = DirectLabel(
                text = info['text'],
                color = (1, 1, 1, 0),
                scale = scale,
                text_font = font3,
                text_fg = (1,1,1,1),
                text_align = TextNode.ALeft,
                parent = self.frame2
            )
            label.setPos(v*info['x'], 0, v*info['z'])

        s = Sequence(
            Parallel(
                LerpScaleInterval(self.blackframe, 0.1, (1,1,1), (1,1,0)),
                LerpColorInterval(self.blackframe, 0.1, (1,1,1,1), (1,1,1,0)),
                LerpPosInterval(   self.fbgframe1, 0.2, (-u*111,0,-u*82), (-2,0,-u*82)),
                LerpPosInterval(   self.fbgframe2, 0.2, ( u*109,0,-u*82), ( 2,0,-u*82)),
            ),
            Func( self.acceptAll ),
        ).start()

    def hide(self):
        if self.fbgframe1:
            s = Sequence(
                Parallel(
                    LerpScaleInterval(self.blackframe, 0.1, (1,1,0), (1,1,1)),
                    LerpColorInterval(self.blackframe, 0.1, (1,1,1,0), (1,1,1,1)),
                    LerpPosInterval(   self.fbgframe1, 0.2, (-2,0,-u*82), (u*111,0,-u*82)),
                    LerpPosInterval(   self.fbgframe2, 0.2, ( 2,0,-u*82), (u*109,0,-u*82)),
                ),
                Func( self.blackframe.destroy ),
                Func( self.fbgframe1.destroy ),
                Func( self.fbgframe2.destroy ),
            ).start()

    def acceptAll(self):
        self.accept(CROSS_BTN,  self.onCrossClicked)
        self.accept(CIRCLE_BTN, self.onCircleClicked)

    def onCircleClicked(self):
        clicked_snd.play()
        self.command()
        self.ignoreAll()

    def onCrossClicked(self):
        cancel_snd.play()
        self.hide()
        self.ignoreAll()
        self.cancelcommand()

class BrownOverlay(DirectObject.DirectObject):

    def __init__(self, textcallback, callback):
        
        self.callback = callback
        self.r = 20
        self.frames = [ [ None for y in range(self.r) ] for x in range(self.r) ]
        
        for x in range(self.r):
            for y in range(self.r):
                frame = DirectFrame(
                    color = (0,0,0,0),
                    frameSize = ( -1.0/self.r, 1.0/self.r, -1.0/self.r, 1.0/self.r ),
                    pos = (
                        (((float(x)/float(self.r))-.5)*2.0)+1.0/self.r,
                        0,
                        ((-(float(y)/float(self.r))+.5)*2.0)-1.0/self.r,
                    ),
                    parent = render2d,
                )
                frame.setTransparency(True)
                self.frames[x][y] = frame

                s = Sequence(
                    Wait(float(x+y)/40.0),
                    Parallel(
                        LerpHprInterval(frame, .125, (0,0,0), (0,0,90)),
                        LerpColorInterval(frame, .125, (.3,.22,.05,.5), (.3,.22,.04,0)),
                        LerpScaleInterval(frame, .25, 1, .01),
                    ),
                )
                if x == self.r-1 and y == self.r-1:
                    s.append(Func(lambda: textcallback(self.hide)))
                s.start()

    def hide(self):
        
        for x in range(self.r):
            for y in range(self.r):
                frame = self.frames[x][y]
                
                s = Sequence(
                    Wait(float(x+y)/40.0),
                    Parallel(
                        LerpHprInterval(frame, .125, (0,0,90), (0,0,0)),
                        LerpColorInterval(frame, .125, (.3,.22,.05,0), (.3,.22,.04,.5)),
                        LerpScaleInterval(frame, .25, .01, 1),
                    ),
                    Func(frame.destroy),
                )
                if x == self.r-1 and y == self.r-1:
                    s.append(Wait(1))
                    s.append(Func(self.callback))
                s.start()

class ConditionsForWinning(DirectObject.DirectObject):

    def __init__(self, callback):
        
        cfwtex = loader.loadTexture(GAME+'/textures/gui/conditions_for_winning.png')
        cfwtex.setMagfilter(Texture.FTNearest)
        cfwtex.setMinfilter(Texture.FTNearest)
        cfw = DirectFrame(
            color = (1,1,1,0),
            frameTexture = cfwtex,
            frameSize = ( -v*128.0, v*128.0, -v*16.0, v*16.0 ),
            pos = (v*20, 0, v*90),
        )
        cfw.setTransparency(True)

        daetex = loader.loadTexture(GAME+'/textures/gui/defeat_all_enemies.png')
        daetex.setMagfilter(Texture.FTNearest)
        daetex.setMinfilter(Texture.FTNearest)
        dae = DirectFrame(
            color = (1,1,1,0),
            frameTexture = daetex,
            frameSize = ( -v*128.0, v*128.0, -v*16.0, v*16.0 ),
            pos = (v*49, 0, v*60),
        )
        dae.setTransparency(True)

        readytex = loader.loadTexture(GAME+'/textures/gui/ready.png')
        readytex.setMagfilter(Texture.FTNearest)
        readytex.setMinfilter(Texture.FTNearest)
        ready = DirectFrame(
            color = (1,1,1,0),
            frameTexture = readytex,
            frameSize = ( -v*128.0, v*128.0, -v*16.0, v*16.0 ),
        )
        ready.setTransparency(True)

        s = Sequence(
            Wait(1),
            LerpColorInterval(cfw, .5, (1,1,1,1), (1,1,1,0)),
            Wait(.5),
            LerpColorInterval(dae, .5, (1,1,1,1), (1,1,1,0)),
            Wait(2),
            Parallel(
                LerpColorInterval(cfw, .5, (1,1,1,0), (1,1,1,1)),
                LerpColorInterval(dae, .5, (1,1,1,0), (1,1,1,1)),
            ),
            Func(cfw.destroy),
            Func(dae.destroy),
            LerpColorInterval(ready, 1, (1,1,1,1), (1,1,1,0)),
            Wait(2),
            LerpColorInterval(ready, 1, (1,1,1,0), (1,1,1,1)),
            Func(ready.destroy),
            Func(callback),
        ).start()

class Congratulations(DirectObject.DirectObject):

    def __init__(self, callback):
        
        ggtex = loader.loadTexture(GAME+'/textures/gui/congratulations.png')
        ggtex.setMagfilter(Texture.FTNearest)
        ggtex.setMinfilter(Texture.FTNearest)
        gg = DirectFrame(
            color = (1,1,1,0),
            frameTexture = ggtex,
            frameSize = ( -v*128.0, v*128.0, -v*16.0, v*16.0 ),
            pos = (v*0, 0, v*30),
        )
        gg.setTransparency(True)

        bctex = loader.loadTexture(GAME+'/textures/gui/battle_complete.png')
        bctex.setMagfilter(Texture.FTNearest)
        bctex.setMinfilter(Texture.FTNearest)
        bc = DirectFrame(
            color = (1,1,1,0),
            frameTexture = bctex,
            frameSize = ( -v*64.0, v*64.0, -v*16.0, v*16.0 ),
            pos = (v*0, 0, -v*30),
        )
        bc.setTransparency(True)

        s = Sequence(
            Wait(1),
            LerpColorInterval(gg, .5, (1,1,1,1), (1,1,1,0)),
            Wait(.5),
            LerpColorInterval(bc, .5, (1,1,1,1), (1,1,1,0)),
            Wait(2),
            Parallel(
                LerpColorInterval(gg, .5, (1,1,1,0), (1,1,1,1)),
                LerpColorInterval(bc, .5, (1,1,1,0), (1,1,1,1)),
            ),
            Func(gg.destroy),
            Func(bc.destroy),
            Func(callback),
        ).start()

class GameOver(DirectObject.DirectObject):

    def __init__(self, callback):
        
        gotex = loader.loadTexture(GAME+'/textures/gui/game_over.png')
        gotex.setMagfilter(Texture.FTNearest)
        gotex.setMinfilter(Texture.FTNearest)
        go = DirectFrame(
            color = (1,1,1,0),
            frameTexture = gotex,
            frameSize = ( -2, 2, -2, 2 ),
        )
        go.setTransparency(True)

        s = Sequence(
            LerpColorInterval(go, 3, (1,1,1,1), (1,1,1,0)),
            Wait(2),
            LerpColorInterval(go, 3, (0,0,0,1), (1,1,1,1)),
            Func(go.destroy),
            Func(callback),
        ).start()

class MapChooser(DirectObject.DirectObject):

    def __init__(self, maplist, parent, command, cancelcommand):
        self.parent = parent
        self.command = command
        self.cancelcommand = cancelcommand
        self.current = 0
        self.maplist = maplist

        loadingtexture = loader.loadTexture(GAME+'/textures/gui/now_loading.png')
        loadingtexture.setMagfilter(Texture.FTNearest)
        loadingtexture.setMinfilter(Texture.FTNearest)

        self.loadingframe = DirectFrame(
            frameTexture = loadingtexture,
            frameColor = (1, 1, 1, 1),
            frameSize = ( -.25, .25, -.0625, .0625 ),
            pos = (.9, 0, -.8),
            scale = 1.0,
        )
        self.loadingframe.setTransparency(True)

        for mapinfo in self.maplist:
            terrain = loader.loadModel(GAME+'/models/maps/'+mapinfo['model'])
            terrain.setTransparency(TransparencyAttrib.MAlpha)
            terrain.setScale( *[ x/25.0 for x in mapinfo['scale'] ] )
            terrain.setDepthWrite(True)
            terrain.setDepthTest(True)
            bbcenter = terrain.getBounds().getCenter()
            hprcontainer = NodePath("hprcontainer")
            recentrer = NodePath("recentrer")
            hprcontainer.setHpr(0,33,0)
            terrain.reparentTo(recentrer)
            terrain.setPos(-bbcenter[0], -bbcenter[1], -bbcenter[2]/2.0)
            recentrer.reparentTo(hprcontainer)
            mapinfo['recentrer'] = recentrer
            mapinfo['terrain'] = hprcontainer

        self.loadingframe.destroy()

        l1texture = loader.loadTexture(GAME+'/textures/gui/L1.png')
        l1texture.setMagfilter(Texture.FTNearest)
        l1texture.setMinfilter(Texture.FTNearest)

        self.l1frame = DirectFrame(
            frameTexture = l1texture,
            frameColor = (1, 1, 1, 1),
            frameSize = ( -.125, .125, -.0625, .0625 ),
            pos = (-.9, 0, .8),
            scale = 1.0,
        )
        self.l1frame.setTransparency(True)

        r1texture = loader.loadTexture(GAME+'/textures/gui/R1.png')
        r1texture.setMagfilter(Texture.FTNearest)
        r1texture.setMinfilter(Texture.FTNearest)

        self.r1frame = DirectFrame(
            frameTexture = r1texture,
            frameColor = (1, 1, 1, 1),
            frameSize = ( -.125, .125, -.0625, .0625 ),
            pos = (.9, 0, .8),
            scale = 1.0,
        )
        self.r1frame.setTransparency(True)

        starttexture = loader.loadTexture(GAME+'/textures/gui/start_end.png')
        starttexture.setMagfilter(Texture.FTNearest)
        starttexture.setMinfilter(Texture.FTNearest)

        self.startframe = DirectFrame(
            frameTexture = starttexture,
            frameColor = (1, 1, 1, 1),
            frameSize = ( -.25, .25, -.0625, .0625 ),
            pos = (0, 0, -.8),
            scale = 1.0,
        )
        self.startframe.setTransparency(True)
        
        seq = Sequence(
            Parallel(
                LerpPosInterval(self.l1frame, 0.25, (-.9, 0, .8), (-.9, 0, 1.0)),
                LerpPosInterval(self.r1frame, 0.25, ( .9, 0, .8), ( .9, 0, 1.0)),
                LerpPosInterval(self.startframe, 0.25, (0, 0, -.8), (0, 0, -1.0)),
                Func( self.maplist[self.current]['terrain'].reparentTo, self.parent ),
                LerpColorInterval(self.maplist[self.current]['terrain'], 0.25, (1,1,1,1), (1,1,1,0)),
            ),
            Func( taskMgr.add, self.mapRotationTask, 'mapRotationTask' ),
            Func( self.acceptAll ),
        ).start()

    def acceptAll(self):
        self.accept(CROSS_BTN,        self.onCrossClicked)
        self.accept(START_BTN,        self.onStartClicked)
        self.accept(L1_BTN,           self.onL1Clicked)
        self.accept(R1_BTN,           self.onR1Clicked)
        self.accept(L1_BTN+"-repeat", self.onL1Clicked)
        self.accept(L1_BTN+"-repeat", self.onR1Clicked)

    def onCrossClicked(self):
        cancel_snd.play()
        self.commandAndDestroy(self.cancelcommand)

    def onStartClicked(self):
        clicked_snd.play()
        self.commandAndDestroy( lambda: self.command( self.maplist[self.current]['name'] ) )

    def commandAndDestroy(self, command):
        self.ignoreAll()

        seq = Sequence(
            Func( taskMgr.remove, 'mapRotationTask' ),
            Wait( 0.5 ),
            Parallel(
                LerpPosInterval(self.l1frame, 0.25, (-.9, 0, 1.0), (-.9, 0, .8)),
                LerpPosInterval(self.r1frame, 0.25, ( .9, 0, 1.0), ( .9, 0, .8)),
                LerpPosInterval(self.startframe, 0.25, (0, 0, -1.0), (0, 0, -.8)),
                LerpColorInterval(self.maplist[self.current]['terrain'], 0.25, (1,1,1,0), (1,1,1,1)),
            ),
            Func( self.l1frame.destroy ),
            Func( self.r1frame.destroy ),
            Func( self.startframe.destroy ),
            Func( command ),
            Func( self.unloadTerrains ),
        ).start()

    def unloadTerrains(self):
        for mapinfo in self.maplist:
            mapinfo['terrain'].removeNode()
            loader.unloadModel(GAME+'/models/maps/'+mapinfo['model'])
        del self.maplist

    def onR1Clicked(self):

        self.previous = self.current
        self.current = self.current - 1
        if self.current < 0:
            self.current = len(self.maplist) - 1

        seq = Sequence(
            Func( self.ignoreAll ),
            Func( self.maplist[self.current]['terrain'].reparentTo, self.parent ),
            Parallel(
                #LerpScaleInterval(self.maplist[self.previous]['terrain'], 0.25, 0.1, startScale=1.0 ),
                LerpColorInterval(self.maplist[self.previous]['terrain'], 0.25, (1,1,1,0), (1,1,1,1)),
                LerpPosInterval(  self.maplist[self.previous]['terrain'], 0.25, (-25,25,0), (0,0,0)),
                #LerpHprInterval(  self.maplist[self.previous]['terrain'], 0.25, (90,0,0), (0,0,0)),
                #LerpScaleInterval(self.maplist[self.current]['terrain'],  0.25, 1.0, startScale=0.1 ),
                LerpColorInterval(self.maplist[self.current]['terrain'],  0.25, (1,1,1,1), (1,1,1,0)),
                LerpPosInterval(  self.maplist[self.current]['terrain'],  0.25, (0,0,0), (25,-25,0)),
                #LerpHprInterval(  self.maplist[self.current]['terrain'], 0.25, (180,0,0), (90,0,0)),
            ),
            Func( self.maplist[self.previous]['terrain'].detachNode ),
            Func( self.acceptAll ),
            Func( hover_snd.play ),
        ).start()

    def onL1Clicked(self):

        self.previous = self.current
        self.current = self.current + 1
        if self.current > len(self.maplist) - 1:
            self.current = 0

        seq = Sequence(
            Func( self.ignoreAll ),
            Func( self.maplist[self.current]['terrain'].reparentTo, self.parent ),
            Parallel(
                #LerpScaleInterval(self.maplist[self.previous]['terrain'], 0.25, 0.1, startScale=1.0 ),
                LerpColorInterval(self.maplist[self.previous]['terrain'], 0.25, (1,1,1,0), (1,1,1,1)),
                LerpPosInterval(  self.maplist[self.previous]['terrain'], 0.25, (25,-25,0), (0,0,0)),
                #LerpHprInterval(  self.maplist[self.previous]['terrain'], 0.25, (90,0,0), (0,0,0)),
                #LerpScaleInterval(self.maplist[self.current]['terrain'],  0.25, 1.0, startScale=0.1 ),
                LerpColorInterval(self.maplist[self.current]['terrain'],  0.25, (1,1,1,1), (1,1,1,0)),
                LerpPosInterval(  self.maplist[self.current]['terrain'],  0.25, (0,0,0), (-25,25,0)),
                #LerpHprInterval(  self.maplist[self.current]['terrain'], 0.25, (180,0,0), (90,0,0)),
            ),
            Func( self.maplist[self.previous]['terrain'].detachNode ),
            Func( self.acceptAll ),
            Func( hover_snd.play ),
        ).start()

    def mapRotationTask(self, task):
        h = task.time * 30
        self.maplist[self.current]['recentrer'].setHpr(h,0,0)
        return Task.cont

