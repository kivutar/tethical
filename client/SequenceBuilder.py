from direct.interval.IntervalGlobal import *
import GUI

def battleIntroduction(client):
    seq = Sequence()
    i1 = LerpColorInterval(client.transitionframe, 5, (0,0,0,0), startColor=(0,0,0,1))
    cx, cy, cz = client.battleGraphics.terrain.getBounds().getCenter()
    i2 = LerpPosInterval(client.camhandler.container, 5, (cx,cy,cz), startPos=(cx,cy,cz+50))
    ch, cp, cr = client.camhandler.container.getHpr()
    i3 = LerpHprInterval(client.camhandler.container, 5, (ch+90, cp, cr), (ch-180, cp, cr))
    p1 = Parallel(i1,i2,i3)
    seq.append(p1)
    seq.append(Func(client.transitionframe.destroy))
    seq.append(Wait(1))
    seq.append(Func(client.updateAllSpritesAnimations, 'walk'))
    seq.append(Func(lambda: GUI.BrownOverlay(GUI.ConditionsForWinning, client.send.UPDATE_PARTY)))
    return seq

# Returns the sequence of a character punching another
def characterAttackSequence(client, charid, targetid):
    seq = Sequence()
    seq.append( Func(client.at.hide) )
    seq.append( Func(client.characterLookAt,       charid, targetid) )
    seq.append( Func(client.updateSpriteAnimation, charid, 'attack') )
    seq.append( Wait(0.5) )
    seq.append( Func(client.updateSpriteAnimation, targetid, 'hit') )
    seq.append( Func(client.attack_snd.play) )
    seq.append( Wait(0.5) )
    seq.append( Func(client.updateSpriteAnimation, charid) )
    seq.append( Wait(0.5) )
    seq.append( Func(client.updateSpriteAnimation, targetid) )
    seq.append( Wait(0.5) )
    seq.append( Func(client.matrix.clearZone) )
    return seq

# Returns a sequence showing the character moving through a path
def characterMoveSequence(client, charid, path):
    sprite = client.matrix.sprites[charid]
    seq = Sequence()
    origin = False
    for destination in path:
        if origin:

            (x1, y1, z1) = origin
            (x2, y2, z2) = destination

            # first, face the right direction
            if x2 > x1:
                d = 1
            elif x2 < x1:
                d = 3
            elif y2 > y1:
                d = 2
            elif y2 < y1:
                d = 4
            seq.append( Func(sprite.setRealDir, d) )

            # then, add the move animation from one tile to the next
            if z2 - z1 >= 4:
                middle = (
                    origin[0] + (destination[0] - origin[0]) / 2.0,
                    origin[1] + (destination[1] - origin[1]) / 2.0,
                    destination[2] + 0.5
                )
                seq.append(
                    Sequence(
                        Func(client.updateSpriteAnimation, charid, 'smalljump'),
                        LerpPosInterval(
                            sprite.node, 
                            0.125,
                            client.battleGraphics.logic2terrain(middle), 
                            startPos=client.battleGraphics.logic2terrain(origin)
                        ),
                        LerpPosInterval(
                            sprite.node, 
                            0.125,
                            client.battleGraphics.logic2terrain(destination), 
                            startPos=client.battleGraphics.logic2terrain(middle)
                        ),
                        Func(client.updateSpriteAnimation, charid, 'run'),
                    )
                )
            elif z1 - z2 >= 4:
                middle = (
                    origin[0] + (destination[0] - origin[0]) / 2.0,
                    origin[1] + (destination[1] - origin[1]) / 2.0,
                    origin[2] + 0.5
                )
                seq.append(
                    Sequence(
                        Func(client.updateSpriteAnimation, charid, 'smalljump'),
                        LerpPosInterval(
                            sprite.node, 
                            0.125,
                            client.battleGraphics.logic2terrain(middle), 
                            startPos=client.battleGraphics.logic2terrain(origin)
                        ),
                        LerpPosInterval(
                            sprite.node, 
                            0.125,
                            client.battleGraphics.logic2terrain(destination), 
                            startPos=client.battleGraphics.logic2terrain(middle)
                        ),
                        Func(client.updateSpriteAnimation, charid, 'run'),
                    )
                )
            else:
                seq.append(
                    LerpPosInterval(
                        sprite.node, 
                        0.25,
                        client.battleGraphics.logic2terrain(destination), 
                        startPos=client.battleGraphics.logic2terrain(origin)
                    )
                )
        origin = destination
    return seq