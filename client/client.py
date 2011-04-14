import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.task.Task import Task
from direct.interval.IntervalGlobal import LerpScaleInterval, LerpColorInterval, Sequence, Func, Wait
import battle
import Network
import GUI

font = loader.loadFont('fonts/fft.egg')
u = 1.0/128.0
scale = u*12.0
hover_snd = base.loader.loadSfx("sounds/hover.ogg")
clicked_snd = base.loader.loadSfx("sounds/clicked.ogg")

class Client:

    def __init__(self):
    
        # Play the background music
        self.music = base.loader.loadSfx('music/24.ogg')
        self.music.setLoop(True)
        self.music.play()
    
        self.con = Network.ServerConnection()
        
        self.party = False
        self.parties = []

        self.background = GUI.Background(self.logingui)

    def logingui(self):

        self.loginwindow = GUI.LoginWindow(self.login)

    def login(self):
        login = self.loginwindow.loginEntry.get()
        password = self.loginwindow.passwordEntry.get()

        rsp = self.con.Send('login', { 'login': login, 'pass': password })
        if rsp:
            self.loginwindow.commandanddestroy(self.partiesgui)

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
        
        self.partycreationwindow = GUI.PartyCreationWindow(self.createparty)

    def refreshParties(self):
        self.refreshpartiestask = taskMgr.doMethodLater(1, self.refreshPartiesTask, 'refreshPartiesTask')

    def refreshPartiesTask(self, task):
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
                    rolloverSound = hover_snd,
                    clickSound = clicked_snd,
                    pressEffect = 0,
                    parent = self.partiesWindow
                )
                joinPartyButton.setPos(u*80, 0, u*49 - i*u*16)

                if parties[key].has_key('player1') and parties[key].has_key('player2'):
                    joinPartyButton['state'] = DGG.DISABLED

        return Task.again    

    def joinparty(self, key):
        party = self.con.Send('joinparty/'+key)
        if party:
            self.party = party
            taskMgr.remove(self.refreshpartiestask)
            self.partiesWindow.destroy()
            self.partycreationwindow.frame.destroy()
            self.partygui()

    def createparty(self):
        name = self.partycreationwindow.nameEntry.get()
        mapname = self.partycreationwindow.mapOptionMenu.get()

        party = self.con.Send('ownparty', { 'name': name, 'mapname': mapname })
        if party:
            self.party = party
            taskMgr.remove(self.refreshpartiestask)
            self.partiesWindow.destroy()
            self.partycreationwindow.frame.destroy()
            self.partygui()

    def partygui(self):
        
        self.partyFrame = DirectFrame( color = (0, 0, 0, 0.5), frameSize = ( -1, 1, -0.9, 0.9 ) )
        self.partyFrame.setTransparency(True)
        self.partyFrame.setPos(0, 0, 0)
        
        partyName  = OnscreenText(text = 'Party: '+self.party['name'],         pos = (0, 0.8), scale = 0.07, parent = self.partyFrame)
        createdBy  = OnscreenText(text = 'Created by: '+self.party['creator'], pos = (0, 0.7), scale = 0.05, parent = self.partyFrame)
        waitingFor = OnscreenText(text = 'Waiting for second character',       pos = (0, 0.0), scale = 0.05, parent = self.partyFrame)

        self.refreshpartytask = taskMgr.doMethodLater(1, self.refreshPartyTask, 'refreshPartyTask')

    def refreshPartyTask(self, task):
        party = self.con.Send('party')
        if party and party.has_key('player2'):
            self.party = party
            self.selectchargui()
            return Task.done

        return Task.again

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
            self.refreshbattletask = taskMgr.doMethodLater(1, self.refreshBattleTask, 'refreshBattleTask')

    def refreshBattleTask(self, task):
        party = self.con.Send('battle')
        if party:
            self.party = party
            self.battle_begins()
            return Task.done

        return Task.again

    def battle_begins(self):
        self.transitionframe = DirectFrame( frameSize = ( -2, 2, -2, 2 ) )
        self.transitionframe.setTransparency(True)
        seq = Sequence()
        seq.append(LerpColorInterval(self.transitionframe, 2, (0,0,0,1), startColor=(0,0,0,0)))
        seq.append(Func(self.partyFrame.destroy))
        seq.append(Func(self.background.frame.destroy))
        seq.append(Func(self.music.stop))
        seq.append(Func(battle.Battle, self.con, self.party, self.transitionframe))
        seq.start()

