
def Coords( mp, char ):
    
    for x in range( mp['x'] ):
        for y in range( mp['y'] ):
            for z in range( mp['z'] ):
                
                tile = mp['tiles'][x][y][z]
                
                if tile and tile.has_key('char') and int(tile['char']) == int(char['id']):
                    return (x, y, z)

