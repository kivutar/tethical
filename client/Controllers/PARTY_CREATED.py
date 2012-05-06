import json

# Your party has been created server side. Put the party data in the client instance
def execute(client, iterator):
    party = json.loads(iterator.getString32())
    client.party = party