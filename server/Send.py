from direct.distributed.PyDatagram import PyDatagram, ConnectionWriter
import json

# Datagrams to be sent to the clients
class Send(object):

    def __init__(self, cManager):
        self.cWriter = ConnectionWriter(cManager, 0)
        self.cWriter.setTcpHeaderSize(4)

    def LOGIN_FAIL(self, errormsg, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('LOGIN_FAIL')
        myPyDatagram.addString(errormsg)
        self.cWriter.send(myPyDatagram, player)

    def LOGIN_SUCCESS(self, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('LOGIN_SUCCESS')
        self.cWriter.send(myPyDatagram, player)

    def PARTY_CREATED(self, party, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('PARTY_CREATED')
        myPyDatagram.addString32(json.dumps(party))
        self.cWriter.send(myPyDatagram, player)

    def MAP_LIST(self, maps, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('MAP_LIST')
        myPyDatagram.addString(json.dumps(maps))
        self.cWriter.send(myPyDatagram, player)

    def PARTY_LIST(self, parties, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('PARTY_LIST')
        myPyDatagram.addString32(json.dumps(parties))
        self.cWriter.send(myPyDatagram, player)

    def PARTY_JOIN_FAIL(self, name, parties, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('PARTY_JOIN_FAIL')
        myPyDatagram.addString('Party '+name+' is full.')
        myPyDatagram.addString32(json.dumps(parties))
        self.cWriter.send(myPyDatagram, player)

    def PARTY_JOINED(self, party, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('PARTY_JOINED')
        myPyDatagram.addString32(json.dumps(party))
        self.cWriter.send(myPyDatagram, player)

    def START_FORMATION(self, tileset, team, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('START_FORMATION')
        myPyDatagram.addString32(json.dumps(tileset))
        myPyDatagram.addString32(json.dumps(team))
        self.cWriter.send(myPyDatagram, player)

    def BATTLE_COMPLETE(self, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('BATTLE_COMPLETE')
        self.cWriter.send(myPyDatagram, player)

    def GAME_OVER(self, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('GAME_OVER')
        self.cWriter.send(myPyDatagram, player)

    def PARTY_UPDATED(self, yourturn, chars, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('PARTY_UPDATED')
        myPyDatagram.addBool(yourturn)
        myPyDatagram.addString32(json.dumps(chars))
        self.cWriter.send(myPyDatagram, player)

    def WALKABLES_LIST(self, charid, walkables, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('WALKABLES_LIST')
        myPyDatagram.addString(charid)
        myPyDatagram.addString(json.dumps(walkables))
        self.cWriter.send(myPyDatagram, player)

    def PASSIVE_WALKABLES_LIST(self, charid, walkables, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('PASSIVE_WALKABLES_LIST')
        myPyDatagram.addString(charid)
        myPyDatagram.addString(json.dumps(walkables))
        self.cWriter.send(myPyDatagram, player)

    def PATH(self, charid, orig, direction, dest, path, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('PATH')
        myPyDatagram.addString(charid)
        myPyDatagram.addString(json.dumps(orig))
        myPyDatagram.addUint8(direction)
        myPyDatagram.addString(json.dumps(dest))
        myPyDatagram.addString(json.dumps(path))
        self.cWriter.send(myPyDatagram, player)

    def MOVED(self, charid, x, y, z, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('MOVED')
        myPyDatagram.addString(charid)
        myPyDatagram.addUint8(x)
        myPyDatagram.addUint8(y)
        myPyDatagram.addUint8(z)
        self.cWriter.send(myPyDatagram, player)

    def MOVED_PASSIVE(self, charid, walkables, path, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('MOVED_PASSIVE')
        myPyDatagram.addString(charid)
        myPyDatagram.addString(json.dumps(walkables))
        myPyDatagram.addString(json.dumps(path))
        self.cWriter.send(myPyDatagram, player)

    def WAIT_PASSIVE(self, charid, direction, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('WAIT_PASSIVE')
        myPyDatagram.addString(charid)
        myPyDatagram.addUint8(direction)
        self.cWriter.send(myPyDatagram, player)

    def ATTACKABLES_LIST(self, charid, attackables, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('ATTACKABLES_LIST')
        myPyDatagram.addString(charid)
        myPyDatagram.addString(json.dumps(attackables))
        self.cWriter.send(myPyDatagram, player)

    def ATTACK_SUCCESS(self, charid1, charid2, damages, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('ATTACK_SUCCESS')
        myPyDatagram.addString(charid1)
        myPyDatagram.addString(charid2)
        myPyDatagram.addUint8(damages)
        self.cWriter.send(myPyDatagram, player)

    def ATTACK_PASSIVE(self, charid1, charid2, damages, attackables, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('ATTACK_PASSIVE')
        myPyDatagram.addString(charid1)
        myPyDatagram.addString(charid2)
        myPyDatagram.addUint8(damages)
        myPyDatagram.addString(json.dumps(attackables))
        self.cWriter.send(myPyDatagram, player)

    def START_BATTLE(self, party, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('START_BATTLE')
        myPyDatagram.addString32(json.dumps(party))
        self.cWriter.send(myPyDatagram, player)

    def UPDATE_PARTY_LIST(self, parties, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('UPDATE_PARTY_LIST')
        myPyDatagram.addString32(json.dumps(parties))
        self.cWriter.send(myPyDatagram, player)

    def WAIT_SUCCESS(self, player):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('WAIT_SUCCESS')
        self.cWriter.send(myPyDatagram, player)