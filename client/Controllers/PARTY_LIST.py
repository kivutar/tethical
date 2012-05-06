import json, GUI

# Party list data received, display the party list GUI
def execute(client, iterator):
    parties = json.loads(iterator.getString32())
    client.partylistwindow = GUI.PartyListWindow(client.send.JOIN_PARTY, client.send.GET_MAPS)
    client.partylistwindow.refresh(parties)