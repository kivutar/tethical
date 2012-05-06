import Map

# A player tries to create a party.
def execute(server, iterator, source):
    name = iterator.getString()
    mapname = iterator.getString()
    
    party = {
        'name': name,
        'mapname': mapname,
        'map' : Map.load(mapname),
        'chars': {},
        'log': {},
        'creator': server.sessions[source]['login'],
        'players': [],
        'formations': [],
    }
    party['players'].append(server.sessions[source]['login'])

    server.parties[name] = party
    server.sessions[source]['party'] = name
    server.sessions[source]['player'] = len(party['players'])-1
    
    server.updateAllPartyLists()
    
    print server.sessions[source]['login'], "created the party", name, "using the map", mapname
    server.send.PARTY_CREATED(party, source)