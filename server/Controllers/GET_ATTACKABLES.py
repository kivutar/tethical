import Attack

# Return the list of tiles that a unit can attack
def execute(server, iterator, source):
    charid = iterator.getString()
    
    party = server.parties[server.sessions[source]['party']]
    
    attackables = Attack.GetAttackables( party, charid )

    server.send.ATTACKABLES_LIST(charid, attackables, source)