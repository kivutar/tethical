import json, GUI

# Receive map list, display the map chooser
def execute(client, iterator):
    maps = json.loads(iterator.getString())
    client.mapchooserwindow = GUI.MapChooser(maps, client.background.frame, client.send.CREATE_PARTY, client.send.GET_PARTIES)
