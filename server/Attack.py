import math
import Character

def GetAttackables ( mp, char ):

    t1 = Character.Coords( mp, char )
    (x1, y1, z1) = t1
    
    a = []
    for tx in ( (x1-1, y1), (x1+1, y1), (x1, y1-1), (x1, y1+1) ):

        try:
            (x2, y2) = tx
            t2 = mp['tiles'][x2][y2]
            if t2 and x2 >= 0 and y2 >= 0:
                for z2,t3 in enumerate(t2):
                    if t3 and t3['walkable'] and t3['selectable'] and math.fabs(z2-z1) <= 4:
                        a.append( (x2, y2, z2) )
        except:
            pass

    return a

def IsAttackable( mp, char1, char2 ):

    attackables = GetAttackables( mp, char1 )
    
    tile2 = Character.Coords( mp, char2 )
    
    return tile2 in attackables

