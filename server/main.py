from panda3d.core import loadPrcFile
loadPrcFile("config.prc")
import direct.directbase.DirectStart
from direct.task.Task import Task
from direct.distributed.PyDatagramIterator import *
import sys
from copy import deepcopy
from Send import Send
from Controllers import *

class Server:

    def __init__(self):

        self.activeConnections = [] # lists all connections
        self.players = {} # keys are the players logins, values are the players datagram connections
        self.parties = {} # keys are the parties names, values are dicts representing parties data
        self.sessions = {} # keys are the datagram connections, values are dicts storing the characters of the player and its party
        self.playersinlobby = [] # lists players in the party screen
        self.charid = 0 # used for random team generation
        self.chars = [] # lists of dicts representing characters data
        self.readysources = {}

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

    def processData(self, datagram):
        iterator = PyDatagramIterator(datagram)
        source = datagram.getConnection()
        callback = iterator.getString()
        getattr(globals()[callback], 'execute')(self, iterator, source)

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