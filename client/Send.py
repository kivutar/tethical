from direct.distributed.PyDatagram import PyDatagram, ConnectionWriter
import json

# Datagrams to be sent to the server
class Send(object):

    def __init__(self, cManager, myConnection):
        self.cWriter = ConnectionWriter(cManager, 0)
        self.cWriter.setTcpHeaderSize(4)
        self.myConnection = myConnection

    # Get the path from the server, and makes the character walk on it
    def GET_PATH(self, charid, dest):
        (x, y, z) = dest
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('GET_PATH')
        myPyDatagram.addString(charid)
        myPyDatagram.addUint8(x)
        myPyDatagram.addUint8(y)
        myPyDatagram.addUint8(z)
        self.cWriter.send(myPyDatagram, self.myConnection)

    # Send the MOVE_TO packet and update the map tags with new char coords
    def MOVE_TO(self, charid, dest):
        (x2, y2, z2) = dest
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('MOVE_TO')
        myPyDatagram.addString(charid)
        myPyDatagram.addUint8(x2)
        myPyDatagram.addUint8(y2)
        myPyDatagram.addUint8(z2)
        self.cWriter.send(myPyDatagram, self.myConnection)

    # Send the ATTACK packet, get the returned damages and display the attack animation
    def ATTACK(self, charid, targetid):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('ATTACK')
        myPyDatagram.addString(charid)
        myPyDatagram.addString(targetid)
        self.cWriter.send(myPyDatagram, self.myConnection)

    # The team is formed, send the formation data to the server
    def FORMATION_READY(self, formation):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('FORMATION_READY')
        myPyDatagram.addString(json.dumps(formation))
        self.cWriter.send(myPyDatagram, self.myConnection)

    def GET_PARTIES(self):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('GET_PARTIES')
        self.cWriter.send(myPyDatagram, self.myConnection)

    def GET_MAPS(self):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('GET_MAPS')
        self.cWriter.send(myPyDatagram, self.myConnection)

    # Send the party details to the server in order to instanciate a party
    def CREATE_PARTY(self, mapname):
        import time
        partyname = str(int(time.time()))
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('CREATE_PARTY')
        myPyDatagram.addString(partyname)
        myPyDatagram.addString(mapname)
        self.cWriter.send(myPyDatagram, self.myConnection)

    # Join a party
    def JOIN_PARTY(self, name):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('JOIN_PARTY')
        myPyDatagram.addString(name)
        self.cWriter.send(myPyDatagram, self.myConnection)

    # Try to log into the server
    def LOGIN_MESSAGE(self, login, password):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('LOGIN_MESSAGE')
        myPyDatagram.addString(login)
        myPyDatagram.addString(password)
        self.cWriter.send(myPyDatagram, self.myConnection)

    # The battle main dispatcher, see it as a "next turn"
    def UPDATE_PARTY(self):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('UPDATE_PARTY')
        self.cWriter.send(myPyDatagram, self.myConnection)

    def GET_PASSIVE_WALKABLES(self, charid):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('GET_PASSIVE_WALKABLES')
        myPyDatagram.addString(charid)
        self.cWriter.send(myPyDatagram, self.myConnection)

    # Move button clicked
    def GET_WALKABLES(self, charid):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('GET_WALKABLES')
        myPyDatagram.addString(charid)
        self.cWriter.send(myPyDatagram, self.myConnection)

    def GET_ATTACKABLES(self, charid):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('GET_ATTACKABLES')
        myPyDatagram.addString(charid)
        self.cWriter.send(myPyDatagram, self.myConnection)

    # The direction has been chosen, send the WAIT datagram
    def WAIT(self, charid, direction):
        myPyDatagram = PyDatagram()
        myPyDatagram.addString('WAIT')
        myPyDatagram.addString(charid)
        myPyDatagram.addUint8(direction)
        self.cWriter.send(myPyDatagram, self.myConnection)