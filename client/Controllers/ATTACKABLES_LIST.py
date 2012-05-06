import json

def execute(client, iterator):
    charid = iterator.getString()
    attackables = json.loads(iterator.getString())

    client.setPhase('tile')
    client.subphase = 'attack'
    client.matrix.setupAttackableZone(charid, attackables)
    if client.charcard:
        client.charcard.hide()