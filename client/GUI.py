from Config import *
import direct.directbase.DirectStart
from direct.showbase import DirectObject
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.DirectGui import *
from direct.task import Task
from direct.actor import Actor
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
import Sprite
import functools
from WindowNodeDrawer import WindowNodeDrawer
from BarNodeDrawer import Bar

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
whitefont = loader.loadFont(GAME+'/fonts/fftwhite')
smwhitefont = loader.loadFont(GAME+'/fonts/fftwhite-small-caps')

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

class Blueprint(DirectObject.DirectObject):

    def __init__(self, image):

        tex = loader.loadTexture(GAME+'/textures/blueprints/'+image+'.png')
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
        
        self.frame = DirectFrame(
            frameColor = (1, 1, 1, .25),
            frameSize = ( -v*56, v*56, -v*22, v*22 ),
            pos = (v*10, 0, -v*0),
            geom = WindowNodeDrawer(112, 44, 'shadowed', 'Login'),
        )
        self.frame.setTransparency(True)

        self.loginLabel = DirectLabel(
            text = 'Username:',
            color = (0,0,0,0),
            scale = regularscale,
            text_font = regularfont,
            text_fg = (1,1,1,1),
            text_align = TextNode.ALeft,
            parent = self.frame,
        )
        self.loginLabel.setPos(-v*50, 0, v*4)

        self.loginEntry = DirectEntry(
            color = (0,0,0,0),
            scale = regularscale,
            numLines = 1,
            focus = 1,
            text_font = regularfont,
            text_fg = (1,1,1,1),
            parent = self.frame
        )
        self.loginEntry.setPos(-v*6, 0, v*4)

        self.passwordLabel = DirectLabel(
            text = 'Password:',
            color = (0,0,0,0),
            scale = regularscale,
            text_font = regularfont,
            text_fg = (1,1,1,1),
            text_align = TextNode.ALeft,
            parent = self.frame,
        )
        self.passwordLabel.setPos(-v*50, 0, -v*12)

        self.passwordEntry = DirectEntry(
            color = (0,0,0,0),
            scale = regularscale,
            numLines = 1,
            text_font = regularfont,
            text_fg = (1,1,1,1),
            obscured = True,
            parent = self.frame,
        )
        self.passwordEntry.setPos(-v*6, 0, -v*12)

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
        connectButton.setPos(v*37, 0, -v*40)

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
                text  = (str(len(parties[key]['players']))+'/'+str(len(parties[key]['map']['tilesets'])), "Join", "Join", "Full"),
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

            if len(parties[key]['players']) >= len(parties[key]['map']['tilesets']):
                buttons[key]['state'] = DGG.DISABLED

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

# Display an help message, the player can confirm or cancel
class Help(DirectObject.DirectObject):

    def __init__(self, x, y, w, h, style, title, message, command, cancelcommand):

        self.command = command
        self.cancelcommand = cancelcommand

        self.frame = DirectFrame(
            frameColor = (1, 1, 1, 0),
            frameSize = ( -v*w/2.0, v*w/2.0, -v*h/2.0, v*h/2.0 ),
            pos = (v*x, 0, v*y),
            geom = WindowNodeDrawer(w, h, style, title),
            scale=0.1,
        )
        self.frame.setTransparency(True)

        messageLabel = DirectLabel(
            color = (0,0,0,0),
            text = message,
            scale = regularscale,
            text_font = regularfont,
            text_fg = (1,1,1,1),
            text_align = TextNode.ALeft,
            parent = self.frame,
            pos = (-v*(w/2-6), 0, v*(h/2-17))
        )
        
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
        self.face.setPos(-v*17, 0, -v*31)
        
        self.frame = DirectFrame(
            frameColor=(1, 1, 1, 0),
            frameSize = ( -v*64.0, v*64.0, -v*32.0, v*32.0 ),
            parent = self.fbgframe
        )
        self.frame.setPos(v*46, 0, -v*9)
        self.frame.setTransparency(True)

        bar = Bar(bar='bar-1')
        bar.updateTo(int(float(char['hp'])/float(char['hpmax'])*100))
        self.hpbar = DirectFrame(
            frameColor=(1, 1, 1, 1),
            frameSize=(0, 0, 0, 0), 
            parent = self.fbgframe,
            geom = bar.container,
            pos = (v*24, 0, -v*2),
        )
        self.hpbar.setTransparency(True)

        bar = Bar(bar='bar-2')
        bar.updateTo(int(float(char['mp'])/float(char['mpmax'])*100))
        self.mpbar = DirectFrame(
            frameColor=(1, 1, 1, 1),
            frameSize=(0, 0, 0, 0), 
            parent = self.fbgframe,
            geom = bar.container,
            pos = (v*24, 0, -v*13),
        )
        self.mpbar.setTransparency(True)

        bar = Bar(bar='bar-3')
        bar.updateTo(int(char['ct']))
        self.ctbar = DirectFrame(
            frameColor=(1, 1, 1, 1),
            frameSize=(0, 0, 0, 0), 
            parent = self.fbgframe,
            geom = bar.container,
            pos = (.20, 0, -.20)
        )
        self.ctbar.setTransparency(True)

        infos = [
            { 'x':  12, 'z':  23, 'text':  '%02d' % char['lv']   , 'font':   whitefont },
            { 'x':  43, 'z':  23, 'text':  '%02d' % char['exp']  , 'font':   whitefont },
            { 'x':  15, 'z':   9, 'text':  '%03d' % char['hp']   , 'font':   whitefont },
            { 'x':  28, 'z':   5, 'text': '/%03d' % char['hpmax'], 'font':   whitefont },
            { 'x':  15, 'z':  -2, 'text':  '%03d' % char['mp']   , 'font':   whitefont },
            { 'x':  28, 'z':  -6, 'text': '/%03d' % char['mpmax'], 'font':   whitefont },
            { 'x':  15, 'z': -13, 'text':  '%03d' % char['ct']   , 'font':   whitefont },
            { 'x':  28, 'z': -17, 'text':  '/100'                , 'font':   whitefont },
            { 'x': -33, 'z':   8, 'text':    'Hp'                , 'font': smwhitefont },
            { 'x': -33, 'z':  -3, 'text':    'Mp'                , 'font': smwhitefont },
            { 'x': -33, 'z': -13, 'text':    'Ct'                , 'font': smwhitefont },
            { 'x':   0, 'z':  23, 'text':   'Lv.'                , 'font': smwhitefont },
            { 'x':  27, 'z':  23, 'text':  'Exp.'                , 'font': smwhitefont },
        ]
        
        for info in infos:
            label = DirectLabel(
                text = info['text'],
                color = (1, 1, 1, 0),
                scale = scale,
                text_font = info['font'],
                text_fg = (1, 1, 1, 1),
                text_align = TextNode.ALeft,
                parent = self.frame,
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
        
        self.frame = DirectFrame(
            frameColor=(1, 1, 1, 0),
            frameSize = ( -v*64.0, v*64.0, -v*32.0, v*32.0 ),
            parent = self.fbgframe
        )
        self.frame.setPos(-v*64, 0, v*7)
        self.frame.setTransparency(True)

        bar = Bar(bar='bar-1')
        bar.updateTo(int(float(char['hp'])/float(char['hpmax'])*100))
        self.hpbar = DirectFrame(
            frameColor=(1, 1, 1, 1),
            frameSize=(0,0,0,0),
            parent = self.fbgframe,
            geom = bar.container,
            pos = (-.72, 0, .12),
        )
        self.hpbar.setTransparency(True)
        
        bar = Bar(bar='bar-2')
        bar.updateTo(int(float(char['mp'])/float(char['mpmax'])*100))
        self.mpbar = DirectFrame(
            frameColor=(1, 1, 1, 1),
            frameSize=(0,0,0,0),
            parent = self.fbgframe,
            geom = bar.container,
            pos = (-.72, 0, .03),
        )
        self.mpbar.setTransparency(True)
        
        bar = Bar(bar='bar-3')
        bar.updateTo(int(char['ct']))
        self.ctbar = DirectFrame(
            frameColor=(1, 1, 1, 1),
            frameSize=(0,0,0,0),
            parent = self.fbgframe,
            geom = bar.container,
            pos = (-.72, 0, -.07),
        )
        self.ctbar.setTransparency(True)

        infos = [
            { 'x':   16, 'z': -29, 'text':  '%02d' % char['lv']   , 'font':   whitefont },
            { 'x':   48, 'z': -29, 'text':  '%02d' % char['exp']  , 'font':   whitefont },
            { 'x':   14, 'z':   9, 'text':  '%03d' % char['hp']   , 'font':   whitefont },
            { 'x':   28, 'z':   5, 'text': '/%03d' % char['hpmax'], 'font':   whitefont },
            { 'x':   14, 'z':  -2, 'text':  '%03d' % char['mp']   , 'font':   whitefont },
            { 'x':   28, 'z':  -6, 'text': '/%03d' % char['mpmax'], 'font':   whitefont },
            { 'x':   14, 'z': -13, 'text':  '%03d' % char['ct']   , 'font':   whitefont },
            { 'x':   28, 'z': -17, 'text':  '/100'                , 'font':   whitefont },            
            { 'x':  -33, 'z':   8, 'text':    'Hp'                , 'font': smwhitefont },
            { 'x':  -33, 'z':   3, 'text':    'Mp'                , 'font': smwhitefont },
            { 'x':  -33, 'z': -13, 'text':    'Ct'                , 'font': smwhitefont },
            { 'x':    2, 'z': -29, 'text':   'Lv.'                , 'font': smwhitefont },
            { 'x':   29, 'z': -29, 'text':  'Exp.'                , 'font': smwhitefont },
        ]
        
        for info in infos:
            label = DirectLabel(
                text = info['text'],
                color = (1, 1, 1, 0),
                scale = scale,
                text_font = info['font'],
                text_fg = (1,1,1,1),
                text_align = TextNode.ALeft,
                parent = self.frame,
                sortOrder = 100
            )
            label.setPos(v*info['x'], -1, v*info['z'])

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

class Formation(DirectObject.DirectObject):

    def __init__(self, parent, tileset, chars, command):
    
        self.tileset = tileset
        self.chars = chars
        self.current = 0
        self.char = self.chars[self.current]
        self.direction = self.tileset['direction']
        self.capacity = self.tileset['capacity']
        self.remaining = self.capacity
        self.command = command
        self.sprites = [ [ None for y in range(5) ] for x in range(5) ]

        tex0 = loader.loadTexture(GAME+'/textures/gui/frm0.png')
        tex0.setMagfilter(Texture.FTNearest)
        tex0.setMinfilter(Texture.FTNearest)

        tex1 = loader.loadTexture(GAME+'/textures/gui/frm1.png')
        tex1.setMagfilter(Texture.FTNearest)
        tex1.setMinfilter(Texture.FTNearest)

        self.hprcontainer = parent.attachNewNode('hprcontainer')
        self.hprcontainer.setHpr(0,30,0)
        self.hprcontainer.setScale(0.235)
        self.hprcontainer.setPos(0,0,-.415)
        self.hprcontainer.setDepthWrite(True)
        self.hprcontainer.setDepthTest(True)

        self.root = NodePath("root")
        self.root.setHpr(-45,0,0)
        self.root.reparentTo(self.hprcontainer)

        self.tiles = [ [ {} for y in range(5) ] for x in range(5) ]
        for y,l in enumerate(self.tileset['maping']):
            y = 4-y
            for x,t in enumerate(l):
                self.tiles[x][y]['coords'] = t
                self.tiles[x][y]['char'] = None
                self.tiles[x][y]['model'] = loader.loadModel(GAME+"/models/slopes/flat")
                self.tiles[x][y]['model'].setTexture(tex0)
                self.tiles[x][y]['model'].setColor(1,1,1,1)
                self.tiles[x][y]['model'].setTransparency(TransparencyAttrib.MAlpha)
                self.tiles[x][y]['model'].reparentTo(self.root)
                self.tiles[x][y]['model'].setPos((x-2, y-2, 0))

                if t:
                    self.tiles[x][y]['model'].setTexture(tex1)
                    self.tiles[x][y]['model'].setPos((x-2, y-2, .33))
                else:
                    self.tiles[x][y]['model'].setTexture(tex0)                

        l1texture = loader.loadTexture(GAME+'/textures/gui/L1.png')
        l1texture.setMagfilter(Texture.FTNearest)
        l1texture.setMinfilter(Texture.FTNearest)

        self.l1frame = DirectFrame(
            frameTexture = l1texture,
            frameColor = (1, 1, 1, 0),
            frameSize = ( -v*16, v*16, -v*8, v*8 ),
            pos = (-v*104, 0, v*100),
            scale = 1.0,
        )
        self.l1frame.setTransparency(True)

        r1texture = loader.loadTexture(GAME+'/textures/gui/R1.png')
        r1texture.setMagfilter(Texture.FTNearest)
        r1texture.setMinfilter(Texture.FTNearest)

        self.r1frame = DirectFrame(
            frameTexture = r1texture,
            frameColor = (1, 1, 1, 0),
            frameSize = ( -v*16, v*16, -v*8, v*8 ),
            pos = (v*109, 0, v*100),
            scale = 1.0,
        )
        self.r1frame.setTransparency(True)

        searchtexture = loader.loadTexture(GAME+'/textures/gui/search_btn.png')
        searchtexture.setMagfilter(Texture.FTNearest)
        searchtexture.setMinfilter(Texture.FTNearest)

        self.searchframe = DirectFrame(
            frameTexture = searchtexture,
            frameColor = (1, 1, 1, 0),
            frameSize = ( -v*32, v*32, -v*8, v*8 ),
            pos = (-v*58, 0, -v*100),
            scale = 1.0,
        )
        self.searchframe.setTransparency(True)

        statustexture = loader.loadTexture(GAME+'/textures/gui/status_btn.png')
        statustexture.setMagfilter(Texture.FTNearest)
        statustexture.setMinfilter(Texture.FTNearest)

        self.statusframe = DirectFrame(
            frameTexture = statustexture,
            frameColor = (1, 1, 1, 0),
            frameSize = ( -v*32, v*32, -v*8, v*8 ),
            pos = (-v*0, 0, -v*100),
            scale = 1.0,
        )
        self.statusframe.setTransparency(True)

        starttexture = loader.loadTexture(GAME+'/textures/gui/start_end.png')
        starttexture.setMagfilter(Texture.FTNearest)
        starttexture.setMinfilter(Texture.FTNearest)

        self.startframe = DirectFrame(
            frameTexture = starttexture,
            frameColor = (1, 1, 1, 0),
            frameSize = ( -v*32, v*32, -v*8, v*8 ),
            pos = (v*61, 0, -v*100),
            scale = 1.0,
        )
        self.startframe.setTransparency(True)

        squadtexture0 = loader.loadTexture(GAME+'/textures/gui/squad_lbl0.png')
        squadtexture0.setMagfilter(Texture.FTNearest)
        squadtexture0.setMinfilter(Texture.FTNearest)

        self.squadframe = DirectFrame(
            frameTexture = squadtexture0,
            frameColor = (1, 1, 1, 0),
            frameSize = ( -v*32, v*32, -v*8, v*8 ),
            pos = (-v*96, 0, v*23),
            scale = 1.0,
        )
        self.squadframe.setTransparency(True)

        capacitytexture = loader.loadTexture(GAME+'/textures/gui/capacity_lbl.png')
        capacitytexture.setMagfilter(Texture.FTNearest)
        capacitytexture.setMinfilter(Texture.FTNearest)

        self.capacityframe = DirectFrame(
            frameTexture = capacitytexture,
            frameColor = (1, 1, 1, 0),
            frameSize = ( -v*32, v*32, -v*8, v*8 ),
            pos = (-v*96, 0, v*7),
            scale = 1.0,
        )
        self.capacityframe.setTransparency(True)

        remainingtexture = loader.loadTexture(GAME+'/textures/gui/remaining_lbl.png')
        remainingtexture.setMagfilter(Texture.FTNearest)
        remainingtexture.setMinfilter(Texture.FTNearest)

        self.remainingframe = DirectFrame(
            frameTexture = remainingtexture,
            frameColor = (1, 1, 1, 0),
            frameSize = ( -v*32, v*32, -v*8, v*8 ),
            pos = (-v*94, 0, -v*9),
            scale = 1.0,
        )
        self.remainingframe.setTransparency(True)

        # Cursor stuff
        self.curtex = loader.loadTexture(GAME+'/textures/cursor.png')
        self.curtex.setMagfilter(Texture.FTNearest)
        self.curtex.setMinfilter(Texture.FTNearest)
        self.cux = 2
        self.cuy = 2
        self.cursor = loader.loadModel(GAME+'/models/slopes/flat')
        self.cursor.reparentTo(self.root)
        self.cursor.setPos(0, 0, .33+0.025)
        self.cursor.setTransparency(TransparencyAttrib.MAlpha)
        self.cursor.setColor(1, 1, 1, 1)
        self.cursor.setTexture(self.curtex)

        fbgtex = loader.loadTexture(GAME+'/textures/gui/face_background.png')
        fbgtex.setMagfilter(Texture.FTNearest)
        fbgtex.setMinfilter(Texture.FTNearest)

        self.fbgframe = DirectFrame(
            frameTexture = fbgtex, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( -v*32.0, v*32.0, -v*32.0, v*32.0 ),
        )
        self.fbgframe.setTransparency(True)
        self.fbgframe.setPos(-v*97, 0, v*61)

        facetex = loader.loadTexture(GAME+'/textures/sprites/'+self.char['sprite']+'_face.png')
        facetex.setMagfilter(Texture.FTNearest)
        facetex.setMinfilter(Texture.FTNearest)

        self.face = DirectFrame(
            frameTexture = facetex, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( 0, v*32, 0, v*64 ),
            parent = self.fbgframe,
        )
        self.face.setPos(-v*(59-42), 0, -v*31)

        barstex = loader.loadTexture(GAME+'/textures/gui/char_bars.png')
        barstex.setMagfilter(Texture.FTNearest)
        barstex.setMinfilter(Texture.FTNearest)

        self.barsframe = DirectFrame(
            frameTexture = barstex, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( -v*64.0, v*64.0, -v*32.0, v*32.0 ),
            parent = self.fbgframe
        )
        self.barsframe.setPos(v*46, 0, -v*9)
        self.barsframe.setTransparency(True)

        infos = [
            { 'x':   -2 , 'z':    25 , 'text': '%02d' % self.char['lv'] },
            { 'x':   30 , 'z':    25 , 'text': '%02d' % self.char['exp'] },
            { 'x': 18-4 , 'z':   2+9 , 'text': '%03d' % self.char['hp'] },
            { 'x': 37-4 , 'z':  -2+9 , 'text': '%03d' % self.char['hpmax'] },
            { 'x': 18-4 , 'z':  -9+9 , 'text': '%03d' % self.char['mp'] },
            { 'x': 37-4 , 'z': -13+9 , 'text': '%03d' % self.char['mpmax'] },
            { 'x': 18-4 , 'z': -20+9 , 'text': '---' },
            { 'x': 37-4 , 'z': -24+9 , 'text': '---' },
        ]

        self.labels = [ None for i in infos ]
        for i,info in enumerate(infos):
            self.labels[i] = DirectLabel(
                text = info['text'],
                color = (1, 1, 1, 0),
                scale = scale,
                text_font = font3,
                text_fg = (1,1,1,1),
                text_align = TextNode.ALeft,
                parent = self.barsframe
            )
            self.labels[i].setPos(v*info['x'], 0, v*info['z'])

        cardtex = loader.loadTexture(GAME+'/textures/gui/char_card.png')
        cardtex.setMagfilter(Texture.FTNearest)
        cardtex.setMinfilter(Texture.FTNearest)

        self.cardframe = DirectFrame(
            frameTexture = cardtex, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( -v*64.0, v*64.0, -v*32.0, v*32.0 ),
        )
        self.cardframe.setTransparency(True)
        self.cardframe.setPos(v*63, 0, u*65)

        self.name = DirectLabel(
            text = self.char['name'],
            color = (0,0,0,0),
            scale = regularscale,
            text_font = regularfont,
            text_fg = (1,1,1,1),
            text_align = TextNode.ALeft,
            parent = self.cardframe
        )
        self.name.setPos(-v*33, 0, v*12)

        self.job = DirectLabel(
            text = self.char['job'],
            color = (0,0,0,0),
            scale = regularscale,
            text_font = regularfont,
            text_fg = (1,1,1,1),
            text_align = TextNode.ALeft,
            parent = self.cardframe
        )
        self.job.setPos(-v*33, 0, -v*4)

        teamcolors = ['blue','red','green']
        ledtex = loader.loadTexture(GAME+'/textures/gui/led_'+teamcolors[int(self.char['team'])]+'.png')
        ledtex.setMagfilter(Texture.FTNearest)
        ledtex.setMinfilter(Texture.FTNearest)

        self.led = DirectFrame(
            frameTexture = ledtex, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( -.0625, .0625, -.0625, .0625 ),
            parent = self.cardframe
        )
        self.led.setTransparency(True)
        self.led.setPos(-v*49, 0, v*18)

        signs = ['aries','scorpio']
        signtex = loader.loadTexture(GAME+'/textures/gui/'+signs[int(self.char['sign'])]+'.png')
        signtex.setMagfilter(Texture.FTNearest)
        signtex.setMinfilter(Texture.FTNearest)

        self.sign = DirectFrame(
            frameTexture = signtex, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( -.125, .125, -.125, .125 ),
            parent = self.cardframe
        )
        self.sign.setTransparency(True)
        self.sign.setPos(-v*42, 0, -v*12)

        self.brlabel = DirectLabel(
            text = str(self.char['br']),
            color = (1, 1, 1, 0),
            scale = scale,
            text_font = font4,
            text_fg = (1,1,1,1),
            text_align = TextNode.ARight,
            parent = self.cardframe
        )
        self.brlabel.setPos(v*6, 0, -v*22)

        self.falabel = DirectLabel(
            text = str(self.char['fa']),
            color = (1, 1, 1, 0),
            scale = scale,
            text_font = font4,
            text_fg = (1,1,1,1),
            text_align = TextNode.ARight,
            parent = self.cardframe
        )
        self.falabel.setPos(v*45, 0, -v*22)
        
        for char in self.chars:
            char['placed'] = False

        seq = Sequence(
            Parallel(
                LerpPosInterval(  self.hprcontainer,   .5, (0,0,-.415), (0,0,-2)),
                LerpPosInterval(  self.cardframe,      .5, (v*63,0,u*65), (v*63,0,2)),
                LerpPosInterval(  self.fbgframe,       .5, (-v*97,0,v*61), (-v*97,0,2)),
            ),
            Parallel(
                LerpColorInterval(self.l1frame,        .5, (1,1,1,1), (1,1,1,0)),
                LerpColorInterval(self.r1frame,        .5, (1,1,1,1), (1,1,1,0)),
                LerpColorInterval(self.squadframe,     .5, (1,1,1,1), (1,1,1,0)),
                LerpColorInterval(self.capacityframe,  .5, (1,1,1,1), (1,1,1,0)),
                LerpColorInterval(self.remainingframe, .5, (1,1,1,1), (1,1,1,0)),
                LerpColorInterval(self.searchframe,    .5, (.75,.75,.75,1), (1,1,1,0)),
                LerpColorInterval(self.statusframe,    .5, (.75,.75,.75,1), (1,1,1,0)),
                LerpColorInterval(self.startframe,     .5, (.75,.75,.75,1), (1,1,1,0)),
            ),
            Func( self.updateButtons ),
            Func( self.acceptAll ),
            Func( self.updateChar ),
        ).start()

    def acceptAll(self):
        self.accept("arrow_up", lambda: self.onArrowClicked('up'))
        self.accept("arrow_down", lambda: self.onArrowClicked('down'))
        self.accept("arrow_left", lambda: self.onArrowClicked('left'))
        self.accept("arrow_right", lambda: self.onArrowClicked('right'))
        self.accept("arrow_up-repeat", lambda: self.onArrowClicked('up'))
        self.accept("arrow_down-repeat", lambda: self.onArrowClicked('down'))
        self.accept("arrow_left-repeat", lambda: self.onArrowClicked('left'))
        self.accept("arrow_right-repeat", lambda: self.onArrowClicked('right'))
        self.accept(L1_BTN,           lambda: self.updateChar(-1))
        self.accept(R1_BTN,           lambda: self.updateChar(+1))
        self.accept(L1_BTN+"-repeat", lambda: self.updateChar(-1))
        self.accept(R1_BTN+"-repeat", lambda: self.updateChar(+1))
        self.accept(CIRCLE_BTN, self.onCircleClicked)
        self.accept(TRIANGLE_BTN, self.onTriangleClicked)
        self.accept(START_BTN, self.onStartClicked)

    def updateChar(self, delta=0, current=None):
        if current != None:
            self.current = current
        else:
            self.current = self.current + delta
            if self.current == len(self.chars):
                self.current = 0
            elif self.current == -1:
                self.current = len(self.chars)-1
        self.char = self.chars[self.current]

        self.labels[0]['text'] = '%02d' % self.char['lv']
        self.labels[1]['text'] = '%02d' % self.char['exp']
        self.labels[2]['text'] = '%03d' % self.char['hpmax']
        self.labels[3]['text'] = '%03d' % self.char['hpmax']
        self.labels[4]['text'] = '%03d' % self.char['mpmax']
        self.labels[5]['text'] = '%03d' % self.char['mpmax']

        self.name['text'] = self.char['name']
        self.job['text']  = self.char['job']
        self.brlabel['text']= str(self.char['br'])
        self.falabel['text']= str(self.char['fa'])

        facetex = loader.loadTexture(GAME+'/textures/sprites/'+self.char['sprite']+'_face.png')
        facetex.setMagfilter(Texture.FTNearest)
        facetex.setMinfilter(Texture.FTNearest)
        self.face['frameTexture'] = facetex

        signs = ['aries','scorpio']
        signtex = loader.loadTexture(GAME+'/textures/gui/'+signs[int(self.char['sign'])]+'.png')
        signtex.setMagfilter(Texture.FTNearest)
        signtex.setMinfilter(Texture.FTNearest)
        self.sign['frameTexture'] = signtex

        if self.char['placed']:
            color = [.7,.7,.9,1]
        else:
            color = [1,1,1,1]

        self.cardframe['frameColor'] = color
        self.led['frameColor'] = color
        self.sign['frameColor'] = color
        self.name['text_fg'] = color
        self.job['text_fg'] = color
        self.brlabel['text_fg'] = color
        self.falabel['text_fg'] = color
        self.face['frameColor'] = color
        self.barsframe['frameColor'] = color
        self.fbgframe['frameColor'] = color
        for label in self.labels:
            label['text_fg'] = color

    def onArrowClicked(self, direction):
        if direction == 'up':
            if self.cuy < 4:
                self.cuy = self.cuy+1
        elif direction == 'down':
            if self.cuy > 0:
                self.cuy = self.cuy-1
        elif direction == 'left':
            if self.cux > 0:
                self.cux = self.cux-1
        elif direction == 'right':
            if self.cux < 4:
                self.cux = self.cux+1

        y = .33 if self.tiles[self.cux][self.cuy]['coords'] else 0
        self.cursor.setPos(self.cux-2, self.cuy-2, y+0.025)
        
        self.updateButtons()

    def onCircleClicked(self):

        if self.tiles[self.cux][self.cuy]['coords']:
        
            if not self.char['placed']:
            
                if self.tiles[self.cux][self.cuy]['char']:
                
                    print 'Switch verticaly'
                    self.sprites[self.cux][self.cuy].node.removeNode()
                    self.sprites[self.cux][self.cuy] = Sprite.Sprite(GAME+'/textures/sprites/'+self.char['sprite']+'.png', 1)
                    self.sprites[self.cux][self.cuy].animation = 'stand'
                    self.sprites[self.cux][self.cuy].node.setPos(self.cux-2, self.cuy-2, .33+0.025)
                    self.sprites[self.cux][self.cuy].node.setScale(.3)
                    self.sprites[self.cux][self.cuy].node.reparentTo(self.root)
                    self.char['placed'] = True
                    self.tiles[self.cux][self.cuy]['char']['placed'] = False
                    self.tiles[self.cux][self.cuy]['char'] = self.char

                else:
                
                    print 'Place'
            
                    if self.remaining > 0:
                    
                        print 'Placed successfully'
                        self.sprites[self.cux][self.cuy] = Sprite.Sprite(GAME+'/textures/sprites/'+self.char['sprite']+'.png', 1)
                        self.sprites[self.cux][self.cuy].animation = 'stand'
                        self.sprites[self.cux][self.cuy].node.setPos(self.cux-2, self.cuy-2, .33+0.025)
                        self.sprites[self.cux][self.cuy].node.setScale(.3)
                        self.sprites[self.cux][self.cuy].node.reparentTo(self.root)
                        self.char['placed'] = True
                        self.tiles[self.cux][self.cuy]['char'] = self.char
                        self.remaining = self.remaining - 1
        
            else:
            
                if self.tiles[self.cux][self.cuy]['char']:

                    if self.tiles[self.cux][self.cuy]['char'] == self.char:
                
                        print 'Remove'
                        self.sprites[self.cux][self.cuy].node.removeNode()
                        self.char['placed'] = False
                        self.tiles[self.cux][self.cuy]['char']['placed'] = False
                        self.tiles[self.cux][self.cuy]['char'] = None
                        self.remaining = self.remaining + 1
                    
                    else:

                        print 'Switch horizontaly'
                        ox = oy = oc = None
                        
                        # remove the char at destination
                        self.sprites[self.cux][self.cuy].node.removeNode()
                        self.char['placed'] = False
                        self.tiles[self.cux][self.cuy]['char']['placed'] = False
                        oc = self.tiles[self.cux][self.cuy]['char']
                        self.tiles[self.cux][self.cuy]['char'] = None

                        # remove the char at origin
                        for x,l in enumerate(self.tiles):
                            for y,t in enumerate(l):
                                if t['char'] == self.char:
                                    ox = x
                                    oy = y
                                    self.sprites[x][y].node.removeNode()
                                    self.char['placed'] = False
                                    self.tiles[x][y]['char']['placed'] = False
                                    self.tiles[x][y]['char'] = None

                        # place the char at destination
                        self.sprites[self.cux][self.cuy] = Sprite.Sprite(GAME+'/textures/sprites/'+self.char['sprite']+'.png', 1)
                        self.sprites[self.cux][self.cuy].animation = 'stand'
                        self.sprites[self.cux][self.cuy].node.setPos(self.cux-2, self.cuy-2, .33+0.025)
                        self.sprites[self.cux][self.cuy].node.setScale(.3)
                        self.sprites[self.cux][self.cuy].node.reparentTo(self.root)
                        self.char['placed'] = True
                        self.tiles[self.cux][self.cuy]['char'] = self.char
                        
                        # place the char at origin
                        self.sprites[ox][oy] = Sprite.Sprite(GAME+'/textures/sprites/'+oc['sprite']+'.png', 1)
                        self.sprites[ox][oy].animation = 'stand'
                        self.sprites[ox][oy].node.setPos(ox-2, oy-2, .33+0.025)
                        self.sprites[ox][oy].node.setScale(.3)
                        self.sprites[ox][oy].node.reparentTo(self.root)
                        oc['placed'] = True
                        self.tiles[ox][oy]['char'] = oc

                else:

                    print 'Move'

                    for x,l in enumerate(self.tiles):
                        for y,t in enumerate(l):
                            if t['char'] == self.char:
                                self.sprites[x][y].node.removeNode()
                                self.char['placed'] = False
                                self.tiles[x][y]['char']['placed'] = False
                                self.tiles[x][y]['char'] = None

                    self.sprites[self.cux][self.cuy] = Sprite.Sprite(GAME+'/textures/sprites/'+self.char['sprite']+'.png', 1)
                    self.sprites[self.cux][self.cuy].animation = 'stand'
                    self.sprites[self.cux][self.cuy].node.setPos(self.cux-2, self.cuy-2, .33+0.025)
                    self.sprites[self.cux][self.cuy].node.setScale(.3)
                    self.sprites[self.cux][self.cuy].node.reparentTo(self.root)
                    self.char['placed'] = True
                    self.tiles[self.cux][self.cuy]['char'] = self.char

            self.updateChar()
            self.updateButtons()

    def onTriangleClicked(self):
        for i,char in enumerate(self.chars):
            if char == self.tiles[self.cux][self.cuy]['char']:
                self.updateChar(delta=None, current=i)

    def onStartClicked(self):
        if self.remaining < self.capacity:
            seq = Sequence(
                Func( self.ignoreAll ),
                Parallel(
                    LerpColorInterval(self.l1frame,        .5, (1,1,1,0), (1,1,1,1)),
                    LerpColorInterval(self.r1frame,        .5, (1,1,1,0), (1,1,1,1)),
                    LerpColorInterval(self.squadframe,     .5, (1,1,1,0), (1,1,1,1)),
                    LerpColorInterval(self.capacityframe,  .5, (1,1,1,0), (1,1,1,1)),
                    LerpColorInterval(self.remainingframe, .5, (1,1,1,0), (1,1,1,1)),
                    LerpColorInterval(self.searchframe,    .5, (1,1,1,0), (.75,.75,.75,1)),
                    LerpColorInterval(self.statusframe,    .5, (1,1,1,0), (.75,.75,.75,1)),
                    LerpColorInterval(self.startframe,     .5, (1,1,1,0), (.75,.75,.75,1)),
                ),
                Parallel(
                    LerpPosInterval(  self.hprcontainer,   .5, (0,0,-2), (0,0,-.415)),
                    LerpPosInterval(  self.cardframe,      .5, (v*63,0,2), (v*63,0,u*65)),
                    LerpPosInterval(  self.fbgframe,       .5, (-v*97,0,2), (-v*97,0,v*61)),
                ),
                Func( self.l1frame.removeNode ),
                Func( self.r1frame.removeNode ),
                Func( self.fbgframe.removeNode ),
                Func( self.cardframe.removeNode ),
                Func( self.squadframe.removeNode ),
                Func( self.capacityframe.removeNode ),
                Func( self.remainingframe.removeNode ),
                Func( self.searchframe.removeNode ),
                Func( self.statusframe.removeNode ),
                Func( self.startframe.removeNode ),
                Func( self.hprcontainer.removeNode ),
            ).start()

            formation = []
            for x,l in enumerate(self.tiles):
                for y,t in enumerate(l):
                    if t['char']:
                        formation.append({'charid': t['char']['id'], 'coords': t['coords'], 'direction': self.direction})
            self.command(formation)

    def updateButtons(self):

        if self.remaining < self.capacity:
            self.startframe.setColor((1,1,1,1))
        else:
            self.startframe.setColor((.75,.75,.75,1))
        if self.tiles[self.cux][self.cuy]['char']:
            self.statusframe.setColor((.75,.75,.75,1)) # TODO
            self.searchframe.setColor((1,1,1,1))
        else:
            self.statusframe.setColor((.75,.75,.75,1))
            self.searchframe.setColor((.75,.75,.75,1))

class ScrollableList(DirectObject.DirectObject):

    def __init__(self, style, x, y, w, h, flushToTop, columns, rows, maxrows, cancelcallback, title=None):

        self.style = style

        # positioning
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.flushToTop = flushToTop

        self.offset = 0
        self.rowheight = 16
        self.index = 0
        self.internalIndex = 0
        self.columns = columns
        self.rows = rows
        self.maxrows = maxrows
        self.cancelcallback = cancelcallback
        self.container = None
        self.maxoffset = len(self.rows) - self.maxrows

        menutexture = loader.loadTexture(GAME+'/textures/gui/menu2.png')
        menutexture.setMagfilter(Texture.FTNearest)
        menutexture.setMinfilter(Texture.FTNearest)

        handtexture = loader.loadTexture(GAME+'/textures/gui/hand.png')
        handtexture.setMagfilter(Texture.FTNearest)
        handtexture.setMinfilter(Texture.FTNearest)

        rulertexture = loader.loadTexture(GAME+'/textures/gui/ruler.png')
        rulertexture.setMagfilter(Texture.FTNearest)
        rulertexture.setMinfilter(Texture.FTNearest)

        self.frame = DirectFrame(
            frameColor = (1, 1, 1, 0),
            frameSize = ( -v*self.w/2.0, v*self.w/2.0, -v*self.h/2.0, v*self.h/2.0 ),
            pos = (v*self.x, 0, -v*self.y),
            geom = WindowNodeDrawer(self.w, self.h, self.style, title),
        )
        self.frame.setTransparency(True)

        self.hand = DirectFrame(
            frameTexture = handtexture,
            frameColor = (1, 1, 1, 1),
            frameSize = ( -v*8, v*8, -v*8, v*8 ),
            pos = (-v*(self.w/2+3.5), 0, v*(self.h/2-self.flushToTop+3)),
            parent = self.frame
        )

        self.ruler = DirectFrame(
            frameTexture = rulertexture,
            frameColor = (1, 1, 1, 1),
            frameSize = ( -v*4, v*4, -v*4, v*4 ),
            pos = (v*(self.w/2.0-1), 0, v*(self.h/2.0-self.flushToTop)),
            parent = self.frame
        )
        if len(rows) <= self.maxrows:
            self.ruler['frameColor'] = (1,1,1,0)

        seq = Sequence()
        seq.append(Func(self.printContent, self.offset))
        seq.append(LerpScaleInterval(self.frame, 0.1, 1, startScale=0.1))
        seq.append(Func(self.acceptAll))
        seq.start()

    def printContent(self, offset=0):

        if self.container:
            self.container.removeNode()           
        self.container = DirectFrame(parent=self.frame)

        for cid,column in enumerate(self.columns):
            for y,i in enumerate(range(offset, self.maxrows+offset)):
                rid = i
                row = self.rows[rid]
                label = DirectLabel(
                    parent = self.container,
                    color = (0,0,0,0),
                    text_fg = (1,1,1,1),
                    text = row['cells'][cid],
                    scale = regularscale,
                    text_font = column['font'],
                    text_align = column['align'],
                    pos = (v*column['x'], 0, v*(self.h/2.0-self.flushToTop-self.rowheight*y))
                )
                if not row['enabled']:
                    label['text_fg'] = (1,1,1,.5)

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
        # Array navigation.
        internalNext = (self.internalIndex + direction)
        if internalNext < len(self.rows) and internalNext > -1:
            self.internalIndex = internalNext
            # Move relative to ruler's existing position; 0 = no change.
            self.ruler.setPos(self.ruler, 0, 0, -v*direction*(self.rowheight*self.maxrows/len(self.rows)))
        # Printed list navigation.
        if next == self.maxrows:
            next = self.maxrows-1
            if self.offset < self.maxoffset:
                self.offset = self.offset + 1
                self.printContent(self.offset)
        if next == -1:
            next = 0
            if self.offset > 0:
                self.offset = self.offset - 1
                self.printContent(self.offset)
        self.hand.setPos(-v*(self.w/2+3.5), 0, v*(self.h/2-self.flushToTop-self.rowheight*next+3))        
        self.index = next

    def onCircleClicked(self):
        # self.index is in range(0, viewable row count); it is not true where len(rows) > maxrows
        if self.rows[self.internalIndex]['enabled']:
            clicked_snd.play()
            self.commandAndDestroy(self.rows[self.internalIndex]['callback'])

    def onCrossClicked(self):
        cancel_snd.play()
        self.commandAndDestroy(self.cancelcallback)

    def commandAndDestroy(self, callback):
        seq = Sequence()
        seq.append(LerpScaleInterval(self.frame, 0.1, 0.1, startScale=1))
        seq.append(Func(self.ignoreAll))
        seq.append(Func(self.frame.destroy))
        seq.append(Func(callback))
        seq.start()