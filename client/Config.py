import sys
from panda3d.core import loadPrcFile
from pandac.PandaModules import ConfigVariableString
loadPrcFile("../config.prc")
GAME = ConfigVariableString('game', 'fft').getValue()
loadPrcFile(GAME+"/config.prc")

IP = ConfigVariableString('ip', '127.0.0.1').getValue()
PORT =  int(ConfigVariableString('port', '3001').getValue())

CROSS_BTN    = ConfigVariableString('cross-btn',    '0').getValue()
CIRCLE_BTN   = ConfigVariableString('circle-btn',   '3').getValue()
TRIANGLE_BTN = ConfigVariableString('triangle-btn', '2').getValue()
SQUARE_BTN   = ConfigVariableString('square-btn',   '1').getValue()
L1_BTN       = ConfigVariableString('l1-btn',       '4').getValue()
L2_BTN       = ConfigVariableString('l2-btn',       '7').getValue()
R1_BTN       = ConfigVariableString('r1-btn',       '6').getValue()
R2_BTN       = ConfigVariableString('r2-btn',       '9').getValue()
START_BTN    = ConfigVariableString('start-btn',    '8').getValue()
SELECT_BTN   = ConfigVariableString('select-btn',   '5').getValue()

SPRITE_SCALE = float( ConfigVariableString('sprite-scale', '2').getValue() )
