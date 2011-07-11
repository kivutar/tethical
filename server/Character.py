import json, random

jobs = {}
jobids = ['4C']
for jobid in jobids:
    f = open('jobs/'+jobid+'.json', 'r')
    jobs[jobid] = json.loads(f.read())
    f.close()

def Coords( party, charid ):
    
    for x in range( party['map']['x'] ):
        for y in range( party['map']['y'] ):
            for z in range( party['map']['z'] ):
                
                tile = party['map']['tiles'][x][y][z]
                
                if tile and tile.has_key('char') and int(tile['char']) == int(charid):
                    return (x, y, z)

def Random( charid, teamid, direction ):
    jobid = jobids[random.randint(0, len(jobids)-1)]
    job = jobs[jobid]
    gender = 'F'#('F','M')[random.randint(0, 1)]
    sprite = str(jobid)+'_'+str(gender)+'_'+str(teamid)

    if gender == 'F':
        rhp = random.randint(458752, 491519)
        rmp = random.randint(245760, 262143)
        rsp = 98304
        rpa = 65536
        rma = 81920
    elif gender == 'M':
        rhp = random.randint(491520, 524287)
        rmp = random.randint(229376, 245759)
        rsp = 98304
        rpa = 81920
        rma = 65536

    hp = rhp * job['hpm'] / 1638400
    mp = rmp * job['mpm'] / 1638400
    sp = rsp * job['spm'] / 1638400
    pa = rpa * job['pam'] / 1638400
    ma = rma * job['mam'] / 1638400

    lv = random.randint(10, 15)
    for l in range(1, lv+1):
        hp = hp + ( hp / (job['hpc'] + l) )
        mp = mp + ( mp / (job['mpc'] + l) )
        sp = sp + ( sp / (job['spc'] + l) )
        pa = pa + ( pa / (job['pac'] + l) )
        ma = ma + ( ma / (job['mac'] + l) )

    return {  'id': charid
           , 'name': GetRandomName(gender)
           , 'job': job['name']
           , 'sign': 1
           , 'br': random.randint(45, 74)
           , 'fa': random.randint(45, 74)
           , 'hp': hp
           , 'hpmax': hp
           , 'mp': mp
           , 'mpmax': mp
           , 'speed': sp
           , 'pa': pa
           , 'ma': ma
           , 'ct': random.randint(0, 100)
           , 'lv': lv
           , 'exp': random.randint(0, 99)
           , 'team': teamid
           , 'move': job['move']
           , 'jump': job['jump']*2
           , 'direction': direction
           , 'sprite': sprite
           , 'gender': gender
           , 'active': 0
           }

def GetRandomName( gender ):
    f = open(gender+'_names.txt', 'r')
    names = f.readlines()
    f.close()
    
    i = random.randint(0, len(names)-1)
    
    return names[i]

