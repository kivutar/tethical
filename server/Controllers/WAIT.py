# End of the turn of a unit
def execute(server, iterator, source):
    charid = iterator.getString()
    direction = iterator.getUint8()
    
    party = server.parties[server.sessions[source]['party']]
    char = party['chars'][charid]

    if char['canmove'] and char['canact']:
        char['ct'] = char['ct'] - 60
    elif char['canmove'] or char['canact']:
        char['ct'] = char['ct'] - 80
    else:
        char['ct'] = char['ct'] - 100

    char['direction'] = direction

    char['active'] = False
    char['canmove'] = False
    char['canact'] = False

    server.send.WAIT_SUCCESS(source)

    for playerid,playerlogin in enumerate(party['players']):
        if playerid != server.sessions[source]['player']:
            server.send.WAIT_PASSIVE(charid, direction, server.players[playerlogin])