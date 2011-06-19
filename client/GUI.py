import direct.directbase.DirectStart
from direct.showbase import DirectObject
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.DirectGui import *
from direct.task import Task
from direct.actor import Actor
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *

u = 1.0/128.0
hover_snd = base.loader.loadSfx("sounds/hover.ogg")
clicked_snd = base.loader.loadSfx("sounds/clicked.ogg")
cancel_snd = base.loader.loadSfx("sounds/cancel.ogg")
scale = u*12.0
font = loader.loadFont('fonts/fft')
font3 = loader.loadFont('fonts/fft3')
font4 = loader.loadFont('fonts/fft4')
coordsfont = loader.loadFont('fonts/fftcoords')

class Coords(DirectObject.DirectObject):

    def __init__(self, tile):

        self.coordstn = TextNode('tn')
        self.coordstn.setFont(coordsfont)
        self.coordstn.setAlign(self.coordstn.ARight)
        self.coordstn.setTextColor(1,1,1,1)
        self.tnp = aspect2d.attachNewNode(self.coordstn)
        self.tnp.setScale(scale)
        self.tnp.setPos(0.9, 0.0, 0.6)

        self.update(tile)

    def update(self, tile):
        self.coordstn.setText(str(tile['z']/2).replace('.0','').replace('.5','a')+'h')

    def destroy(self):
        self.tnp.removeNode()

class Background(DirectObject.DirectObject):

    def __init__(self, command):
        
        tex = loader.loadTexture('textures/gui/loadingbackground.png')
        tex.setMagfilter(Texture.FTNearest)
        tex.setMinfilter(Texture.FTNearest)

        base.setBackgroundColor(.03125, .03125, .03125)

        self.frame = DirectFrame( color = (1, 1, 1, 1), frameTexture = tex, frameSize = ( -2.2, 2.2, -2.2, 2.2 ), scale = 10 )
        self.frame.setTransparency(True)

        seq = Sequence()
        i = LerpScaleInterval(self.frame, 0.1, 1, startScale=10 )
        seq.append(i)
        seq.append( Wait(0.5) )
        seq.append( Func(command) )
        seq.start()

class LoginWindow(DirectObject.DirectObject):

    def __init__(self, command):
        
        tex = loader.loadTexture('textures/gui/login_window.png')
        tex.setMagfilter(Texture.FTNearest)
        tex.setMinfilter(Texture.FTNearest)

        self.frame = DirectFrame( frameTexture = tex, color = (1, 1, 1, 1), frameSize = ( -.5, .5, -.25, .25 ), scale = 0.1 )
        self.frame.setTransparency(True)

        self.loginLabel = DirectLabel(
            text = 'Username:',
            color = (.62, .6, .5, 0),
            scale = scale,
            text_font = font,
            text_fg = (.0625,.3125,.5,1),
            text_shadow = (.5,.46484375,.40625,1),
            text_align = TextNode.ALeft,
            parent = self.frame
        )
        self.loginLabel.setPos(-u*50, 0, u*3)

        self.loginEntry = DirectEntry(
            color = (.62, .6, .5, 0),
            scale = scale,
            numLines = 1,
            focus = 1,
            text_font = font,
            text_fg = (.1875,.15625,.125,1),
            text_shadow = (.5,.46484375,.40625,1),
            parent = self.frame
        )
        self.loginEntry.setPos(-u*6, 0, u*3)

        self.passwordLabel = DirectLabel(
            text = 'Password:',
            color = (.62, .6, .5, 0),
            scale = scale,
            text_font = font,
            text_fg = (.0625,.3125,.5,1),
            text_shadow = (.5,.46484375,.40625,1),
            text_align = TextNode.ALeft,
            parent = self.frame
        )
        self.passwordLabel.setPos(-u*50, 0, -u*13)

        self.passwordEntry = DirectEntry(
            color = (.62, .6, .5, 0),
            scale = scale,
            numLines = 1,
            text_font = font,
            text_fg = (.1875,.15625,.125,1),
            text_shadow = (.5,.46484375,.40625,1),
            obscured = True,
            parent = self.frame
        )
        self.passwordEntry.setPos(-u*6, 0, -u*13)

        connectButton = DirectButton(
            scale = scale,
            text  = ("Connect", "Connect", "Connect", "disabled"),
            command = command,
            color = (.62, .6, .5, 1),
            text_font = font,
            text_fg = (.1875,.15625,.125,1),
            text_shadow = (.5,.46484375,.40625,1),
            rolloverSound = hover_snd,
            clickSound = clicked_snd,
            pressEffect = 0,
            pad = (.15,.15),
            parent = self.frame
        )
        connectButton.setPos(u*38, 0, -u*40)

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

        tex = loader.loadTexture('textures/gui/parties_window.png')
        tex.setMagfilter(Texture.FTNearest)
        tex.setMinfilter(Texture.FTNearest)
    
        self.frame = DirectFrame( frameTexture = tex, color = (1, 1, 1, 1), frameSize = ( -1, 1, -1, 1 ), scale=0.1 )
        self.frame.setTransparency(True)
        
        cptexture = loader.loadTexture('textures/gui/create_party.png')
        cptexture.setMagfilter(Texture.FTNearest)
        cptexture.setMinfilter(Texture.FTNearest)

        self.cpframe = DirectFrame(
            frameTexture = cptexture,
            frameColor = (1, 1, 1, 1),
            frameSize = ( -.25, .25, -.0625, .0625 ),
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
        self.accept("v",    self.onTriangleClicked)

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

        for i,key in enumerate(parties):
            nameLabel = DirectLabel(
                color = (0,0,0,0),
                text = parties[key]['name'],
                scale = scale,
                text_font = font,
                text_fg = (.1875,.15625,.125,1),
                text_shadow = (.5,.46484375,.40625,1),
                text_align = TextNode.ALeft,
                parent = self.frame
            )
            nameLabel.setPos(-u*93, 0, u*49 - i*u*16)

            creatorLabel = DirectLabel(
                color = (0,0,0,0),
                text = parties[key]['creator'],
                scale = scale,
                text_font = font,
                text_fg = (.1875,.15625,.125,1),
                text_shadow = (.5,.46484375,.40625,1),
                text_align = TextNode.ALeft,
                parent = self.frame
            )
            creatorLabel.setPos(-u*30, 0, u*49 - i*u*16)

            mapLabel = DirectLabel(
                color = (0,0,0,0),
                text = parties[key]['map']['name'],
                scale = scale,
                text_font = font,
                text_fg = (.1875,.15625,.125,1),
                text_shadow = (.5,.46484375,.40625,1),
                text_align = TextNode.ALeft,
                parent = self.frame
            )
            mapLabel.setPos(u*20, 0, u*49 - i*u*16)
            
            joinButton = DirectButton(
                text  = ("Join", "Join", "Join", "Full"),
                command = self.commandAndDestroy,
                extraArgs = [lambda: self.command(key)],
                scale = scale,
                text_font = font,
                text_fg = (.1875,.15625,.125,1),
                text_shadow = (.5,.46484375,.40625,1),
                text_align = TextNode.ALeft,
                rolloverSound = hover_snd,
                clickSound = clicked_snd,
                pressEffect = 0,
                parent = self.frame
            )
            joinButton.setPos(u*80, 0, u*49 - i*u*16)

            if parties[key].has_key('player1') and parties[key].has_key('player2'):
                joinButton['state'] = DGG.DISABLED

class Menu(DirectObject.DirectObject):

    def __init__(self, char, movecommand, attackcommand, waitcommand, cancelcommand):

        self.offset = 22
        self.height = 16
        self.index = 0
        self.cancelcommand = cancelcommand

        self.buttons = [
            { 'text': 'Move',   'enabled': char['canmove'], 'pos': (-u*36.5,0,u*(self.offset-self.height*0)), 'command': movecommand   },
            { 'text': 'Attack', 'enabled': char['canact' ], 'pos': (-u*36.5,0,u*(self.offset-self.height*1)), 'command': attackcommand },
            { 'text': 'Wait',   'enabled': True           , 'pos': (-u*36.5,0,u*(self.offset-self.height*2)), 'command': waitcommand   },
            { 'text': 'Status', 'enabled': False          , 'pos': (-u*36.5,0,u*(self.offset-self.height*3)), 'command': cancelcommand },
        ]

        menutexture = loader.loadTexture('textures/gui/menu.png')
        menutexture.setMagfilter(Texture.FTNearest)
        menutexture.setMinfilter(Texture.FTNearest)

        handtexture = loader.loadTexture('textures/gui/hand.png')
        handtexture.setMagfilter(Texture.FTNearest)
        handtexture.setMinfilter(Texture.FTNearest)

        self.frame = DirectFrame(
            frameTexture = menutexture,
            frameColor = (1, 1, 1, 1),
            frameSize = ( -.25, .25, -.5, .5 ),
            pos = (.75, 0, 0),
            scale = 0.1,
        )
        self.frame.setTransparency(True)

        self.hand = DirectFrame(
            frameTexture = handtexture,
            frameColor = (1, 1, 1, 1),
            frameSize = ( -u*8, u*8, -u*8, u*8 ),
            pos = self.buttons[0]['pos'],
            parent = self.frame
        )

        for i,button in enumerate(self.buttons):
            label = DirectLabel(
                color = (0,0,0,0),
                text = button['text'],
                scale = scale,
                text_font = font,
                text_fg = (.1875,.15625,.125,1),
                text_shadow = (.5,.46484375,.40625,1),
                text_align = TextNode.ALeft,
                parent = self.frame,
                pos = (-u*25, 0, u*(self.offset-3-self.height*i))
            )
            if not button['enabled']:
                label['text_fg'] = (.375,.34375,.28125,1)
        
        seq = Sequence()
        seq.append(LerpScaleInterval(self.frame, 0.1, 1, startScale=0.1))
        seq.append(Func(self.acceptAll))
        seq.start()

    def acceptAll(self):
        self.accept("space", self.onCrossClicked)
        self.accept("b",    self.onCircleClicked)
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
            { 'text': 'Yes',   'enabled': True, 'pos': (u*45.5,0,u*(self.offset-self.height*0)), 'command': command       },
            { 'text': 'No',    'enabled': True, 'pos': (u*45.5,0,u*(self.offset-self.height*1)), 'command': cancelcommand },
        ]

        tex = loader.loadTexture('textures/gui/move_check.png')
        tex.setMagfilter(Texture.FTNearest)
        tex.setMinfilter(Texture.FTNearest)

        handtexture = loader.loadTexture('textures/gui/hand.png')
        handtexture.setMagfilter(Texture.FTNearest)
        handtexture.setMinfilter(Texture.FTNearest)

        self.frame = DirectFrame(
            frameTexture = tex,
            frameColor = (1, 1, 1, 1),
            frameSize = ( -1, 1, -.5, .5 ),
            pos = (0, 0, 0),
            scale = 0.1,
        )
        self.frame.setTransparency(True)

        self.hand = DirectFrame(
            frameTexture = handtexture,
            frameColor = (1, 1, 1, 1),
            frameSize = ( -u*8, u*8, -u*8, u*8 ),
            pos = self.buttons[0]['pos'],
            parent = self.frame
        )

        messageLabel = DirectLabel(
            color = (0,0,0,0),
            text = 'Are you sure you want to move here?',
            scale = scale,
            text_font = font,
            text_fg = (.1875,.15625,.125,1),
            text_shadow = (.5,.46484375,.40625,1),
            text_align = TextNode.ALeft,
            parent = self.frame,
            pos = (-u*75, 0, u*19)
        )

        for i,button in enumerate(self.buttons):
            label = DirectLabel(
                color = (0,0,0,0),
                text = button['text'],
                scale = scale,
                text_font = font,
                text_fg = (.1875,.15625,.125,1),
                text_shadow = (.5,.46484375,.40625,1),
                text_align = TextNode.ALeft,
                parent = self.frame,
                pos = (u*57, 0, u*(self.offset-3-self.height*i))
            )
            if not button['enabled']:
                label['text_fg'] = (.375,.34375,.28125,1)

        seq = Sequence()
        seq.append(LerpScaleInterval(self.frame, 0.1, 1, startScale=0.1))
        seq.append(Func(self.acceptAll))
        seq.start()

    def acceptAll(self):
        self.accept("space", self.onCrossClicked)
        self.accept("b",    self.onCircleClicked)
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
            { 'text': 'Execute', 'enabled': True, 'pos': (-u*8.5,0,u*(self.offset-self.height*0)), 'command': command       },
            { 'text': 'Quit',    'enabled': True, 'pos': (-u*8.5,0,u*(self.offset-self.height*1)), 'command': cancelcommand },
        ]

        tex = loader.loadTexture('textures/gui/attack_check.png')
        tex.setMagfilter(Texture.FTNearest)
        tex.setMinfilter(Texture.FTNearest)

        handtexture = loader.loadTexture('textures/gui/hand.png')
        handtexture.setMagfilter(Texture.FTNearest)
        handtexture.setMinfilter(Texture.FTNearest)

        self.frame = DirectFrame(
            frameTexture = tex,
            frameColor = (1, 1, 1, 1),
            frameSize = ( -.5, .5, -.5, .5 ),
            pos = (0, 0, 0),
            scale = 0.1,
        )
        self.frame.setTransparency(True)

        self.hand = DirectFrame(
            frameTexture = handtexture,
            frameColor = (1, 1, 1, 1),
            frameSize = ( -u*8, u*8, -u*8, u*8 ),
            pos = self.buttons[0]['pos'],
            parent = self.frame
        )

# TODO: Fix line height
#        messageLabel = DirectLabel(
#            color = (0,0,0,0),
#            text = 'Executing action.\nOK?',
#            scale = scale,
#            text_font = font,
#            text_fg = (.1875,.15625,.125,1),
#            text_shadow = (.5,.46484375,.40625,1),
#            text_align = TextNode.ALeft,
#            parent = self.frame,
#            pos = (-u*33, 0, u*27)
#        )

        for i,button in enumerate(self.buttons):
            label = DirectLabel(
                color = (0,0,0,0),
                text = button['text'],
                scale = scale,
                text_font = font,
                text_fg = (.1875,.15625,.125,1),
                text_shadow = (.5,.46484375,.40625,1),
                text_align = TextNode.ALeft,
                parent = self.frame,
                pos = (u*3, 0, u*(self.offset-3-self.height*i))
            )
            if not button['enabled']:
                label['text_fg'] = (.375,.34375,.28125,1)

        seq = Sequence()
        seq.append(LerpScaleInterval(self.frame, 0.1, 1, startScale=0.1))
        seq.append(Func(self.acceptAll))
        seq.start()

    def acceptAll(self):
        self.accept("space", self.onCrossClicked)
        self.accept("b",    self.onCircleClicked)
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

        tex = loader.loadTexture('textures/gui/'+message+'.png')
        tex.setMagfilter(Texture.FTNearest)
        tex.setMinfilter(Texture.FTNearest)

        self.frame = DirectFrame(
            frameTexture = tex,
            frameColor = (1, 1, 1, 1),
            frameSize = ( -1.0, 1.0, -.25, .25 ),
            pos = (0, 0, .25),
            scale = 0.1,
        )
        self.frame.setTransparency(True)
        
        seq = Sequence()
        seq.append(LerpScaleInterval(self.frame, 0.1, 1, startScale=0.1))
        seq.append(Func(self.acceptAll))
        seq.start()

    def acceptAll(self):
        self.accept("space", self.onCrossClicked)
        self.accept("b", self.onCircleClicked )

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

class CharCard:

    def __init__(self, char):
        tex = loader.loadTexture('textures/gui/char_card1.png')
        tex.setMagfilter(Texture.FTNearest)
        tex.setMinfilter(Texture.FTNearest)

        self.frame = DirectFrame(
            frameTexture = tex, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( -.5, .5, -.25, .25 )
        )
        self.frame.setTransparency(True)
        self.frame.setPos(-2, 0, -u*85)
        
        facetex = loader.loadTexture('textures/sprites/'+char['sprite']+'_face.png')
        facetex.setMagfilter(Texture.FTNearest)
        facetex.setMinfilter(Texture.FTNearest)
        
        self.face = DirectFrame(
            frameTexture = facetex, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( 0, u*32, 0, u*64 ),
            parent = self.frame
        )
        self.face.setPos(-u*59, 0, -u*31)
        
        tex2 = loader.loadTexture('textures/gui/char_card2.png')
        tex2.setMagfilter(Texture.FTNearest)
        tex2.setMinfilter(Texture.FTNearest)

        self.frame2 = DirectFrame(
            frameTexture = tex2, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( -.5, .5, -.25, .25 ),
            parent = self.frame
        )
        self.frame2.setTransparency(True)
        
        infos = [
            { 'x': 16 , 'z':  16 , 'text': '%02d' % char['lv'] },
            { 'x': 48 , 'z':  16 , 'text': '%02d' % char['exp'] },
            { 'x': 18 , 'z':   2 , 'text': '%03d' % char['hp'] },
            { 'x': 37 , 'z':  -2 , 'text': '%03d' % char['hpmax'] },
            { 'x': 18 , 'z':  -9 , 'text': '%03d' % char['mp'] },
            { 'x': 37 , 'z': -13 , 'text': '%03d' % char['mpmax'] },
            { 'x': 18 , 'z': -20 , 'text': '%03d' % char['ct'] },
            { 'x': 37 , 'z': -24 , 'text': '100' },
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
            label.setPos(u*info['x'], 0, u*info['z'])

        i1 = LerpPosInterval(self.frame, 0.2, (-u*55,0,-u*85), (-2,0,-u*85))
        s = Sequence(i1)
        s.start()

    def hide(self):
        if self.frame:
            i1 = LerpPosInterval(self.frame, 0.2, (-2,0,-u*85), (-u*55,0,-u*85))
            i2 = Func( self.frame.destroy )
            s = Sequence(i1,i2)
            s.start()

class CharCard2:

    def __init__(self, char):
        blacktex = loader.loadTexture('textures/gui/black.png')
        blacktex.setMagfilter(Texture.FTNearest)
        blacktex.setMinfilter(Texture.FTNearest)

        self.blackframe = DirectFrame(frameTexture = blacktex, 
                                 frameColor=(1, 1, 1, 1),
                                 frameSize = ( -1, 1, -.5, .5 ))
        self.blackframe.reparentTo(render2d)
        self.blackframe.setTransparency(True)
        self.blackframe.setPos(0, 0, u*-85)

        tex = loader.loadTexture('textures/gui/char_card3.png')
        tex.setMagfilter(Texture.FTNearest)
        tex.setMinfilter(Texture.FTNearest)

        self.frame = DirectFrame(
            frameTexture = tex, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( -.5, .5, -.25, .25 )
        )
        self.frame.setTransparency(True)
        self.frame.setPos(2, 0, -u*85)

        self.name = DirectLabel(
            text = char['name'],
            color = (.62, .6, .5, 0),
            scale = scale,
            text_font = font,
            text_fg = (.1875,.15625,.125,1),
            text_shadow = (.5,.46484375,.40625,1),
            text_align = TextNode.ALeft,
            parent = self.frame
        )
        self.name.setPos(-u*33, 0, u*12)

        self.name = DirectLabel(
            text = char['job'],
            color = (.62, .6, .5, 0),
            scale = scale,
            text_font = font,
            text_fg = (.1875,.15625,.125,1),
            text_shadow = (.5,.46484375,.40625,1),
            text_align = TextNode.ALeft,
            parent = self.frame
        )
        self.name.setPos(-u*33, 0, -u*4)

        teamcolors = ['','blue','red']
        ledtex = loader.loadTexture('textures/gui/char_card_'+teamcolors[int(char['team'])]+'.png')
        ledtex.setMagfilter(Texture.FTNearest)
        ledtex.setMinfilter(Texture.FTNearest)

        self.led = DirectFrame(
            frameTexture = ledtex, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( -.0625, .0625, -.0625, .0625 ),
            parent = self.frame
        )
        self.led.setTransparency(True)
        self.led.setPos(-u*49, 0, u*18)

        signs = ['aries','scorpio']
        signtex = loader.loadTexture('textures/gui/'+signs[int(char['sign'])]+'.png')
        signtex.setMagfilter(Texture.FTNearest)
        signtex.setMinfilter(Texture.FTNearest)

        self.sign = DirectFrame(
            frameTexture = signtex, 
            frameColor=(1, 1, 1, 1),
            frameSize = ( -.125, .125, -.125, .125 ),
            parent = self.frame
        )
        self.sign.setTransparency(True)
        self.sign.setPos(-u*42, 0, -u*12)

        brlabel = DirectLabel(
            text = str(char['br']),
            color = (1, 1, 1, 0),
            scale = scale,
            text_font = font4,
            text_fg = (1,1,1,1),
            text_align = TextNode.ARight,
            parent = self.frame
        )
        brlabel.setPos(u*6, 0, -u*22)

        falabel = DirectLabel(
            text = str(char['fa']),
            color = (1, 1, 1, 0),
            scale = scale,
            text_font = font4,
            text_fg = (1,1,1,1),
            text_align = TextNode.ARight,
            parent = self.frame
        )
        falabel.setPos(u*45, 0, -u*22)

        i1 = LerpScaleInterval(self.blackframe, 0.1, (1,1,1), (1,1,0))
        i2 = LerpColorInterval(self.blackframe, 0.1, (1,1,1,1), (1,1,1,0))
        i3 = LerpPosInterval(  self.frame,      0.2, (u*63,0,-u*85), (2,0,-u*85))
        p1 = Parallel(i1,i2,i3)
        s = Sequence(p1)
        s.start()

    def hide(self):
        if self.frame:
            i1 = LerpScaleInterval(self.blackframe, 0.1, (1,1,0), (1,1,1))
            i2 = LerpColorInterval(self.blackframe, 0.1, (1,1,1,0), (1,1,1,1))
            i3 = LerpPosInterval(  self.frame,      0.2, (2,0,-u*85), (.5,0,-u*85))
            p1 = Parallel(i1,i2,i3)
            i4 = Func( self.blackframe.destroy )
            i5 = Func( self.frame.destroy )
            s = Sequence(p1,i4,i5)
            s.start()

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
        
        cfwtex = loader.loadTexture('textures/gui/conditions_for_winning.png')
        cfwtex.setMagfilter(Texture.FTNearest)
        cfwtex.setMinfilter(Texture.FTNearest)
        cfw = DirectFrame(
            color = (1,1,1,0),
            frameTexture = cfwtex,
            frameSize = ( -1.0, 1.0, -.125, .125 ),
            pos = (u*20, 0, u*90),
        )
        cfw.setTransparency(True)

        daetex = loader.loadTexture('textures/gui/defeat_all_enemies.png')
        daetex.setMagfilter(Texture.FTNearest)
        daetex.setMinfilter(Texture.FTNearest)
        dae = DirectFrame(
            color = (1,1,1,0),
            frameTexture = daetex,
            frameSize = ( -1.0, 1.0, -.125, .125 ),
            pos = (u*49, 0, u*60),
        )
        dae.setTransparency(True)

        readytex = loader.loadTexture('textures/gui/ready.png')
        readytex.setMagfilter(Texture.FTNearest)
        readytex.setMinfilter(Texture.FTNearest)
        ready = DirectFrame(
            color = (1,1,1,0),
            frameTexture = readytex,
            frameSize = ( -1.0, 1.0, -.125, .125 ),
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
        
        ggtex = loader.loadTexture('textures/gui/congratulations.png')
        ggtex.setMagfilter(Texture.FTNearest)
        ggtex.setMinfilter(Texture.FTNearest)
        gg = DirectFrame(
            color = (1,1,1,0),
            frameTexture = ggtex,
            frameSize = ( -1.0, 1.0, -.125, .125 ),
            pos = (u*0, 0, u*30),
        )
        gg.setTransparency(True)

        bctex = loader.loadTexture('textures/gui/battle_complete.png')
        bctex.setMagfilter(Texture.FTNearest)
        bctex.setMinfilter(Texture.FTNearest)
        bc = DirectFrame(
            color = (1,1,1,0),
            frameTexture = bctex,
            frameSize = ( -.5, .5, -.125, .125 ),
            pos = (u*0, 0, -u*30),
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
        
        gotex = loader.loadTexture('textures/gui/game_over.png')
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

        loadingtexture = loader.loadTexture('textures/gui/now_loading.png')
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
            terrain = loader.loadModel( 'models/maps/'+mapinfo['model'] )
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

        l1texture = loader.loadTexture('textures/gui/L1.png')
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

        r1texture = loader.loadTexture('textures/gui/R1.png')
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

        starttexture = loader.loadTexture('textures/gui/start_end.png')
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
        self.accept("space", self.onCrossClicked)
        self.accept("enter", self.onStartClicked)
        self.accept("a",     self.onL1Clicked)
        self.accept("z",     self.onR1Clicked)
        self.accept("a-repeat", self.onL1Clicked)
        self.accept("z-repeat", self.onR1Clicked)

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
            loader.unloadModel( 'models/maps/'+mapinfo['model'] )
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

