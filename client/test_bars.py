from Config import *
import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
import GUI
import os
import os.path
from operator import itemgetter, attrgetter

GUI.Blueprint('menu1')

char = {
    'sprite': '4A_F_1',
    'lv': 15,
    'exp': 20,
    'hp': 205,
    'hpmax': 245,
    'mp': 30,
    'mpmax': 30,
    'ct': 20
}
GUI.CharBarsLeft(char)

# GUI.Blueprint('charbarsright')

# char = {
#     'sprite': '4A_F_0',
#     'lv': 15,
#     'exp': 0,
#     'hp': 225,
#     'hpmax': 225,
#     'mp': 32,
#     'mpmax': 36,
#     'ct': 50
# }
# GUI.CharBarsRight(char)

run()
