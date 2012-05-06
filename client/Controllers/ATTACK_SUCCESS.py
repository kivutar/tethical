from direct.interval.IntervalGlobal import Sequence, Func

def execute(client, iterator):
    charid = iterator.getString()
    targetid = iterator.getString()
    damages = iterator.getUint8()

    print damages
    target = client.party['chars'][targetid]
    target['hp'] = target['hp'] - damages
    if target['hp'] < 0:
        target['hp'] = 0

    seq = Sequence()
    seq.append( client.getCharacterAttackSequence(charid, targetid) )
    seq.append( Func(client.send.UPDATE_PARTY) )
    seq.start()