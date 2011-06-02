import math
import Character

def GetAttackables ( party, charid ):

    t1 = Character.Coords( party, charid )
    (x1, y1, z1) = t1
    
    a = []
    for tx in ( (x1-1, y1), (x1+1, y1), (x1, y1-1), (x1, y1+1) ):

        try:
            (x2, y2) = tx
            t2 = party['map']['tiles'][x2][y2]
            if t2 and x2 >= 0 and y2 >= 0:
                for z2,t3 in enumerate(t2):
                    if t3 and t3['walkable'] and t3['selectable'] and math.fabs(z2-z1) <= 4:
                        a.append( (x2, y2, z2) )
        except:
            pass

    return a

def IsAttackable( party, charid1, charid2 ):

    attackables = GetAttackables( party, charid1 )
    
    tile2 = Character.Coords( party, charid2 )
    
    return tile2 in attackables

