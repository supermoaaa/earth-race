from bge import logic as gl
import os.path
from logs import log
import objects
import loaderVehicles

def loadMap( ):
	loadSky()
	gl.matFriction = {}
	if not hasattr(gl , 'mapName'):
		gl.mapName = "routeDeTest"
	gl.checkpoints=[]
	path = gl.expandPath("//")+"objects/maps/"+gl.mapName+"/"
	#~ gl.LibLoad( path+gl.mapName+".blend", "Scene", load_actions=True, load_scripts=True, async=True).onFinish = t
	gl.LibLoad( path+gl.mapName+".blend", "Scene", load_actions=True, load_scripts=True, async=False)
	onFinishMapLoaded()

def loadSky():
	path = gl.expandPath("//")+"objects/sky/"
	blend = path+"skydome"+gl.generalConf[4][0].upper()+gl.generalConf[4][1:]+".blend"
	if not os.path.isfile(blend):
		log("error", "couldn't find file "+str(blend))
		blend = path+"skydomeCloud.blend"
	gl.LibLoad( blend, "Scene", load_actions=True, load_scripts=True, async=False)

def t(status):
	print("Library (%s) loaded in %.2fms." % (status.libraryName, status.timeTaken))
	onFinishMapLoaded()

def onFinishMapLoaded():
	print("finishLoading : "+gl.mapName)
	path = gl.expandPath("//")+"objects/maps/"+gl.mapName+"/"
	propertieFile = open(path+gl.mapName+".cfg")
	for line in propertieFile:
		if "start = " in line:
			addCheckpoint(line[8:-1])
		elif "checkpoint = " in line:
			addCheckpoint(line[13:-1])
		elif "end = " in line:
			addCheckpoint(line[6:-1])
		elif "mat = " in line:
			gl.matFriction = eval(line[6:-1])
	loaderVehicles.placeStart(gl.checkpoints[0].position,gl.checkpoints[0].orientation,gl.checkpoints[0].scaling)

def addCheckpoint(objectName):
	gl.checkpoints.append(gl.getCurrentScene().objects.get(objectName))

def isCheckpoint(objectLink):
	if objectLink in gl.checkpoints:
		return True
	else:
		return False
