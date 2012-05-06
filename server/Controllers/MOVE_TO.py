import Move, Character

# A player wants to move one of its units
def execute(server, iterator, source):
    charid = iterator.getString()
    x2 = iterator.getUint8()
    y2 = iterator.getUint8()
    z2 = iterator.getUint8()
    
    party = server.parties[server.sessions[source]['party']]
    
    orig = Character.Coords( party, charid )
    x1 = orig[0]
    y1 = orig[1]
    z1 = orig[2]

    path = Move.GetPath( party, charid, x1, y1, z1, x2, y2, z2 )
    walkables = Move.GetWalkables( party, charid )

    del party['map']['tiles'][x1][y1][z1]['char']
    party['map']['tiles'][x2][y2][z2]['char'] = charid

    party['chars'][charid]['direction'] = Move.GetNewDirection( x1, y1, x2, y2 )
    party['chars'][charid]['canmove'] = False
    
    server.send.MOVED(charid, x2, y2, z2, source)
    
    for playerid,playerlogin in enumerate(party['players']):
        if playerid != server.sessions[source]['player']:
            server.send.MOVED_PASSIVE(charid, walkables, path, server.players[playerlogin])