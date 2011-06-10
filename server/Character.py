import random

def Coords( party, charid ):
    
    for x in range( party['map']['x'] ):
        for y in range( party['map']['y'] ):
            for z in range( party['map']['z'] ):
                
                tile = party['map']['tiles'][x][y][z]
                
                if tile and tile.has_key('char') and int(tile['char']) == int(charid):
                    return (x, y, z)

def Random( charid, player, direction ):
    race = 'human'
    gender = ('F','M')[random.randint(0, 1)]
    job = random.randint(0, 7)
    sprite = str(job)+'_'+str(gender)
    hpmax = random.randint(5, 15)
    mpmax = random.randint(5, 15)
    return {  'id': charid
            , 'name': GetRandomName( race, gender )
            , 'job': 'Unknown'
            , 'sign': 1
            , 'hp': hpmax
            , 'hpmax': hpmax
            , 'mp': mpmax
            , 'mpmax': mpmax
            , 'ct': random.randint(0, 100)
            , 'speed': random.randint(8, 20)
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
