from Config import *
import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.DirectGui import *
from pandac.PandaModules import *
import GUI

#GUI.Test('test_menu')

def exemplecallback(text):
    print "You clicked the row #"+str(text)

def cancelcallback():
    print "Bye"

columns = [
    { 'x': -90, 'font': GUI.regularfont, 'align': TextNode.ALeft   },
    { 'x':  19, 'font': GUI.regularfont, 'align': TextNode.ARight  },
    { 'x':  49, 'font': GUI.regularfont, 'align': TextNode.ARight  },
    { 'x':  81, 'font': GUI.regularfont, 'align': TextNode.ACenter },
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
]

GUI.SkillList(columns, rows, 8, cancelcallback)

run()
