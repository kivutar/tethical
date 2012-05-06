import json

# A team is complete. See if all teams are complete, and if so, start the battle
def execute(server, iterator, source):
    formation = json.loads(iterator.getString())

    party = server.parties[server.sessions[source]['party']]
    party['formations'].append(formation)

    if len(party['formations']) == len(party['map']['tilesets']):

        for team,formation in enumerate(party['formations']):
            for line in formation:
                x, y, z = line['coords']
                charid = line['charid']
                party['map']['tiles'][x][y][z]['char'] = str(charid)
                char = filter(lambda x: x['id'] == charid, server.chars)[0]
                char['team'] = team
                char['direction'] = line['direction']
                party['chars'][str(charid)] = char

        for playerlogin in party['players']:
            server.send.START_BATTLE(party, server.players[playerlogin])