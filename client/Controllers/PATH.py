from direct.interval.IntervalGlobal import Sequence, Func
import json
import SequenceBuilder

def execute(client, iterator):
    charid = iterator.getString()
    orig = json.loads(iterator.getString())
    origdir = iterator.getUint8()
    dest = json.loads(iterator.getString())
    path = json.loads(iterator.getString())

    seq = Sequence()
    seq.append( Func(client.at.hide) )
    seq.append( Func(client.updateSpriteAnimation, charid, 'run') )
    seq.append( Func(client.matrix.clearZone) )
    seq.append( SequenceBuilder.characterMoveSequence(client, charid, path) )
    seq.append( Func(client.updateSpriteAnimation, charid) )
    seq.append( Func(client.moveCheck, charid, orig, origdir, dest) )
    seq.start()