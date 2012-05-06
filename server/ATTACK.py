import Attack

# A unit is attacking another
def execute(server, iterator, source):
    charid1 = iterator.getString()
    charid2 = iterator.getString()
    party = server.parties[server.sessions[source]['party']]
    char1 = party['chars'][charid1]
    char2 = party['chars'][charid2]
    
    damages = char1['pa'] * char1['br'] / 100 * char1['pa']
    
    char2['hp'] = char2['hp'] - damages*4
    if char2['hp'] < 0:
        char2['hp'] = 0
    
    char1['canact'] = False
    
    server.send.ATTACK_SUCCESS(charid1, charid2, damages, source)
    
    attackables = Attack.GetAttackables( party, charid1 )
    
    for playerid,playerlogin in enumerate(party['players']):
        if playerid != server.sessions[source]['player']:
            server.send.ATTACK_PASSIVE(charid1, charid2, damages, attackables, server.players[playerlogin])