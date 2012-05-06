import Move

# Return the list of walkable tile for a character to a client
def execute(server, iterator, source):
    charid = iterator.getString()
    party = server.parties[server.sessions[source]['party']]
    walkables = Move.GetWalkables( party, charid )

    server.send.WALKABLES_LIST(charid, walkables, source)