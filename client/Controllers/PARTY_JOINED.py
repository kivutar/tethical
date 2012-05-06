import json

# You joined a party
def execute(client, iterator):
    party = json.loads(iterator.getString32())
    client.party = party