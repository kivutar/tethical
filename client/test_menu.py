from Config import *
import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.DirectGui import *
from pandac.PandaModules import *
import GUI

def exemplecallback(text):
    print "You clicked the row #"+str(text)

def cancelcallback():
    print "Bye"

GUI.Blueprint('menu0')

columns = [
    { 'name': "abilityName", 'label': "Ability", 'x': -93, 'font': GUI.regularfont, 'align': TextNode.ALeft   },
    { 'name': "mpCost",      'label': "MP",      'x':   4, 'font': GUI.regularfont, 'align': TextNode.ALeft   },
    { 'name': "speed",       'label': "Speed",   'x':  35, 'font': GUI.regularfont, 'align': TextNode.ALeft   },
    { 'name': "jpCost",      'label': "JP",      'x':  78, 'font': GUI.regularfont, 'align': TextNode.ACenter },
]

rows = [
    { 'cells': ['Aim',      '00', '50', 'Learned', ], 'enabled': True , 'callback': exemplecallback, },
    { 'cells': ['Blackout', '00', '25', 'Learned', ], 'enabled': True , 'callback': exemplecallback, },
    { 'cells': ['Wait',     '00', '25', 'Learned', ], 'enabled': True , 'callback': exemplecallback, },
    { 'cells': ['Status',   '00', '25', 'Learned', ], 'enabled': False, 'callback': exemplecallback, },
    { 'cells': ['Blackout', '00', '00', 'Learned', ], 'enabled': True , 'callback': exemplecallback, },
    { 'cells': ['Test1',    '00', '34', 'Learned', ], 'enabled': True , 'callback': exemplecallback, },
    { 'cells': ['Test2',    '00', '17', 'Learned', ], 'enabled': False, 'callback': exemplecallback, },
    { 'cells': ['Test3',    '00', '15', 'Learned', ], 'enabled': False, 'callback': exemplecallback, },
    { 'cells': ['Test4',    '00', '25', 'Learned', ], 'enabled': False, 'callback': exemplecallback, },
    { 'cells': ['Test5',    '00', '00', 'Learned', ], 'enabled': True , 'callback': exemplecallback, },
    { 'cells': ['Test6',    '00', '30', 'Learned', ], 'enabled': True , 'callback': exemplecallback, },
    { 'cells': ['Aim',      '00', '50', 'Learned', ], 'enabled': True , 'callback': exemplecallback, },
    { 'cells': ['Blackout', '00', '25', 'Learned', ], 'enabled': True , 'callback': exemplecallback, },
    { 'cells': ['Wait',     '00', '25', 'Learned', ], 'enabled': True , 'callback': exemplecallback, },
    { 'cells': ['Status',   '00', '25', 'Learned', ], 'enabled': False, 'callback': exemplecallback, },
]

GUI.ScrollableList('list', 3.0, 31.0, 206.0, 148.0, 23, columns, rows, 8, cancelcallback)

# GUI.Blueprint('menu1')

# columns = [
#     { 'name': "menu", 'label': "Menu", 'x': -25, 'font': GUI.regularfont, 'align': TextNode.ALeft   },
# ]

# rows = [
#     { 'cells': ['Status',      ], 'enabled': True , 'callback': exemplecallback, },
#     { 'cells': ['Auto-Battle', ], 'enabled': True , 'callback': exemplecallback, },
# ]

# GUI.ScrollableList('shadowed', 73, -32, 62.0, 43.0, 16, columns, rows, 2, cancelcallback, 'Menu')

# GUI.Blueprint('menu2')

# columns = [
#     { 'name': "menu", 'label': "Menu", 'x': -44, 'font': GUI.regularfont, 'align': TextNode.ALeft   },
# ]

# rows = [
#     { 'cells': ['Sleep Blade',   ], 'enabled': True , 'callback': exemplecallback, },
#     { 'cells': ['Coral Sword',   ], 'enabled': True , 'callback': exemplecallback, },
#     { 'cells': ['Mythril Sword', ], 'enabled': True , 'callback': exemplecallback, },
#     { 'cells': ['Iron Sword',    ], 'enabled': True , 'callback': exemplecallback, },
#     { 'cells': ['Auto-Battle',   ], 'enabled': True , 'callback': exemplecallback, },
#     { 'cells': ['Sleep Blade',   ], 'enabled': True , 'callback': exemplecallback, },
#     { 'cells': ['Coral Sword',   ], 'enabled': True , 'callback': exemplecallback, },
#     { 'cells': ['Mythril Sword', ], 'enabled': True , 'callback': exemplecallback, },
#     { 'cells': ['Iron Sword',    ], 'enabled': True , 'callback': exemplecallback, },
#     { 'cells': ['Auto-Battle',   ], 'enabled': True , 'callback': exemplecallback, },
#     { 'cells': ['Sleep Blade',   ], 'enabled': True , 'callback': exemplecallback, },
#     { 'cells': ['Coral Sword',   ], 'enabled': True , 'callback': exemplecallback, },
#     { 'cells': ['Mythril Sword', ], 'enabled': True , 'callback': exemplecallback, },
#     { 'cells': ['Iron Sword',    ], 'enabled': True , 'callback': exemplecallback, },
#     { 'cells': ['Auto-Battle',   ], 'enabled': True , 'callback': exemplecallback, },
# ]

# GUI.ScrollableList('list', -31, 35, 170.0, 148.0, 23, columns, rows, 8, cancelcallback)

run()
