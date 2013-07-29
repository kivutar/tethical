import AI

# The most important controller
def execute(server, iterator, source):
    party = server.parties[server.sessions[source]['party']]
    chars = party['chars']

    # Compute the number of teams with alive chars in the party
    aliveteams = {}
    for charid in chars.keys():
        if chars[charid]['hp'] > 0:
            if aliveteams.has_key(chars[charid]['team']):
                aliveteams[chars[charid]['team']] = aliveteams[chars[charid]['team']] + 1
            else:
                aliveteams[chars[charid]['team']] = 1

    # Be sure that all clients are ready to go on before continuing the CT algo
    server.readysources[party['name']].add(source)
    if len(server.readysources[party['name']]) < len(aliveteams):
        return
    else:
        server.readysources[party['name']].remove(source)

    # If we already have a char tagged with 'active', it is still its turn,
    # let's update its party info and let him play again
    for charid in chars.keys():
        if chars[charid]['active']:
            party['yourturn'] = int(chars[charid]['team']) == int(server.sessions[source]['player'])
            server.send.PARTY_UPDATED(party['yourturn'], chars, source)
            if chars[charid]['ai']:
                AI.AI(server, iterator, source, charid)
            return

    # Code to trigger game over or battle complete
    if len(aliveteams) < 2:
        for client in party['players']:
            if source == server.players[client]:
                server.send.BATTLE_COMPLETE(server.players[client])
            else:
                server.send.GAME_OVER(server.players[client])
        del server.parties[server.sessions[source]['party']]
        server.updateAllPartyLists()
        return
    
    # The CT algo
    while True:
        for charid in chars.keys():
            char = chars[charid]
            char['ct'] = char['ct'] + char['speed']
            if char['ct'] >= 100:
                if char['hp'] > 0:
                    char['active'] = True
                    char['canmove'] = True
                    char['canact'] = True
                    for playerid,playerlogin in enumerate(party['players']):
                        source = server.players[playerlogin]
                        party['yourturn'] = int(chars[charid]['team']) == int(server.sessions[source]['player'])
                        server.send.PARTY_UPDATED(party['yourturn'], chars, source)
                    if chars[charid]['ai']:
                        AI.AI(server, iterator, source, charid)
                    return
                else:
                    char['ct'] = 0
