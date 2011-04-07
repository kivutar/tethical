import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.task.Task import Task
from direct.interval.IntervalGlobal import LerpScaleInterval, Sequence, Func, Wait
import battle
import Network

font = loader.loadFont('fonts/fft.egg')
u = 1.0/128.0
scale = u*12.0

class Client:

    def __init__(self):
    
        self.con = Network.ServerConnection()
        
        self.party = False
        self.parties = []
        
        self.refreshparties = False
        self.refreshPartiesTask = taskMgr.add(self.refreshPartiesTask, 'refreshPartiesTask')
        
        self.refreshparty = False
        self.refreshPartyTask = taskMgr.add(self.refreshPartyTask, 'refreshPartyTask')
        
        self.refreshbattle = False
        self.refreshBattleTask = taskMgr.add(self.refreshBattleTask, 'refreshBattleTask')
        
        bgtex = loader.loadTexture('textures/gui/loadingbackground.png')
        bgtex.setMagfilter(Texture.FTNearest)
        bgtex.setMinfilter(Texture.FTNearest)

        base.setBackgroundColor(.03125, .03125, .03125)

        self.loginBackground = DirectFrame( color = (1, 1, 1, 1), frameTexture = bgtex, frameSize = ( -1.33, 1.33, -1, 1 ), scale = 10 )
        
        seq = Sequence()
        i = LerpScaleInterval(self.loginBackground, 0.1, 1, startScale=10 )
        seq.append(i)
        seq.append( Wait(0.5) )
        seq.append( Func(self.logingui) )
        seq.start()

    def logingui(self):
    
        bgtex = loader.loadTexture('textures/gui/login_window.png')
        bgtex.setMagfilter(Texture.FTNearest)
        bgtex.setMinfilter(Texture.FTNearest)

        self.loginWindow = DirectFrame( frameTexture = bgtex, color = (1, 1, 1, 1), frameSize = ( -.5, .5, -.25, .25 ), scale = 0.1 )
        self.loginWindow.setTransparency(True)
        self.loginWindow.reparentTo( self.loginBackground )
        self.loginWindow.setPos(0, 0, 0)

        self.loginLabel = DirectLabel(
            text = 'Username:',
            color = (.62, .6, .5, 0),
            scale = scale,
            text_font = font,
            text_fg = (.0625,.3125,.5,1),
            text_shadow = (.5,.46484375,.40625,1),
            text_align = TextNode.ALeft
        )
        self.loginLabel.reparentTo( self.loginWindow )
        self.loginLabel.setPos(-u*50, 0, u*3)

        self.loginEntry = DirectEntry(
            color = (.62, .6, .5, 0),
            scale = scale,
            numLines = 1,
            focus = 1,
            text_font = font,
            text_fg = (.1875,.15625,.125,1),
            text_shadow = (.5,.46484375,.40625,1)
        )
        self.loginEntry.reparentTo( self.loginWindow )
        self.loginEntry.setPos(-u*6, 0, u*3)

        self.passwordLabel = DirectLabel(
            text = 'Password:',
            color = (.62, .6, .5, 0),
            scale = scale,
            text_font = font,
            text_fg = (.0625,.3125,.5,1),
            text_shadow = (.5,.46484375,.40625,1),
            text_align = TextNode.ALeft
        )
        self.passwordLabel.reparentTo( self.loginWindow )
        self.passwordLabel.setPos(-u*50, 0, -u*13)

        self.passwordEntry = DirectEntry(
            color = (.62, .6, .5, 0),
            scale = scale,
            numLines = 1,
            text_font = font,
            text_fg = (.1875,.15625,.125,1),
            text_shadow = (.5,.46484375,.40625,1),
            obscured = True
        )
        self.passwordEntry.reparentTo( self.loginWindow )
        self.passwordEntry.setPos(-u*6, 0, -u*13)

        connectButton = DirectButton(
            scale = scale,
            text  = ("Connect", "Connect", "Connect", "disabled"),
            command = self.login,
            color = (.62, .6, .5, 1),
            text_font = font,
            text_fg = (.1875,.15625,.125,1),
            text_shadow = (.5,.46484375,.40625,1),
            pad = (.15,.15)
        )
        connectButton.reparentTo( self.loginWindow )
        connectButton.setPos(u*38, 0, -u*40)
        
        seq = Sequence()
        i = LerpScaleInterval(self.loginWindow, 0.1, 1, startScale=0.1 )
        seq.append(i)
        seq.start()

    def login(self):
        login = self.loginEntry.get()
        password = self.passwordEntry.get()

        rsp = self.con.Send('login', { 'login': login, 'pass': password })
        if rsp:
            seq = Sequence()
            i = LerpScaleInterval(self.loginWindow, 0.1, 0.1, startScale=1 )
            seq.append(i)
            seq.append( Func(self.loginWindow.destroy) )
            seq.append( Wait(0.5) )
            seq.append( Func(self.partiesgui) )
            seq.start()

    def partiesgui(self):
    
        pwbgtex = loader.loadTexture('textures/gui/parties_window.png')
        pwbgtex.setMagfilter(Texture.FTNearest)
        pwbgtex.setMinfilter(Texture.FTNearest)
    
        self.partiesWindow = DirectFrame( frameTexture = pwbgtex, color = (1, 1, 1, 1), frameSize = ( -1, 1, -1, 1 ), scale=0.1 )
        self.partiesWindow.setTransparency(True)
        self.partiesWindow.setPos(0, 0, u*21)
        
        seq = Sequence()
        i = LerpScaleInterval(self.partiesWindow, 0.1, 1, startScale=0.1 )
        seq.append(i)
        seq.append(Func(self.refreshParties))
        seq.start()
        
        npwbgtex = loader.loadTexture('textures/gui/newparty_window.png')
        npwbgtex.setMagfilter(Texture.FTNearest)
        npwbgtex.setMinfilter(Texture.FTNearest)

        self.createPartyFrame = DirectFrame( frameTexture = npwbgtex, color = (1, 1, 1, 1), frameSize = ( -1, 1, -.25, .25 ), scale=0.1 )
        self.createPartyFrame.setTransparency(True)
        self.createPartyFrame.setPos(0, 0, -u*80)
        
        self.partyNameEntry = DirectEntry(
            color = (0,0,0,0),
            scale = scale,
            numLines = 1,
            focus = 1,
            text_font = font,
            text_fg = (.1875,.15625,.125,1),
            text_shadow = (.5,.46484375,.40625,1),
            parent = self.createPartyFrame,
        )
        self.partyNameEntry.setPos(-u*93, 0, -u*7)

        self.mapMenu = DirectOptionMenu(
            text = "options",
            scale = scale, 
            items = [ "Test City", "Test City 3", "Test City 65" ],
            highlightColor = ( 0.65, 0.65, 0.65, 1 ),
            text_font = font,
            text_fg = (.1875,.15625,.125,1),
            text_shadow = (.5,.46484375,.40625,1),
            text_align = TextNode.ALeft,
            parent = self.createPartyFrame,
        )
        self.mapMenu.setPos(-u*10, 0, -u*7)
        
        createPartyButton = DirectButton(
            text  = ("Create", "Create", "Create", "disabled"),
            scale = scale,
            text_font = font,
            text_fg = (.1875,.15625,.125,1),
            text_shadow = (.5,.46484375,.40625,1),
            text_align = TextNode.ALeft,
            parent = self.createPartyFrame,
            command = self.createparty
        )
        createPartyButton.setPos(u*70, 0, -u*7)
        
        seq2 = Sequence()
        i2 = LerpScaleInterval(self.createPartyFrame, 0.1, 1, startScale=0.1 )
        seq2.append(i2)
        seq2.start()

    def refreshParties(self):
        self.refreshparties = True

    def refreshPartiesTask(self, task):
        if self.refreshparties:

            parties = self.con.Send('parties')
            if parties and parties != self.parties:

                if hasattr(self, 'partiesWindow'):
                    self.partiesWindow.destroy()

                bgtex = loader.loadTexture('textures/gui/parties_window.png')
                bgtex.setMagfilter(Texture.FTNearest)
                bgtex.setMinfilter(Texture.FTNearest)

                self.partiesWindow = DirectFrame( frameTexture = bgtex, color = (1, 1, 1, 1), frameSize = ( -1, 1, -1, 1 ) )
                self.partiesWindow.setTransparency(True)
                self.partiesWindow.setPos(0, 0, 0.15)

                self.parties = parties
                for i,key in enumerate(parties):
                    nameLabel = DirectLabel(
                        color = (0,0,0,0),
                        text = parties[key]['name'],
                        scale = scale,
                        text_font = font,
                        text_fg = (.1875,.15625,.125,1),
                        text_shadow = (.5,.46484375,.40625,1),
                        text_align = TextNode.ALeft,
                        parent = self.partiesWindow
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
                        parent = self.partiesWindow
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
                        parent = self.partiesWindow
                    )
                    mapLabel.setPos(u*20, 0, u*49 - i*u*16)
                    
                    joinPartyButton = DirectButton(
                        text  = ("Join", "Join", "Join", "Full"),
                        command = self.joinparty,
                        extraArgs = [key],
                        scale = scale,
                        text_font = font,
                        text_fg = (.1875,.15625,.125,1),
                        text_shadow = (.5,.46484375,.40625,1),
                        text_align = TextNode.ALeft,
                        parent = self.partiesWindow
                    )
                    joinPartyButton.setPos(u*80, 0, u*49 - i*u*16)

                    if parties[key].has_key('player1') and parties[key].has_key('player2'):
                        joinPartyButton['state'] = DGG.DISABLED

        return Task.cont    

    def joinparty(self, key):
        party = self.con.Send('joinparty/'+key)
        if party:
            self.party = party
            self.refreshparties = False
            self.partiesWindow.destroy()
            self.createPartyFrame.destroy()
            self.partygui()

    def createparty(self):
        name = self.partyNameEntry.get()
        mapname = self.mapMenu.get()

        party = self.con.Send('ownparty', { 'name': name, 'mapname': mapname })
        if party:
            self.party = party
            self.refreshparties = False
            self.partiesWindow.destroy()
            self.createPartyFrame.destroy()
            self.partygui()

    def partygui(self):
        
        self.partyFrame = DirectFrame( color = (0, 0, 0, 0.5), frameSize = ( -1, 1, -0.9, 0.9 ) )
        self.partyFrame.setTransparency(True)
        self.partyFrame.setPos(0, 0, 0)
        
        partyName  = OnscreenText(text = 'Party: '+self.party['name'],         pos = (0, 0.8), scale = 0.07, parent = self.partyFrame)
        createdBy  = OnscreenText(text = 'Created by: '+self.party['creator'], pos = (0, 0.7), scale = 0.05, parent = self.partyFrame)
        waitingFor = OnscreenText(text = 'Waiting for second character',       pos = (0, 0.0), scale = 0.05, parent = self.partyFrame)
        
        self.refreshparty = True

    def refreshPartyTask(self, task):
        if self.refreshparty:
            
            party = self.con.Send('party')
            if party and party.has_key('player2'):
                self.party = party
                self.partyFrame.destroy()
                self.refreshparty = False
                self.selectchargui()

        return Task.cont

    def selectchargui(self):
        tiles = self.con.Send('choosechar')
        if tiles:
            values = {}
            for i,tile in enumerate(tiles):
                values[str(tile['x'])+'-'+str(tile['y'])+'-'+str(tile['z'])+'-'+str(tile['direction'])] = str(tile['x'])+str(tile['y'])+str(tile['z'])
            self.characters_selected(values)

    def characters_selected(self, values):
        res = self.con.Send('startbattle', values)
        if res:
            self.refreshbattle = True

    def refreshBattleTask(self, task):
        if self.refreshbattle:

            party = self.con.Send('battle')
            if party:
                self.party = party
                self.refreshbattle = False
                self.loginBackground.destroy()
                self.battle_begins()

        return Task.cont

    def battle_begins(self):
        b = battle.Battle(self.con, self.party)

