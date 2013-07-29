from direct.interval.IntervalGlobal import Sequence, Func, Wait

def execute(client, iterator):
    charid = iterator.getString()
    direction = iterator.getUint8()

    pos = client.matrix.getCharacterCoords(charid)
    
    client.inputs.ignoreAll()
    seq = Sequence()
    seq.append( Func(client.camhandler.move, client.battleGraphics.logic2terrain(pos)) )
    seq.append( Func(client.at.hide) )
    seq.append( Wait(0.5) )
    seq.append( Func(client.matrix.sprites[charid].setRealDir, direction) )
    seq.append( Wait(0.5) )
    seq.append( Func(client.inputs.ignoreAll) )
    seq.append( Func(client.send.UPDATE_PARTY) )
    seq.start()