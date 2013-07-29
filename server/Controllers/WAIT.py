import Wait

# End of the turn of a unit
def execute(server, iterator, source):
    charid = iterator.getString()
    direction = iterator.getUint8()
    
    Wait.DoWait(server, source, charid, direction)