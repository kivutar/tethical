from direct.gui.DirectGui import DirectFrame
from direct.interval.IntervalGlobal import Sequence, LerpColorInterval, Func
import json

# The teams are ready for the battle, stop the lobby BGM and initiate the battle
def execute(client, iterator):
    client.party = json.loads(iterator.getString32())
    client.transitionframe = DirectFrame( frameSize = ( -2, 2, -2, 2 ) )
    client.transitionframe.setTransparency(True)
    seq = Sequence()
    seq.append(LerpColorInterval(client.transitionframe, 2, (0,0,0,1), startColor=(0,0,0,0)))
    seq.append(Func(client.background.frame.destroy))
    seq.append(Func(client.music.stop))
    seq.append(Func(client.battle_init))
    seq.start()