from direct.interval.IntervalGlobal import Sequence, Func, Wait
import SequenceBuilder
import json

def execute(client, iterator):
    charid = iterator.getString()
    targetid = iterator.getString()
    damages = iterator.getUint8()
    attackables = json.loads(iterator.getString())

    print damages
    target = client.party['chars'][targetid]
    target['hp'] = target['hp'] - damages
    if target['hp'] < 0:
        target['hp'] = 0

    client.inputs.ignoreAll()
    seq = Sequence()
    seq.append( Func(client.matrix.setupAttackableZone, charid, attackables) )
    seq.append( Wait(0.5) )
    seq.append( Func(client.updateCursorPos, client.matrix.getCharacterCoords(targetid)) )
    seq.append( Func(client.camhandler.move, client.battleGraphics.logic2terrain(client.matrix.getCharacterCoords(targetid))) )
    seq.append( Wait(0.5) )
    seq.append( SequenceBuilder.characterAttackSequence(client, charid, targetid) )
    seq.append( Func(client.camhandler.move, client.battleGraphics.logic2terrain(client.matrix.getCharacterCoords(charid))) )
    seq.start()