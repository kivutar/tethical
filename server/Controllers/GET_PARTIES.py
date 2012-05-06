from copy import deepcopy

# Return party list to a client
def execute(server, iterator, source):
    server.playersinlobby.append(source)

    parties = deepcopy(server.parties)
    for party in parties.values():
        del party['map']['tiles']

    server.send.PARTY_LIST(parties, source)