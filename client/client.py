import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.task.Task import Task
import battle
import Network

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

        self.logingui()

    def logingui(self):

        bgtexture = loader.loadTexture('textures/gui/loadingbackground.png')
        bgtexture.setMagfilter(Texture.FTNearest)
        bgtexture.setMinfilter(Texture.FTNearest)

        base.setBackgroundColor(.03125, .03125, .03125)

        self.loginBackground = DirectFrame( color = (1, 1, 1, 1), frameTexture = bgtexture, frameSize = ( -1.33, 1.33, -1, 1 ) )
        self.loginBackground.setTransparency(True)
    
        self.loginWindow = DirectFrame( color = (.62, .6, .5, 1), frameSize = ( -.35, .35, -.1, .15 ) )
        self.loginWindow.setTransparency(True)
        self.loginWindow.reparentTo( self.loginBackground )
        self.loginWindow.setPos(0, 0, -0.33)

        font = loader.loadFont('fonts/fft.egg')
        winHeight = base.win.getYSize()
        ppu = 12
        scale = (4.0 * ppu) / winHeight      

        self.loginLabel = DirectLabel(
            text = 'Login:',
            color = (.62, .6, .5, 0),
            scale = scale,
            text_font = font,
            text_fg = (.0625,.3125,.5,1),
            text_shadow = (.5,.46484375,.40625,1),
            text_align = TextNode.ALeft
        )
        self.loginLabel.reparentTo( self.loginWindow )
        self.loginLabel.setPos(-0.3, 0, 0.05)

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
        self.loginEntry.setPos(-0.1, 0, 0.05)

        self.passwordLabel = DirectLabel(
            text = 'Pass:',
            color = (.62, .6, .5, 0),
            scale = scale,
            text_font = font,
            text_fg = (.0625,.3125,.5,1),
            text_shadow = (.5,.46484375,.40625,1),
            text_align = TextNode.ALeft
        )
        self.passwordLabel.reparentTo( self.loginWindow )
        self.passwordLabel.setPos(-0.3, 0, -0.05)

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
        self.passwordEntry.setPos(-0.1, 0, -0.05)

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
        connectButton.setPos(0.2, 0, -0.2)

    def login(self):
        login = self.loginEntry.get()
        password = self.passwordEntry.get()

        rsp = self.con.Send('login', { 'login': login, 'pass': password })
        if rsp:
            self.loginBackground.destroy()
            self.partiesgui()

    def partiesgui(self):
        self.partiesFrame = DirectFrame( color = (0, 0, 0, 0.5), frameSize = ( -1.2, 1.2, -0.7, 0.7 ) )
        self.partiesFrame.setTransparency(True)
        self.partiesFrame.setPos(0, 0, 0.15)

        self.createPartyFrame = DirectFrame( color = (0, 0, 0, 0.5), frameSize = ( -1.2, 1.2, 0.1, -0.1 ) )
        self.createPartyFrame.setTransparency(True)
        self.createPartyFrame.setPos(0, 0, -0.75)
        
        partyNameLabel = DirectLabel( scale = .05, text  = ("Name", "Name", "Name", "disabled") )
        partyNameLabel.reparentTo( self.createPartyFrame  )
        partyNameLabel.setPos(-1.0, 0, 0)
        
        self.partyNameEntry = DirectEntry( scale = .05, numLines = 1, focus = 1 )
        self.partyNameEntry.reparentTo( self.createPartyFrame  )
        self.partyNameEntry.setPos(-0.8, 0, 0)
        
        mapLabel = DirectLabel( scale = .05, text  = ("Map", "Map", "Map", "disabled") )
        mapLabel.reparentTo( self.createPartyFrame  )
        mapLabel.setPos(-0.1, 0, 0)
        
        self.mapMenu = DirectOptionMenu( text = "options", scale = 0.05, 
                                         items = [ "Test City" ],
                                         highlightColor = ( 0.65, 0.65, 0.65, 1 ) )
        self.mapMenu.reparentTo( self.createPartyFrame  )
        self.mapMenu.setPos(0, 0, 0)
        
        createPartyButton = DirectButton( scale = .05, text  = ("Create", "Create", "Create", "disabled"), command = self.createparty )
        createPartyButton.reparentTo( self.createPartyFrame )
        createPartyButton.setPos(0.5, 0, 0)
        
        self.refreshparties = True

    def refreshPartiesTask(self, task):
        if self.refreshparties:

            parties = self.con.Send('parties')
            if parties and parties != self.parties:

                if self.partiesFrame:
                    self.partiesFrame.destroy()
                self.partiesFrame = DirectFrame( color = (0, 0, 0, 0.5), frameSize = ( -1.2, 1.2, -0.7, 0.7 ) )
                self.partiesFrame.setTransparency(True)
                self.partiesFrame.setPos(0, 0, 0.15)
                nameHeader    = OnscreenText(text = 'Name',    pos = (-1.0, .6), scale = 0.05, parent = self.partiesFrame)
                creatorHeader = OnscreenText(text = 'Creator', pos = (-0.5, .6), scale = 0.05, parent = self.partiesFrame)
                mapHeader     = OnscreenText(text = 'Map',     pos = ( 0.0, .6), scale = 0.05, parent = self.partiesFrame)

                self.parties = parties
                for i,key in enumerate(parties):
                    nameLabel    = OnscreenText(text = parties[key]['name'],        pos = (-1.0, -i/10.0+.5), scale = 0.05, parent = self.partiesFrame)
                    creatorLabel = OnscreenText(text = parties[key]['creator'],     pos = (-0.5, -i/10.0+.5), scale = 0.05, parent = self.partiesFrame)
                    mapLabel     = OnscreenText(text = parties[key]['map']['name'], pos = ( 0.0, -i/10.0+.5), scale = 0.05, parent = self.partiesFrame)
                    joinPartyButton = DirectButton( scale = .05, text  = ("Join", "Join", "Join", "Full"), command = self.joinparty, extraArgs = [key] )
                    joinPartyButton.reparentTo( self.partiesFrame )
                    joinPartyButton.setPos(0.5, 0, -i/10.0+.5)

                    if parties[key].has_key('player1') and parties[key].has_key('player2'):
                        joinPartyButton['state'] = DGG.DISABLED

        return Task.cont    

    def joinparty(self, key):
        party = self.con.Send('joinparty/'+key)
        if party:
            self.party = party
            self.refreshparties = False
            self.partiesFrame.destroy()
            self.createPartyFrame.destroy()
            self.partygui()

    def createparty(self):
        name = self.partyNameEntry.get()
        mapname = self.mapMenu.get()

        party = self.con.Send('ownparty', { 'name': name, 'mapname': mapname })
        if party:
            self.party = party
            self.refreshparties = False
            self.partiesFrame.destroy()
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
                self.battle_begins()

        return Task.cont

    def battle_begins(self):
        b = battle.Battle(self.con, self.party)

