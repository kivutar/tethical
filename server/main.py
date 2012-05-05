from panda3d.core import loadPrcFile
loadPrcFile("config.prc")
from pandac.PandaModules import *
import direct.directbase.DirectStart
from panda3d.core import *
from direct.task.Task import Task
from direct.distributed.PyDatagramIterator import *
import os, sys, json
from copy import deepcopy
import Map, Move, Attack, Character
from Send import Send
GAME = ConfigVariableString('game', 'fft').getValue()

class Server:

    def __init__(self):

        self.activeConnections = [] # lists all connections
        self.players = {} # keys are the players logins, values are the players datagram connections
        self.parties = {} # keys are the parties names, values are dicts representing parties data
        self.sessions = {} # keys are the datagram connections, values are dicts storing the characters of the player and its party
        self.playersinlobby = [] # lists players in the party screen
        self.charid = 0 # used for random team generation
        self.chars = [] # lists of dicts representing characters data

        self.cManager  = QueuedConnectionManager()
        self.cListener = QueuedConnectionListener(self.cManager, 0)
        self.cReader   = QueuedConnectionReader(self.cManager, 0)
        self.cReader.setTcpHeaderSize(4)
        self.send = Send(self.cManager)

        port = 3001
        if len(sys.argv) > 1:
            port = sys.argv[1]

        self.tcpSocket = self.cManager.openTCPServerRendezvous(port, 10)
        self.cListener.addConnection(self.tcpSocket)
        print "Server listening on port", port

        taskMgr.add(self.tskListenerPolling, "Poll the connection listener", -39)
        taskMgr.add(self.tskReaderPolling, "Poll the connection reader", -40)

    # The following functions prefixed by get_ are controllers.
    # These controllers are triggered when the server recieve packets.
    # They access packet data, do stuff, and send back instructions to one or more clients

    # A client is trying to log into the server. Let's check its credentials and sent it back a reply
    def get_LOGIN_MESSAGE(self, iterator, source):
        login = iterator.getString()
        password = iterator.getString()

        # since the server code is not connected to the database yet,
        # we authenticate the client if login == password
        if login != password:
            self.send.LOGIN_FAIL('Wrong credentials.', source)
        elif self.sessions.has_key(source):
            self.send.LOGIN_FAIL('Already logged in.', source)
        elif login in self.players.keys():
            self.send.LOGIN_FAIL('Username already in use.', source)
        else:
            self.players[login] = source
            self.sessions[source] = {}
            self.sessions[source]['login'] = login
            print login, 'logged in.'
            # since the server code is not connected to the database yet,
            # we generate a random team for each player
            self.sessions[source]['characters'] = []
            for i in range(10):
                self.charid = self.charid + 1
                char = Character.Random(self.charid)
                self.sessions[source]['characters'].append(char)
                self.chars.append(char)
            self.send.LOGIN_SUCCESS(source)

    # A player tries to create a party.
    def get_CREATE_PARTY(self, iterator, source):
        name = iterator.getString()
        mapname = iterator.getString()
        
        party = {
            'name': name,
            'mapname': mapname,
            'map' : Map.load(mapname),
            'chars': {},
            'log': {},
            'creator': self.sessions[source]['login'],
            'players': [],
            'formations': [],
        }
        party['players'].append(self.sessions[source]['login'])

        self.parties[name] = party
        self.sessions[source]['party'] = name
        self.sessions[source]['player'] = len(party['players'])-1
        
        self.updateAllPartyLists()
        
        print self.sessions[source]['login'], "created the party", name, "using the map", mapname
        self.send.PARTY_CREATED(party, source)

    def get_GET_MAPS(self, iterator, source):
        self.playersinlobby.remove(source)

        mapnames = map( lambda m: m.split('.')[0], os.listdir(GAME+'/maps'))

        maps = []
        for mapname in mapnames:
            mp = Map.load(mapname)
            del mp['tiles']
            maps.append(mp)

        self.send.MAP_LIST(maps, source)

    def get_GET_PARTIES(self, iterator, source):
        self.playersinlobby.append(source)

        parties = deepcopy(self.parties)
        for party in parties.values():
            del party['map']['tiles']

        self.send.PARTY_LIST(parties, source)

    def get_JOIN_PARTY(self, iterator, source):
        name = iterator.getString()
        party = self.parties[name]
        
        if len(party['players']) >= len(party['map']['tilesets']):
            parties = deepcopy(self.parties)
            for party in parties.values():
                del party['map']['tiles']
            self.send.PARTY_JOIN_FAIL(name, parties, source)
        else:
            party['players'].append(self.sessions[source]['login'])
            self.sessions[source]['party'] = name
            self.sessions[source]['player'] = len(party['players'])-1
            self.playersinlobby.remove(source)

            print self.sessions[source]['login'], "joined the party", name
            self.send.PARTY_JOINED(party, source)

            if len(party['players']) == len(party['map']['tilesets']):
                for tilesetid,player in enumerate(party['players']):
                    self.send.START_FORMATION(party['map']['tilesets'][tilesetid], self.sessions[self.players[player]]['characters'], self.players[player])

            self.updateAllPartyLists()

    def get_UPDATE_PARTY(self, iterator, source):
        party = self.parties[self.sessions[source]['party']]
        chars = party['chars']
        
        aliveteams = {}
        for charid in chars.keys():
            if chars[charid]['hp'] > 0:
                if aliveteams.has_key(chars[charid]['team']):
                    aliveteams[chars[charid]['team']] = aliveteams[chars[charid]['team']] + 1
                else:
                    aliveteams[chars[charid]['team']] = 1
        if len(aliveteams) < 2:
            for client in party['players']:
                if source == self.players[client]:
                    self.send.BATTLE_COMPLETE(self.players[client])
                else:
                    self.send.GAME_OVER(self.players[client])
            del self.parties[self.sessions[source]['party']]
            self.updateAllPartyLists()
            return

        for charid in chars.keys():
            party['yourturn'] = int(chars[charid]['team']) == int(self.sessions[source]['player'])
            if chars[charid]['active']:
                self.send.PARTY_UPDATED(party['yourturn'], chars, source)
                return
        
        while True:
            for charid in chars.keys():
                char = chars[charid]
                char['ct'] = char['ct'] + char['speed']
                if char['ct'] >= 100:
                    if char['hp'] > 0:
                        char['active'] = True
                        char['canmove'] = True
                        char['canact'] = True
                        party['yourturn'] = int(chars[charid]['team']) == int(self.sessions[source]['player'])
                        self.send.PARTY_UPDATED(party['yourturn'], chars, source)
                        return
                    else:
                        char['ct'] = 0

    def get_GET_WALKABLES(self, iterator, source):
        charid = iterator.getString()
        party = self.parties[self.sessions[source]['party']]
        walkables = Move.GetWalkables( party, charid )

        self.send.WALKABLES_LIST(charid, walkables, source)

    def get_GET_PASSIVE_WALKABLES(self, iterator, source):
        charid = iterator.getString()
        party = self.parties[self.sessions[source]['party']]
        walkables = Move.GetWalkables( party, charid )
        
        self.send.PASSIVE_WALKABLES_LIST(charid, walkables, source)

    def get_GET_PATH(self, iterator, source):
        charid = iterator.getString()
        x2 = iterator.getUint8()
        y2 = iterator.getUint8()
        z2 = iterator.getUint8()
        
        party = self.parties[self.sessions[source]['party']]
        
        orig = Character.Coords( party, charid )
        x1 = orig[0]
        y1 = orig[1]
        z1 = orig[2]
        
        path = Move.GetPath( party, charid, x1, y1, z1, x2, y2, z2 )

        self.send.PATH(charid, orig, party['chars'][charid]['direction'], (x2,y2,z2), path, source)

    def get_MOVE_TO(self, iterator, source):
        charid = iterator.getString()
        x2 = iterator.getUint8()
        y2 = iterator.getUint8()
        z2 = iterator.getUint8()
        
        party = self.parties[self.sessions[source]['party']]
        
        orig = Character.Coords( party, charid )
        x1 = orig[0]
        y1 = orig[1]
        z1 = orig[2]

        path = Move.GetPath( party, charid, x1, y1, z1, x2, y2, z2 )
        walkables = Move.GetWalkables( party, charid )

        del party['map']['tiles'][x1][y1][z1]['char']
        party['map']['tiles'][x2][y2][z2]['char'] = charid

        party['chars'][charid]['direction'] = Move.GetNewDirection( x1, y1, x2, y2 )
        party['chars'][charid]['canmove'] = False
        
        self.send.MOVED(charid, x2, y2, z2, source)
        
        for playerid,playerlogin in enumerate(party['players']):
            if playerid != self.sessions[source]['player']:
                self.send.MOVED_PASSIVE(charid, walkables, path, self.players[playerlogin])

    def get_WAIT(self, iterator, source):
        charid = iterator.getString()
        direction = iterator.getUint8()
        
        party = self.parties[self.sessions[source]['party']]
        char = party['chars'][charid]

        if char['canmove'] and char['canact']:
            char['ct'] = char['ct'] - 60
        elif char['canmove'] or char['canact']:
            char['ct'] = char['ct'] - 80
        else:
            char['ct'] = char['ct'] - 100

        char['direction'] = direction

        char['active'] = False
        char['canmove'] = False
        char['canact'] = False

        self.send.WAIT_SUCCESS(source)

        for playerid,playerlogin in enumerate(party['players']):
            if playerid != self.sessions[source]['player']:
                self.send.WAIT_PASSIVE(charid, direction, self.players[playerlogin])

    def get_GET_ATTACKABLES(self, iterator, source):
        charid = iterator.getString()
        
        party = self.parties[self.sessions[source]['party']]
        
        attackables = Attack.GetAttackables( party, charid )

        self.send.ATTACKABLES_LIST(charid, attackables, source)

    def get_ATTACK(self, iterator, source):
        charid1 = iterator.getString()
        charid2 = iterator.getString()
        party = self.parties[self.sessions[source]['party']]
        char1 = party['chars'][charid1]
        char2 = party['chars'][charid2]
        
        damages = char1['pa'] * char1['br'] / 100 * char1['pa']
        
        char2['hp'] = char2['hp'] - damages*4
        if char2['hp'] < 0:
            char2['hp'] = 0
        
        char1['canact'] = False
        
        self.send.ATTACK_SUCCESS(charid1, charid2, damages, source)
        
        attackables = Attack.GetAttackables( party, charid1 )
        
        for playerid,playerlogin in enumerate(party['players']):
            if playerid != self.sessions[source]['player']:
                self.send.ATTACK_PASSIVE(charid1, charid2, damages, attackables, self.players[playerlogin])

    def get_FORMATION_READY(self, iterator, source):
        formation = json.loads(iterator.getString())

        party = self.parties[self.sessions[source]['party']]
        party['formations'].append(formation)

        if len(party['formations']) == len(party['map']['tilesets']):

            for team,formation in enumerate(party['formations']):
                for line in formation:
                    x, y, z = line['coords']
                    charid = line['charid']
                    party['map']['tiles'][x][y][z]['char'] = str(charid)
                    char = filter(lambda x: x['id'] == charid, self.chars)[0]
                    char['team'] = team
                    char['direction'] = line['direction']
                    party['chars'][str(charid)] = char

            for playerlogin in party['players']:
                self.send.START_BATTLE(party, self.players[playerlogin])

    def processData(self, datagram):
        iterator = PyDatagramIterator(datagram)
        source = datagram.getConnection()
        callback = iterator.getString()
        getattr(self, 'get_'+callback)(iterator, source)

    def updateAllPartyLists(self):
        parties = deepcopy(self.parties)
        for party in parties.values():
            del party['map']['tiles']

        for player in self.playersinlobby:
            self.send.UPDATE_PARTY_LIST(parties, player)

    def tskListenerPolling(self, taskdata):
        if self.cListener.newConnectionAvailable():

            rendezvous = PointerToConnection()
            netAddress = NetAddress()
            newConnection = PointerToConnection()
     
            if self.cListener.getNewConnection(rendezvous, netAddress, newConnection):
                newConnection = newConnection.p()
                self.activeConnections.append(newConnection)
                self.cReader.addConnection(newConnection)
                print 'A new client is connected', newConnection
        return Task.cont

    def tskReaderPolling(self, taskdata):
        if self.cReader.dataAvailable():
            datagram=NetDatagram()
            if self.cReader.getData(datagram):
                self.processData(datagram)
        return Task.cont

Server()
run()

