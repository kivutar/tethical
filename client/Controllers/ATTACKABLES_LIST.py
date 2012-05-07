import json

def execute(client, iterator):
    charid = iterator.getString()
    attackables = json.loads(iterator.getString())

    client.setupAttackableTileChooser(charid, attackables)