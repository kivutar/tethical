from panda3d.core import loadPrcFile
loadPrcFile("config.prc")
from pandac.PandaModules import ConfigVariableString
import os
import Map
GAME = ConfigVariableString('game', 'fft').getValue()

# Return map list to a client
def execute(server, iterator, source):
    server.playersinlobby.remove(source)

    mapnames = map( lambda m: m.split('.')[0], os.listdir(GAME+'/maps'))

    maps = []
    for mapname in mapnames:
        mp = Map.load(mapname)
        del mp['tiles']
        maps.append(mp)

    server.send.MAP_LIST(maps, source)