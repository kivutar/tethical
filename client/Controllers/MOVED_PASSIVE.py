from direct.interval.IntervalGlobal import Sequence, Func, Wait
import json
import SequenceBuilder

def execute(client, iterator):
    charid = iterator.getString()
    walkables = json.loads(iterator.getString())
    path = json.loads(iterator.getString())

    client.inputs.ignoreAll()
    (x1, y1, z1) = path[0]
    (x2, y2, z2) = path[-1]
    del client.party['map']['tiles'][x1][y1][z1]['char']
    client.party['map']['tiles'][x2][y2][z2]['char'] = charid
    seq = Sequence()
    seq.append( Func(client.matrix.setupPassiveWalkableZone, walkables) )
    seq.append( Wait(0.5) )
    seq.append( Func(client.updateCursorPos, (x2, y2, z2)) )
    seq.append( Wait(0.5) )
    seq.append( Func(client.at.hide) )
    seq.append( Func(client.updateSpriteAnimation, charid, 'run') )
    seq.append( Func(client.camhandler.move, client.battleGraphics.logic2terrain((x2, y2, z2))) )
    seq.append( SequenceBuilder.characterMoveSequence(client, charid, path) )
    seq.append( Wait(0.5) )
    seq.append( Func(client.updateSpriteAnimation, charid) )
    seq.append( Func(client.matrix.clearZone) )
    seq.append( Func(client.at.showOnSprite, client.matrix.sprites[charid]) )
    seq.start()