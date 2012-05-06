import json

def execute(client, iterator):
    charid = iterator.getString()
    walkables = json.loads(iterator.getString())
    if walkables:
        client.clicked_snd.play()
        client.matrix.setupPassiveWalkableZone(walkables)
        client.subphase = 'passivewalkables'
    else:
        #TODO: show message "no walkable tile"
        print "no walkable tile"
        client.send.UPDATE_PARTY()