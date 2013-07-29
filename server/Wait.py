def DoWait(server, source, charid, direction):
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

    if char['ai']:
        for playerid,playerlogin in enumerate(party['players']):
            server.send.WAIT_PASSIVE(charid, direction, server.players[playerlogin])
    else:
        server.send.WAIT_SUCCESS(source)
        for playerid,playerlogin in enumerate(party['players']):
            if playerid != server.sessions[source]['player']:
                server.send.WAIT_PASSIVE(charid, direction, server.players[playerlogin])