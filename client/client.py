import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from pandac.PandaModules import *
import urllib2
from urllib import urlencode
import cookielib
import json
from direct.task.Task import Task
import time
import battle

class Client:

    def __init__(self):
    
        self.cookies = cookielib.CookieJar()
        self.cookies.clear()
        
        self.party = False
        self.parties = []
        
        self.refreshparties = False
        self.refreshPartiesTask = taskMgr.add(self.refreshPartiesTask, 'refreshPartiesTask')
        
        self.refreshparty = False
        self.refreshPartyTask = taskMgr.add(self.refreshPartyTask, 'refreshPartyTask')
        
        self.logingui()

    def logingui(self):
        self.loginFrame = DirectFrame( color = (0, 0, 0, 0.5), frameSize = ( -.35, .35, -.25, .25 ) )
        self.loginFrame.setTransparency(True)
        self.loginFrame.setPos(0, 0, -0.33)

        self.loginEntry = DirectEntry( scale = .05, numLines = 1, focus = 1 )
        self.loginEntry.reparentTo( self.loginFrame )
        self.loginEntry.setPos(-0.25, 0, 0.1)

        self.passwordEntry = DirectEntry( scale = .05, numLines = 1, obscured = True )
        self.passwordEntry.reparentTo( self.loginFrame )
        self.passwordEntry.setPos(-0.25, 0, -0.025)

        connectButton = DirectButton( scale = .05, text  = ("Connect", "Connect", "Connect", "disabled"), command = self.login )
        connectButton.reparentTo( self.loginFrame )
        connectButton.setPos(0, 0, -0.15)

    def login(self):
        login = self.loginEntry.get()
        password = self.passwordEntry.get()
        values = { 'login': login, 'pass': password }
        try:
            opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1), urllib2.HTTPCookieProcessor(self.cookies))
            urllib2.install_opener(opener)
            rsp = opener.open('http://localhost:3000/login', urlencode(values))
        except IOError:
            print 'fail'
        else:
            print rsp.read()
            rsp.close()
            self.loginFrame.destroy()
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
            #time.sleep(1)
            try:
                opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1), urllib2.HTTPCookieProcessor(self.cookies))
                urllib2.install_opener(opener)
                rsp = opener.open('http://localhost:3000/parties')
            except IOError:
                print 'fail'
            else:
                parties = json.loads(rsp.read())
                rsp.close()
                if parties != self.parties:
                    self.parties = parties
                    for key in parties:
                        partyName = OnscreenText(text = 'Name: '+parties[key]['name'], pos = (0, 0), scale = 0.05, parent = self.partiesFrame)
                        joinPartyButton = DirectButton( scale = .05, text  = ("Join", "Join", "Join", "disabled"), command = self.joinparty, extraArgs = [key] )
                        joinPartyButton.reparentTo( self.partiesFrame )
                        joinPartyButton.setPos(0.5, 0, 0)
                
        return Task.cont    

    def joinparty(self, key):
        try:
            opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1), urllib2.HTTPCookieProcessor(self.cookies))
            urllib2.install_opener(opener)
            rsp = opener.open('http://localhost:3000/joinparty/'+key)
        except IOError:
            print 'fail'
        else:
            self.party = json.loads(rsp.read())
            rsp.close()
            self.refreshparties = False
            self.partiesFrame.destroy()
            self.createPartyFrame.destroy()
            self.partygui()        

    def createparty(self):
        name = self.partyNameEntry.get()
        mapname = self.mapMenu.get()
        values = { 'name': name, 'mapname': mapname }
        try:
            opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1), urllib2.HTTPCookieProcessor(self.cookies))
            urllib2.install_opener(opener)
            rsp = opener.open('http://localhost:3000/ownparty', urlencode(values))
        except IOError:
            print 'fail'
        else:
            self.party = json.loads(rsp.read())
            rsp.close()
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
            #time.sleep(1)
            try:
                opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1), urllib2.HTTPCookieProcessor(self.cookies))
                urllib2.install_opener(opener)
                rsp = opener.open('http://localhost:3000/party')
            except IOError:
                print 'fail'
            else:
                self.party = json.loads(rsp.read())
                rsp.close()
                if self.party.has_key('player2'):
                    self.partyFrame.destroy()
                    self.refreshparty = False
                    self.selectchargui()
        return Task.cont

    def selectchargui(self):
        try:
            opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1), urllib2.HTTPCookieProcessor(self.cookies))
            urllib2.install_opener(opener)
            rsp = opener.open('http://localhost:3000/choosechar')
        except IOError:
            print 'fail'
        else:
            tiles = json.loads(rsp.read())
            rsp.close()
            values = {}
            for i,tile in enumerate(tiles):
                values[str(tile['x'])+'-'+str(tile['y'])+'-'+str(tile['z'])+'-'+str(tile['direction'])] = str(tile['x'])+str(tile['y'])+str(tile['z'])
            self.characters_selected(values)

    def characters_selected(self, values):
        try:
            opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1), urllib2.HTTPCookieProcessor(self.cookies))
            urllib2.install_opener(opener)
            rsp = opener.open('http://localhost:3000/startbattle', urlencode(values))
        except IOError:
            print 'fail'
        else:
            res = json.loads(rsp.read())
            rsp.close()
            self.battle_begins()

    def battle_begins(self):
        b = battle.Battle(self.cookies)

Client()
run()
