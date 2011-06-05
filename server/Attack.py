import math
import Character

def GetAttackables ( party, charid ):

    x1, y1, z1 = Character.Coords( party, charid )
    
    attackables = []
    for x2, y2 in ( (x1-1, y1), (x1+1, y1), (x1, y1-1), (x1, y1+1) ):

        try:
            t2 = party['map']['tiles'][x2][y2]
            if t2 and x2 >= 0 and y2 >= 0:
                for z2,t3 in enumerate(t2):
                    if t3 and t3['walkable'] and t3['selectable'] and math.fabs(z2-z1) <= 4:
                        attackables.append( (x2, y2, z2) )
        except:
            pass

    return attackables

def IsAttackable( party, charid1, charid2 ):
    
    return Character.Coords( party, charid2 ) in GetAttackables( party, charid1 )

