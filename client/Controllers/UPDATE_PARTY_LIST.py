import json

# Party list has been updated, refresh the party list window
def execute(client, iterator):
    parties = json.loads(iterator.getString32())
    client.partylistwindow.refresh(parties)