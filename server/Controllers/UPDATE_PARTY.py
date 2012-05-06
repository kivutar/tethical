# The most important controller
def execute(server, iterator, source):
    party = server.parties[server.sessions[source]['party']]
    chars = party['chars']
    
    aliveteams = {}
    for charid in chars.keys():
        if chars[charid]['hp'] > 0:
            if aliveteams.has_key(chars[charid]['team']):
                aliveteams[chars[charid]['team']] = aliveteams[chars[charid]['team']] + 1
            else:
                aliveteams[chars[charid]['team']] = 1
    if len(aliveteams) < 2:
        for client in party['players']:
            if source == server.players[client]:
                server.send.BATTLE_COMPLETE(server.players[client])
            else:
                server.send.GAME_OVER(server.players[client])
        del server.parties[server.sessions[source]['party']]
        server.updateAllPartyLists()
        return

    for charid in chars.keys():
        party['yourturn'] = int(chars[charid]['team']) == int(server.sessions[source]['player'])
        if chars[charid]['active']:
            server.send.PARTY_UPDATED(party['yourturn'], chars, source)
            return
    
    while True:
        for charid in chars.keys():
            char = chars[charid]
            char['ct'] = char['ct'] + char['speed']
            if char['ct'] >= 100:
                if char['hp'] > 0:
                    char['active'] = True
                    char['canmove'] = True
                    char['canact'] = True
                    party['yourturn'] = int(chars[charid]['team']) == int(server.sessions[source]['player'])
                    server.send.PARTY_UPDATED(party['yourturn'], chars, source)
                    return
                else:
                    char['ct'] = 0
