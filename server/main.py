from panda3d.core import loadPrcFile
loadPrcFile("config.prc")
from pandac.PandaModules import *
import direct.directbase.DirectStart
from panda3d.core import *
from direct.task.Task import Task
from direct.distributed.PyDatagramIterator import *
from direct.distributed.PyDatagram import *
import os, sys, json
from copy import deepcopy
import Map, Move, Attack, Character
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
        self.cWriter   = ConnectionWriter(self.cManager, 0)
        self.cReader.setTcpHeaderSize(4)
        self.cWriter.setTcpHeaderSize(4)

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
            self.send_LOGIN_FAIL('Wrong credentials.', source)
        elif self.sessions.has_key(source):
            self.send_LOGIN_FAIL('Already logged in.', source)
        elif login in self.players.keys():
            self.send_LOGIN_FAIL('Username already in use.', source)
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
            self.send_LOGIN_SUCCESS(source)

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
        self.send_PARTY_CREATED(party, source)

    def get_GET_MAPS(self, iterator, source):
        self.playersinlobby.remove(source)

        mapnames = map( lambda m: m.split('.')[0], os.listdir(GAME+'/maps'))

        maps = []
        for mapname in mapnames:
            mp = Map.load(mapname)
            del mp['tiles']
            maps.append(mp)

        self.send_MAP_LIST(maps, source)

    def get_GET_PARTIES(self, iterator, source):
        self.playersinlobby.append(source)

        parties = deepcopy(self.parties)
        for party in parties.values():
            del party['map']['tiles']

        self.send_PARTY_LIST(parties, source)

    def get_JOIN_PARTY(self, iterator, source):
        name = iterator.getString()
        party = self.parties[name]
        
        if len(party['players']) >= len(party['map']['tilesets']):
            parties = deepcopy(self.parties)
            for party in parties.values():
                del party['map']['tiles']
            self.send_PARTY_JOIN_FAIL(name, parties, source)
        else:
            party['players'].append(self.sessions[source]['login'])
            self.sessions[source]['party'] = name
            self.sessions[source]['player'] = len(party['players'])-1
            self.playersinlobby.remove(source)

            print self.sessions[source]['login'], "joined the party", name
            self.send_PARTY_JOINED(party, source)

            if len(party['players']) == len(party['map']['tilesets']):
                for tilesetid,player in enumerate(party['players']):
                    self.send_START_FORMATION(party['map']['tilesets'][tilesetid], self.sessions[self.players[player]]['characters'], self.players[player])

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
                    self.send_BATTLE_COMPLETE(self.players[client])
                else:
                    self.send_GAME_OVER(self.players[client])
            del self.parties[self.sessions[source]['party']]
            self.updateAllPartyLists()
            return

        for charid in chars.keys():
            party['yourturn'] = int(chars[charid]['team']) == int(self.sessions[source]['player'])
            if chars[charid]['active']:
                self.send_PARTY_UPDATED(party['yourturn'], chars, source)
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
                        self.send_PARTY_UPDATED(party['yourturn'], chars, source)
                        return
                    else:
                        char['ct'] = 0

    def get_GET_WALKABLES(self, iterator, source):
        charid = iterator.getString()
        party = self.parties[self.sessions[source]['party']]
        walkables = Move.GetWalkables( party, charid )

        self.send_WALKABLES_LIST(charid, walkables, source)

    def get_GET_PASSIVE_WALKABLES(self, iterator, source):
        charid = iterator.getString()
        party = self.parties[self.sessions[source]['party']]
        walkables = Move.GetWalkables( party, charid )
        
        self.send_PASSIVE_WALKABLES_LIST(charid, walkables, source)

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

        self.send_PATH(charid, orig, party['chars'][charid]['direction'], (x2,y2,z2), path, source)

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
        
        self.send_MOVED(charid, x2, y2, z2, source)
        
        for playerid,playerlogin in enumerate(party['players']):
            if playerid != self.sessions[source]['player']:
                self.send_MOVED_PASSIVE(charid, walkables, path, self.players[playerlogin])

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
        
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('WAIT_SUCCESS')
        self.cWriter.send(myPyDatagram, source)

        for playerid,playerlogin in enumerate(party['players']):
            if playerid != self.sessions[source]['player']:
                self.send_WAIT_PASSIVE(charid, direction, self.players[playerlogin])

    def get_GET_ATTACKABLES(self, iterator, source):
        charid = iterator.getString()
        
        party = self.parties[self.sessions[source]['party']]
        
        attackables = Attack.GetAttackables( party, charid )

        self.send_ATTACKABLES_LIST(charid, attackables, source)

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
        
        self.send_ATTACK_SUCCESS(charid1, charid2, damages, source)
        
        attackables = Attack.GetAttackables( party, charid1 )
        
        for playerid,playerlogin in enumerate(party['players']):
            if playerid != self.sessions[source]['player']:
                self.send_ATTACK_PASSIVE(charid1, charid2, damages, attackables, self.players[playerlogin])

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
                self.send_START_BATTLE(party, self.players[playerlogin])

    def processData(self, datagram):
        iterator = PyDatagramIterator(datagram)
        source = datagram.getConnection()
        callback = iterator.getString()
        getattr(self, 'get_'+callback)(iterator, source)

    def send_LOGIN_FAIL(self, errormsg, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('LOGIN_FAIL')
        myPyDatagram.addString(errormsg)
        self.cWriter.send(myPyDatagram, player)

    def send_LOGIN_SUCCESS(self, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('LOGIN_SUCCESS')
        self.cWriter.send(myPyDatagram, player)

    def send_PARTY_CREATED(self, party, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('PARTY_CREATED')
        myPyDatagram.addString32(json.dumps(party))
        self.cWriter.send(myPyDatagram, player)

    def send_MAP_LIST(self, maps, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('MAP_LIST')
        myPyDatagram.addString(json.dumps(maps))
        self.cWriter.send(myPyDatagram, player)

    def send_PARTY_LIST(self, parties, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('PARTY_LIST')
        myPyDatagram.addString32(json.dumps(parties))
        self.cWriter.send(myPyDatagram, player)

    def send_PARTY_JOIN_FAIL(self, name, parties, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('PARTY_JOIN_FAIL')
        myPyDatagram.addString('Party '+name+' is full.')
        myPyDatagram.addString32(json.dumps(parties))
        self.cWriter.send(myPyDatagram, player)

    def send_PARTY_JOINED(self, party, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('PARTY_JOINED')
        myPyDatagram.addString32(json.dumps(party))
        self.cWriter.send(myPyDatagram, player)

    def send_START_FORMATION(self, tileset, team, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('START_FORMATION')
        myPyDatagram.addString32(json.dumps(tileset))
        myPyDatagram.addString32(json.dumps(team))
        self.cWriter.send(myPyDatagram, player)

    def send_BATTLE_COMPLETE(self, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('BATTLE_COMPLETE')
        self.cWriter.send(myPyDatagram, player)

    def send_GAME_OVER(self, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('GAME_OVER')
        self.cWriter.send(myPyDatagram, player)

    def send_PARTY_UPDATED(self, yourturn, chars, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('PARTY_UPDATED')
        myPyDatagram.addBool(yourturn)
        myPyDatagram.addString32(json.dumps(chars))
        self.cWriter.send(myPyDatagram, player)

    def send_WALKABLES_LIST(self, charid, walkables, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('WALKABLES_LIST')
        myPyDatagram.addString(charid)
        myPyDatagram.addString(json.dumps(walkables))
        self.cWriter.send(myPyDatagram, player)

    def send_PASSIVE_WALKABLES_LIST(self, charid, walkables, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('PASSIVE_WALKABLES_LIST')
        myPyDatagram.addString(charid)
        myPyDatagram.addString(json.dumps(walkables))
        self.cWriter.send(myPyDatagram, player)

    def send_PATH(self, charid, orig, direction, dest, path, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('PATH')
        myPyDatagram.addString(charid)
        myPyDatagram.addString(json.dumps(orig))
        myPyDatagram.addUint8(direction)
        myPyDatagram.addString(json.dumps(dest))
        myPyDatagram.addString(json.dumps(path))
        self.cWriter.send(myPyDatagram, player)

    def send_MOVED(self, charid, x, y, z, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('MOVED')
        myPyDatagram.addString(charid)
        myPyDatagram.addUint8(x)
        myPyDatagram.addUint8(y)
        myPyDatagram.addUint8(z)
        self.cWriter.send(myPyDatagram, player)

    def send_MOVED_PASSIVE(self, charid, walkables, path, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('MOVED_PASSIVE')
        myPyDatagram.addString(charid)
        myPyDatagram.addString(json.dumps(walkables))
        myPyDatagram.addString(json.dumps(path))
        self.cWriter.send(myPyDatagram, player)

    def send_WAIT_PASSIVE(self, charid, direction, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('WAIT_PASSIVE')
        myPyDatagram.addString(charid)
        myPyDatagram.addUint8(direction)
        self.cWriter.send(myPyDatagram, player)

    def send_ATTACKABLES_LIST(self, charid, attackables, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('ATTACKABLES_LIST')
        myPyDatagram.addString(charid)
        myPyDatagram.addString(json.dumps(attackables))
        self.cWriter.send(myPyDatagram, player)

    def send_ATTACK_SUCCESS(self, charid1, charid2, damages, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('ATTACK_SUCCESS')
        myPyDatagram.addString(charid1)
        myPyDatagram.addString(charid2)
        myPyDatagram.addUint8(damages)
        self.cWriter.send(myPyDatagram, player)

    def send_ATTACK_PASSIVE(self, charid1, charid2, damages, attackables, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('ATTACK_PASSIVE')
        myPyDatagram.addString(charid1)
        myPyDatagram.addString(charid2)
        myPyDatagram.addUint8(damages)
        myPyDatagram.addString(json.dumps(attackables))
        self.cWriter.send(myPyDatagram, player)

    def send_START_BATTLE(self, party, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('START_BATTLE')
        myPyDatagram.addString32(json.dumps(party))
        self.cWriter.send(myPyDatagram, player)

    def send_UPDATE_PARTY_LIST(self, parties, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('UPDATE_PARTY_LIST')
        myPyDatagram.addString32(json.dumps(parties))
        self.cWriter.send(myPyDatagram, player)

    def updateAllPartyLists(self):
        parties = deepcopy(self.parties)
        for party in parties.values():
            del party['map']['tiles']

        for player in self.playersinlobby:
            self.send_UPDATE_PARTY_LIST(parties, player)

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

