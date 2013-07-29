import Move, Character

# A player wants to move one of its units
def execute( server, iterator, source ):
    charid = iterator.getString()
    x2 = iterator.getUint8()
    y2 = iterator.getUint8()
    z2 = iterator.getUint8()
    
    party = server.parties[server.sessions[source]['party']]
    
    orig = Character.Coords( party, charid )
    x1 = orig[0]
    y1 = orig[1]
    z1 = orig[2]

    Move.DoMove( server, source, party, charid, x1, y1, z1, x2, y2, z2 )