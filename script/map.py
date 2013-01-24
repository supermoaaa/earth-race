from bge import logic as gl
import objects

def loadMap( ):
	if not hasattr(gl , 'mapName'):
		gl.mapName = "routeDeTest"
	gl.checkpoints=[]
	path = gl.expandPath("//")+"objects/maps/"+gl.mapName+"/"
	objects.libLoad( path+gl.mapName+".blend", "Scene" )
	propertieFile = open(path+gl.mapName+".cfg")
	for line in propertieFile:
		if "start = " in line:
			placeStart(line[8:-1])
			addCheckpoint(line[8:-1])
		elif "checkpoint = " in line:
			addCheckpoint(line[13:-1])
		elif "end = " in line:
			print("end"+str(line[6:-1]))
			addCheckpoint(line[6:-1])

def placeStart(objectName):
	# set car loader
	gl.getCurrentScene().objects.get('Loader').position = gl.getCurrentScene().objects.get(objectName).position
	gl.getCurrentScene().objects.get('Loader').orientation = gl.getCurrentScene().objects.get(objectName).orientation
	gl.getCurrentScene().objects.get('Loader').scaling = gl.getCurrentScene().objects.get(objectName).scaling

	# set camera
	gl.getCurrentScene().objects.get('Camera').position = gl.getCurrentScene().objects.get(objectName).position
	gl.getCurrentScene().objects.get('Camera').localPosition[1] -= 20
	gl.getCurrentScene().objects.get('Camera').position[2] += 6

	# start car loader
	gl.getCurrentScene().objects.get('Loader')['start'] = True

def addCheckpoint(objectName):
	gl.checkpoints.append(gl.getCurrentScene().objects.get(objectName))

def isCheckpoint(objectLink):
	if objectLink in gl.checkpoints:
		return True
	else:
		return False
