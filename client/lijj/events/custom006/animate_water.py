from panda3d.core import *
from direct.interval.IntervalGlobal import *
import sys, getopt, inspect, os, subprocess

# Prepare variables.
tethicalTestApplication = ''
game = ''
gameName = ''
basePath = ''
testName = 'map-event-test'
thisWholeFilename = os.path.abspath(__file__)
thisFilename = os.path.basename(os.path.abspath(__file__))
targetMapNameWithoutExtension = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
targetMapName = os.path.basename(os.path.dirname(os.path.abspath(__file__))) + ".json"
targetMapFullPath = ''
# Prepare path components of event Python file.
path = os.path.abspath(__file__)
folders=[]
while 1:
	path,folder=os.path.split(path)
	if folder!="":
		folders.append(folder)
	else:
		if path!="":
			folders.append(path)
		break
folders.reverse()
# Get Tethical application and maps path.
if 'client' in folders:
	i = folders.index('client')
	if len(folders) > i+1:
		basePath = os.path.join(*folders[:i])
		tethicalTestApplication = os.path.join(*folders[:i+1] + ['Tests.py'])
		game = os.path.join(*folders[:i+2])
		gameName = folders[i+1]
		targetMapFullPath = os.path.join(*folders[:i+2] + ['models', 'maps', targetMapName])
		pass
	pass

# Prepare error class.
class UsageError(Exception):
	def __init__(self, msg):
		self.msg = msg
#
def main(argv=None):
	"""
This is a Tethical client-side map event script. When called from the command-line, the event will load itself into Tethical's map test application. Otherwise, calling the map event from a map description file will result in the event's programming running right before the map is displayed for the user (i.e. at the very beginning of a battle).
	"""
	# Make sure not to throw an exception when dealing with arguments.
	try:
		argv
	except NameError:
		argv = None
	# Pick the appropriate arguments, if not set already.
	if argv is None:
		argv = sys.argv
	try:
		try:
			opts, args = getopt.getopt(argv[1:], "h", ["help"])
		except getopt.error, msg:
			raise UsageError(msg)
		# Create a list with only the options.
		onlyOptions = [a[0] for a in opts]
		# Find supplied options.
		if ('-h' in onlyOptions) or ('--help' in onlyOptions):
			raise UsageError ("Usage: python " + os.path.basename(os.path.abspath(__file__)) + "\n\n" + main.__doc__)
		elif len(argv[1:]) != 0:
			raise UsageError ("Usage: python " + os.path.basename(os.path.abspath(__file__)) + "\n" + "For help, use --help")
		pass
		# Finally, run the test application.
		if tethicalTestApplication is not '' and thisFilename is not '' and targetMapFullPath is not '':
			print "Running: python " + tethicalTestApplication + " " + testName + " " + basePath + " " + gameName + " " + targetMapName + " " + thisWholeFilename
			subprocess.call(["python", tethicalTestApplication, testName, basePath, gameName, targetMapName, thisWholeFilename])
		else:
			raise UsageError ("Cannot execute test. This client-side map event is not in a location conducive to being run.")
	except UsageError, err:
		print >>sys.stderr, err.msg
		return 2
# Run the test event, or run the event code, depending on context.
if __name__ == "__main__":
	sys.exit(main())
else:
	failedToLoadAtLeastOneTexture = False
	# Generate a PNMImage.
	def setupTexture(path):
		global failedToLoadAtLeastOneTexture
		# Set up blank image as a texture.
		texturePNMImage = PNMImage ()
		# Have Panda3d get the appropriate filename.
		file = Filename.fromOsSpecific(path)
		# Make sure the file actually exists first.
		try:
			texture = loader.loadTexture(file) # Use Panda3d's loader to load a pandac.PandaModules.Texture into a variable.
			texture.store(texturePNMImage) # Signal Panda3d to store the contents of what it just loaded into our blank image.
		except:
			failedToLoadAtLeastOneTexture = True
		# Return just the image (not the pandac.PandaModules.Texture).
		return texturePNMImage
	# Prepare to store a record of PNMImage objects.
	textures = []
	# Join each image frame's PNMImage to the record, resulting in: [PNMImage-1, ..., PNMImage-n]
	textures = textures + [setupTexture(os.path.join( gameName, 'textures', 'map', targetMapNameWithoutExtension+'-2.png'))]
	textures = textures + [setupTexture(os.path.join( gameName, 'textures', 'map', targetMapNameWithoutExtension+'-3.png'))]
	textures = textures + [setupTexture(os.path.join( gameName, 'textures', 'map', targetMapNameWithoutExtension+'-4.png'))]
	textures = textures + [setupTexture(os.path.join( gameName, 'textures', 'map', targetMapNameWithoutExtension+'-5.png'))]
	textures = textures + [setupTexture(os.path.join( gameName, 'textures', 'map', targetMapNameWithoutExtension+'-6.png'))]
	textures = textures + [setupTexture(os.path.join( gameName, 'textures', 'map', targetMapNameWithoutExtension+'-7.png'))]
	textures = textures + [setupTexture(os.path.join( gameName, 'textures', 'map', targetMapNameWithoutExtension+'-8.png'))]
	textures = textures + [setupTexture(os.path.join( gameName, 'textures', 'map', targetMapNameWithoutExtension+'-9.png'))]
	textures = textures + [setupTexture(os.path.join( gameName, 'textures', 'map', targetMapNameWithoutExtension+'-1.png'))]
	# Prepare to get the NodePath of the loaded map object (attached to the render object).
	targetMapName = os.path.basename(os.path.dirname(os.path.abspath(__file__))) + ".egg"
	# Get the NodePath.
	mapObject = render.find("**/"+targetMapName+"/Cube")
	# If the NodePath was found, add the sequence of texture switches to the scene in order to animate water.
	if not mapObject.isEmpty() and not failedToLoadAtLeastOneTexture:
		# Prepare the Sequence object.
		seq = Sequence()
		# Go through the range of textures in the record.
		for i in range(len(textures)):
			# Prepare the delay between texture switches.
			delay = 0.14
			# Prepare a function to switch the texture of the passed in NodePath.
			def f(x, c):
				tex = x.findTexture('*')
				tex.load(textures[c])
				pass
			# Push the function to the animation sequence.
			seq.append(Func(f, mapObject, i))
			# Push the wait time to the animation sequence.
			seq.append(Wait(delay))
		# Loop indefinitely.
		seq.loop()
		pass
	else:
		print "Event failed to find map: " + targetMapName