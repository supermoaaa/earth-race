from bge import logic as gl
import os
from logs import log
import objects
import json

def lineParse(line):
	param = line.split("=")
	param[0] = param[0].split(" ")[0]
	param = [param[0]]+param[1].split(" ")
	try:
		param[-1] = param[-1].replace('\n','')
	except:
		pass
	param.remove("")
	return param

def loadVehicle(vehicleType, endFunction):
	path = gl.expandPath("//")+"objects"+os.sep+"vehicles"+os.sep+vehicleType+os.sep
	if vehicleType not in gl.conf[1] or path+vehicleType+".blend" not in objects.libList():

		# load vehicle scene
		gl.conf[1][vehicleType] = []
		gl.conf[1][vehicleType].append(['loaded',False])
		#~ objects.libLoad(path+vehicleType+".blend", "Scene", load_actions=True, load_scripts=True, async=False ).onFinish = fonc
		gl.LibLoad(path+vehicleType+".blend", "Scene", load_actions=True, load_scripts=True, async=True ).onFinish = endFunction

		# load vehicle properties
		propertieFile = open(path+vehicleType+".cfg", "r")
		for line in propertieFile:
			gl.conf[1][vehicleType].append( lineParse(line) )
		gl.conf[1][vehicleType].append(['users',1])
		propertieFile.close
		log("info","loadVehicle "+vehicleType)
	else:
		for param in gl.conf[1][vehicleType]:
			if param[0]=="users":
				param[1]+=1

def setFinishLoadedVehicle(vehicleType):
	gl.conf[1][vehicleType][0][1] = True

def isLoadedVehicle(vehicleType):
	if vehicleType in gl.conf[1] and gl.conf[1][vehicleType][0][0]=='loaded':
		return gl.conf[1][vehicleType][0][1]
	else:
		return False

def freeVehicle(vehicleType):
	if hasattr(gl,"conf"):
		path = gl.expandPath("//")+"objects"+os.sep+"vehicles"+os.sep+vehicleType+os.sep
		for param in gl.conf[1][vehicleType]:
			if param[0]=="users":
				param[1]-=1
				if param[1]==0:
					objects.libFree(path+vehicleType+".blend")
					del(gl.conf[1][vehicleType])
					log("info","freeVehicle "+vehicleType)

def loadWheel(wheelsType,endFunction):
	path = gl.expandPath("//")+"objects"+os.sep+"wheels"+os.sep+wheelsType+os.sep
	if wheelsType not in gl.conf[2] or path+wheelsType+".blend" not in objects.libList():

		# load wheel scene
		gl.conf[2][wheelsType] = []
		gl.conf[2][wheelsType].append(['loaded',False])
		#~ objects.libLoad(path+wheelsType+".blend","Scene", load_actions=True, load_scripts=True, async=True).onFinish = endFunction
		gl.LibLoad(path+wheelsType+".blend", "Scene", load_actions=True, load_scripts=True, async=True).onFinish = endFunction

		# load wheel properties
		propertieFile = open(path+wheelsType+".cfg", "r")
		for line in propertieFile:
			if line!="\n":
				gl.conf[2][wheelsType].append( lineParse(line) )
		gl.conf[2][wheelsType].append(['users',1])
		propertieFile.close
		log("info","loadWheel "+wheelsType)
	else:
		for param in gl.conf[2][wheelsType]:
			if param[0]=="users":
				param[1]+=1

def setFinishLoadedWheel(wheelsType):
	gl.conf[2][wheelsType][0][1] = True

def isLoadedWheel(wheelsType):
	if wheelsType in gl.conf[2] and gl.conf[2][wheelsType][0][0]=='loaded':
		return gl.conf[2][wheelsType][0][1]
	else:
		return False

def freeWheels(wheelsType):
	if hasattr(gl,"conf"):
		path = gl.expandPath("//")+"objects"+os.sep+"wheels"+os.sep+wheelsType+os.sep
		for param in gl.conf[2][wheelsType]:
			if param[0]=="users":
				param[1]-=1
				if param[1]==0:
					objects.libFree(path+wheelsType+".blend")
					del(gl.conf[2][wheelsType])
					log("info","freeWheel "+wheelsType)

def loadPlayer():
	if not hasattr(gl, 'conf'):
		gl.conf = [ [], {}, {} ]
	else:
		gl.conf[0] = []
	with open(gl.expandPath("//")+'players.json', 'r') as f:
		try:
			gl.conf[0] = json.load(f)
		except:
			log("error", "json players mal formaté")
	checkPlayerConf()

def checkPlayerConf():
	defaultConf = [
			[
				'player1',
				'human',
				[
					[ 'accelerate', '122', False ],
					[ 'reverse', '115', False ],
					[ 'left', '113', False ],
					[ 'right', '100', False ],
					[ 'brake', '32', False ],
					[ 'boost', '129', False ],
					[ 'upGear', '101', True ],
					[ 'downGear', '97', True ],
					[ 'respawn', '114', True ],
					[ 'changeCam', '99', True ]
				],
				'caisse',
				'rouepleine1'
			],
			[
				'player2',
				'human',
				[
					[ 'accelerate', '146', False ],
					[ 'reverse', '144', False ],
					[ 'left', '143', False ],
					[ 'right', '145', False ],
					[ 'brake', '32', False ],
					[ 'boost', '129', False ],
					[ 'upGear', '101', True ],
					[ 'downGear', '97', True ],
					[ 'respawn', '114', True ],
					[ 'changeCam', '99', True ]
				],
				'caisse',
				'rouepleine1'
			],
			[
				'player3',
				'human',
				[
					[ 'accelerate', '122', False ],
					[ 'reverse', '115', False ],
					[ 'left', '113', False ],
					[ 'right', '100', False ],
					[ 'brake', '32', False ],
					[ 'boost', '129', False ],
					[ 'upGear', '101', True ],
					[ 'downGear', '97', True ],
					[ 'respawn', '114', True ],
					[ 'changeCam', '99', True ]
				],
				'caisse',
				'rouepleine1'
			],
			[
				'player4',
				'human',
				[
					[ 'accelerate', '122', False ],
					[ 'reverse', '115', False ],
					[ 'left', '113', False ],
					[ 'right', '100', False ],
					[ 'brake', '32', False ],
					[ 'boost', '129', False ],
					[ 'upGear', '101', True ],
					[ 'downGear', '97', True ],
					[ 'respawn', '114', True ],
					[ 'changeCam', '99', True ]
				],
				'caisse',
				'rouepleine1'
			]
		]
	if not hasattr(gl, 'conf'):
		gl.conf = [ [], {}, {} ]
	nbPlayers=len(gl.conf[0])
	if nbPlayers==0:
		gl.conf[0] = defaultConf
	elif nbPlayers==1:
		gl.conf[0].extend(defaultConf[1:])
	elif nbPlayers==2:
		gl.conf[0].extend(defaultConf[2:])
	elif nbPlayers==3:
		gl.conf[0].extend(defaultConf[3:])
	else:
		checkPlayer( 0, defaultConf )
		checkPlayer( 1, defaultConf )
		checkPlayer( 2, defaultConf )
		checkPlayer( 3, defaultConf )

def checkPlayer( idPlayer, defaultConf ):
	if len(gl.conf[0][idPlayer])>3:
		checkKeys( idPlayer, defaultConf )
	nbElements = len(gl.conf[0][idPlayer])
	gl.conf[0][idPlayer].extend(defaultConf[idPlayer][nbElements:])

def checkKeys( idPlayer, defaultConf):
	nbElements = len(gl.conf[0][idPlayer][2])
	gl.conf[0][idPlayer][2].extend(defaultConf[idPlayer][2][nbElements:])

def savePlayer():
	with open(gl.expandPath("//")+'players.json', 'w') as f:
		json.dump(gl.conf[0], f, sort_keys=True, indent=4)

def loadConf():
	with open(gl.expandPath("//")+'conf.json', 'r') as f:
		try:
			conf = json.load(f)
			gl.graphic = conf[0]
			gl.sound = conf[1]
			gl.skin = conf[2]
		except:
			log("error", "json de configuration générale mal formaté")
	checkConf()

def checkConf():
	if not hasattr(gl, 'graphic'):
		gl.graphic = [ True, rd.getAnisotropicFiltering(), 3 ]
	if not hasattr(gl, 'sound'):
		gl.sound = [ 50 ]
	if not hasattr(gl, 'skin'):
		gl.skin = 'themes/default'

def saveConf():
	with open(gl.expandPath("//")+'players.json', 'w') as f:
		json.dump([gl.graphic,gl.sound,gl.skin], f, sort_keys=True, indent=4)

def loadCounter():
	with open(gl.expandPath("//")+'counter.json', 'r') as f:
		try:
			gl.counterPos = json.load(f)
		except:
			log("error", "json de configuration du counter mal formaté")
	if not hasattr(gl, 'counterPos'):
		gl.counterPos = [ [ 0.81002893, 0.158075601, 40 ], [ 0.5, 0.932432, 40 ], [ "under",  0.0,  0.08 ] ]

def loadScore(mapName):
	with open(gl.expandPath("//")+'objects'+os.sep+'maps'+os.sep+str(mapName)+os.sep+'scores.json', 'r') as f:
		try:
			gl.score = json.load(f)
		except:
			log('error', 'json des scores mal formaté')
	if not hasattr(gl, 'score'):
		gl.scores = Scores(mapName)

def saveScore():
	if hasattr(gl,'scores'):
		with open(gl.expandPath("//")+'objects'+os.sep+'maps'+os.sep+str(mapName)+os.sep+'scores.json', 'w') as f:
			json.dump(gl.scores, f, sort_keys=True, indent=4)
