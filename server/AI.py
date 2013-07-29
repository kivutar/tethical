import Move, Wait, Character
import random

def AI( server, iterator, source, charid ):

    party = server.parties[server.sessions[source]['party']]
    chars = party['chars']
    char = chars[charid]

    if char['canmove']:
        walkables = Move.GetWalkables( party, charid )
        (x1, y1, z1) = Character.Coords( party, charid )
        (x2, y2, z2) = walkables[random.randint(0, len(walkables)-1)]

        Move.DoMove( server, source, party, charid, x1, y1, z1, x2, y2, z2 )
    else:
        direction = char['direction'] + 1
        if direction > 4:
            direction = 1

        Wait.DoWait(server, source, charid, direction)