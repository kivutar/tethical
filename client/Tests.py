from direct.showbase.DirectObject import DirectObject
import direct.directbase.DirectStart
import json, sys, getopt, inspect, os, imp
# Tethical's Drawing-Related Features
from BattleGraphics import *
from Matrix import *
from Cursor import *
import SequenceBuilder
# Tethical's Key Handling Feature
import CameraHandler

class UsageError(Exception):
	def __init__(self, msg):
		self.msg = msg

#
try:
    argv
except NameError:
    argv = None
#
if argv is None:
	argv = sys.argv
try:
	try:
		opts, args = getopt.getopt(argv[1:], "h", ["help"])
	except getopt.error, msg:
		raise UsageError(msg)
except UsageError, err:
	print >>sys.stderr, err.msg
# Running: 
#
#	python C:\Tethical\master\client\Tests.py 
#		map-event-test 
#		C:\Tethical\master 
#		lijj 
#		custom006.json 
#		C:\Tethical\master\client\lijj\events\custom006\animate_water.py
if len(argv[1:]) > 0:
	# Required argument matching.
	command = argv[1]	
	BASEPATH = argv[2] # 'C:\Tethical\master'
	GAME = argv[3] # 'lijj', 'fft'
	# Global game directories available.
	SERVERGAME = os.path.join(BASEPATH, 'server', GAME)	
	# Map Event Test (map-event-test) launches a map and manually runs a script.
	if command == 'map-event-test':
		# Event argument usage.
		MAP = argv[4] # 'custom006.json'
		EVENT = argv[5] # 'C:\Tethical\master\client\lijj\events\custom006\animate_water.py'
		# Get directory of map description files (JSON).
		MAPS = os.path.join(SERVERGAME, 'maps', MAP)
		# Get map description file (JSON); ..\server\Map.py:9
		f = open(MAPS, 'r')
		mapJSON = json.loads(f.read())
		f.close()
		# Parse map description file in place of the JSON response the server sends; ..\server\Map.py:13
		tiles = [ [ [ None for z in range(mapJSON['z']) ] for y in range(mapJSON['y']) ] for x in range(mapJSON['x']) ]
		for t in mapJSON['tiles']:
			tiles[int(t['x'])][int(t['y'])][int(t['z'])] = t
		# Add extra information back to the map description file in memory; ..\server\Map.py:17
		mapJSON['tiles'] = tiles
		battleGraphics = None
		try:
			# Instanciate the battle graphics
			battleGraphics = BattleGraphics(mapJSON, GAME)			
			# Display the terrain (map model is actually loaded here).
			battleGraphics.displayTerrain()			
		except IOError:
			# Map couldn't be found.
			battleGraphics = None
			pass
		# If the map was loaded successfully, finish setting everything up and run the event.
		if not battleGraphics is None:
			# Light the scene
			battleGraphics.lightScene()
			# Bind camera controls to keys.
			camhandler = CameraHandler.CameraHandler()
			camhandler.accept('escape', lambda: sys.exit());
			# Play the background music
			music = base.loader.loadSfx(GAME+'/music/'+mapJSON['music']+'.ogg')
			music.setLoop(True)
			music.play()
			# Place highlightable tiles on the map
			matrix = Matrix(battleGraphics, mapJSON)
			# Cursor stuff
			cursor = Cursor(battleGraphics, matrix.container)
			# Add the special effects
			battleGraphics.addEffects()
			try:
				# Load event.
				imp.load_source('event', EVENT)
				#
				print ""
				print ""
				print "Controls: "
				print ""
				print "  G:	Rotate Map Left"
				print "  F:	Rotate Map Right"
				print "  H:	Ascend/Descend"
				print "  D:	Zoom In/Zoom Out"
				print "  ESC:	End Test"
			except:
				print 'Event could not be found at '+str(EVENT)
		pass
	pass
#
run()