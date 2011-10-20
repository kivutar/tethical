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

# GUI.Blueprint('menu1')

# char = {
#     'sprite': '4A_F_1',
#     'lv': 15,
#     'exp': 20,
#     'hp': 205,
#     'hpmax': 245,
#     'mp': 30,
#     'mpmax': 30,
#     'ct': 20
# }
# GUI.CharBarsLeft(char)

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

# GUI.Blueprint('formation0')

# def foo():
# 	pass

# chars = [
# {
# 	'name': 'Kivu',
# 	'job': 'Kivu',
# 	'team': 1,
# 	'sign': 1,
#     'sprite': '4A_F_0',
#     'lv': 15,
#     'exp': 0,
#     'hp': 225,
#     'hpmax': 225,
#     'mp': 32,
#     'mpmax': 36,
#     'ct': 50,
#     'br': 12,
#     'fa': 13,
# },
# {
# 	'name': 'Kivy',
# 	'job': 'Kivy',
# 	'team': 1,
# 	'sign': 1,
#     'sprite': '4A_F_0',
#     'lv': 15,
#     'exp': 0,
#     'hp': 225,
#     'hpmax': 225,
#     'mp': 32,
#     'mpmax': 36,
#     'ct': 50,
#     'br': 12,
#     'fa': 13,
# },
# ]

# tileset = {
#     "capacity": 4,
#     "direction": 2,
#     "maping": [
#         [ None   , None   , None   , None   , None    ],
#         [ None   , None   , None   , None   , None    ],
#         [ None   , [3,0,4], [4,0,4], [5,0,4], [6,0,4] ],
#         [ None   , None   , None   , None   , None    ],
#         [ None   , None   , None   , None   , None    ]
#     ]
# }

# GUI.Formation(render, tileset, chars, foo)

GUI.Blueprint('actionpreview')

char1 = {
	'name': 'Kivu',
	'job': 'Kivu',
	'team': 1,
	'sign': 1,
    'sprite': '4A_F_0',
    'lv': 15,
    'exp': 0,
    'hp': 225,
    'hpmax': 225,
    'mp': 32,
    'mpmax': 36,
    'ct': 50,
    'br': 12,
    'fa': 13,
}

char2 = {
	'name': 'Kivy',
	'job': 'Kivy',
	'team': 1,
	'sign': 1,
    'sprite': '4A_F_0',
    'lv': 15,
    'exp': 0,
    'hp': 225,
    'hpmax': 225,
    'mp': 32,
    'mpmax': 36,
    'ct': 50,
    'br': 12,
    'fa': 13,
}

def foo():
	pass

GUI.ActionPreview(char1, char2, 25, 96, foo, foo)

run()
