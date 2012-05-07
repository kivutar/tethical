from Config import *
import json, GUI

def execute(client, iterator):
    charid = iterator.getString()
    walkables = json.loads(iterator.getString())
    if walkables:
        client.inputs.ignoreAll()
        GUI.Help(
            0, 25, 142, 60,
            'shadowed', 'Check',
            'Specify the point to move with\nthe cursor. Press the %c button\nto select.' % CIRCLE_BTN.upper(),
            lambda: client.setupWalkableTileChooser(charid, walkables),
            client.send.UPDATE_PARTY,
        )
    else:
        #TODO: show message "no walkable tile"
        print "no walkable tile"
        client.send.UPDATE_PARTY()