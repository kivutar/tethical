from Config import GAME
import json, GUI

def execute(client, iterator):
    tilesets = json.loads(iterator.getString32())
    characters = json.loads(iterator.getString32())
    client.music.stop()
    client.music = base.loader.loadSfx(GAME+'/music/11.ogg')
    client.music.play()
    GUI.Formation(client.background.frame, tilesets, characters, client.send.FORMATION_READY)