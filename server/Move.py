import math
import Character

def getadjacentwalkables( mp, char, tiles ):
    
    w2 = []

    for t1 in tiles:
        (x1, y1, z1) = t1
        for tx in ( (x1-1, y1), (x1+1, y1), (x1, y1-1), (x1, y1+1) ):
            try:
                (x2, y2) = tx
                t2 = mp['tiles'][x2][y2]
                if t2 and x2 >= 0 and y2 >= 0:
                    for z2,t3 in enumerate(t2):
                        if t3 and (not t3.has_key('char') or t3['char'] == 0) and t3['walkable'] and t3['selectable'] and math.fabs(z2-z1) <= char['jump']:
                            w2.append( (x2, y2, z2) )
            except:
                pass

    return w2

def GetWalkables( mp, char ):

    tile = Character.Coords( mp, char )
    walkables = [ tile ]
    filtered_walkables = []

    for i in range(1, char['move']+1):
        walkables.extend( getadjacentwalkables( mp, char, walkables ) )

    for walkable in walkables:
        if not walkable == tile:
            filtered_walkables.append( walkable )

    return filtered_walkables

def IsWalkable( mp, char, x, y, z ):

    walkables = GetWalkables( mp, char )
    
    return (x, y, z) in walkables

def GetNewDirection( x1, y1, x2, y2 ):

    dx = x2 - x1
    dy = y2 - y1
    
    if math.fabs(dy) > math.fabs(dx):
        return 1 if dy > 0 else 0
    else:
        return 2 if dx > 0 else 3

def GetPath ( mp, char, x1, y1, z1, x2, y2, z2 ):

    tree = { str(x1)+'-'+str(y1)+'-'+str(z1): {} }
    buildtree( mp, char, tree, char['move']-1, str(x2)+'-'+str(y2)+'-'+str(z2) )

    paths = []
    findpathes( tree, [], paths )
    
    pathtoreturn = []
    for tile in paths[0]:
        (x, y, z) = tile.split('-')
        pathtoreturn.append((int(x), int(y), int(z)))

    return pathtoreturn

def buildtree ( mp, char, tree, moves, dest ):
    
    for k1 in tree.keys():

        for adj in getadjacentwalkables( mp, char, [ tuple( map( int, k1.split('-') ) ) ] ):
            k2 = '-'.join( map( str, adj ) )

            if k2 == dest:
                tree[k1][k2] = 'X'
                return
            else:
                tree[k1][k2] = {}

        if moves > 0:
            buildtree( mp, char, tree[k1], moves-1, dest )

def findpathes ( tree, p, paths ):

    for k in tree.keys():
        if tree[k] == 'X':
            paths.append( p + [k] )
        else:
            findpathes( tree[k], p + [k], paths )

