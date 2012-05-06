import json, GUI

# The client failed at joining a party, display a new party list window
def execute(client, iterator):
    print iterator.getString()
    parties = json.loads(iterator.getString32())
    client.partylistwindow = GUI.PartyListWindow(client.send.JOIN_PARTY, client.send.GET_MAPS)
    client.partylistwindow.refresh(parties)