import random

def Coords( mp, char ):
    
    for x in range( mp['x'] ):
        for y in range( mp['y'] ):
            for z in range( mp['z'] ):
                
                tile = mp['tiles'][x][y][z]
                
                if tile and tile.has_key('char') and int(tile['char']) == int(char['id']):
                    return (x, y, z)

def Random( charid, player, direction ):
    race = 'human'
    gender = 'female' if int(player) == 1 else 'male'
    sprite = 'misty' if int(player) == 1 else 'ramza'
    hpmax = random.randint(5, 15)
    mpmax = random.randint(5, 15)
    ctmax = random.randint(90, 100)
    return {  'id': charid
            , 'name': GetRandomName( race, gender )
            , 'job': 'Unknown'
            , 'sign': 1
            , 'hp': hpmax
            , 'hpmax': hpmax
            , 'mp': mpmax
            , 'mpmax': mpmax
            , 'ct': ctmax
            , 'ctmax': ctmax
            , 'lv': random.randint(5, 15)
            , 'exp': random.randint(0, 99)
            , 'team': player
            , 'move': random.randint(3, 5)
            , 'jump': random.randint(5, 7)
            , 'direction': direction
            , 'sprite': sprite
            , 'gender': gender
            , 'active': 0 }

def GetRandomName( race, gender ):
    f = open(race+'_'+gender+'_names.txt', 'r')
    names = f.readlines()
    f.close()
    
    i = random.randint(0, len(names)-1)
    
    return names[i]
