import Move

# Returns a list of tiles to display the walkable zone of an enemy while in passive mode
def execute(server, iterator, source):
    charid = iterator.getString()
    party = server.parties[server.sessions[source]['party']]
    walkables = Move.GetWalkables( party, charid )
    
    server.send.PASSIVE_WALKABLES_LIST(charid, walkables, source)