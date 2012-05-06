# A client is trying to join a party
def execute(server, iterator, source):
    name = iterator.getString()
    party = server.parties[name]
    
    if len(party['players']) >= len(party['map']['tilesets']):
        parties = deepcopy(server.parties)
        for party in parties.values():
            del party['map']['tiles']
        server.send.PARTY_JOIN_FAIL(name, parties, source)
    else:
        party['players'].append(server.sessions[source]['login'])
        server.sessions[source]['party'] = name
        server.sessions[source]['player'] = len(party['players'])-1
        server.playersinlobby.remove(source)

        print server.sessions[source]['login'], "joined the party", name
        server.send.PARTY_JOINED(party, source)

        if len(party['players']) == len(party['map']['tilesets']):
            for tilesetid,player in enumerate(party['players']):
                server.send.START_FORMATION(party['map']['tilesets'][tilesetid], server.sessions[server.players[player]]['characters'], server.players[player])

        server.updateAllPartyLists()