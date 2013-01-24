from bge import logic as gl
import os
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

def loadVehicle(vehicleType):
	path = gl.expandPath("//")+"objects"+os.sep+"vehicles"+os.sep+vehicleType+os.sep
	if vehicleType not in gl.conf[1] or path+vehicleType+".blend" not in objects.libList():

		# load vehicle scene
		objects.libLoad(path+vehicleType+".blend", "Scene")

		# load vehicle properties
		propertieFile = open(path+vehicleType+".cfg", "r")
		gl.conf[1][vehicleType] = []
		for line in propertieFile:
			gl.conf[1][vehicleType].append( lineParse(line) )
		gl.conf[1][vehicleType].append(['users',1])
		propertieFile.close
		print("loadVehicle "+vehicleType)
	else:
		for param in gl.conf[1][vehicleType]:
			if param[0]=="users":
				param[1]+=1

def freeVehicle(vehicleType):
	if hasattr(gl,"conf"):
		path = gl.expandPath("//")+"objects"+os.sep+"vehicles"+os.sep+vehicleType+os.sep
		for param in gl.conf[1][vehicleType]:
			if param[0]=="users":
				param[1]-=1
				if param[1]==0:
					objects.libFree(path+vehicleType+".blend")
					del(gl.conf[1][vehicleType])
					print("freeVehicle "+vehicleType)

def loadWheel(wheelsType):
	path = gl.expandPath("//")+"objects"+os.sep+"wheels"+os.sep+wheelsType+os.sep
	if wheelsType not in gl.conf[2] or path+wheelsType+".blend" not in objects.libList():

		# load wheel scene
		objects.libLoad(path+wheelsType+".blend","Scene")

		# load wheel properties
		propertieFile = open(path+wheelsType+".cfg", "r")
		gl.conf[2][wheelsType] = []
		for line in propertieFile:
			if line!="\n":
				gl.conf[2][wheelsType].append( lineParse(line) )
		gl.conf[2][wheelsType].append(['users',1])
		propertieFile.close
		print("loadWheel "+wheelsType)
	else:
		for param in gl.conf[2][wheelsType]:
			if param[0]=="users":
				param[1]+=1

def freeWheels(wheelsType):
	if hasattr(gl,"conf"):
		path = gl.expandPath("//")+"objects"+os.sep+"wheels"+os.sep+wheelsType+os.sep
		for param in gl.conf[2][wheelsType]:
			if param[0]=="users":
				param[1]-=1
				if param[1]==0:
					objects.libFree(path+wheelsType+".blend")
					del(gl.conf[2][wheelsType])
					print("freeWheel "+wheelsType)

def loadPlayer():
	if not hasattr(gl, 'conf'):
		gl.conf = [ [], {}, {} ]
	else:
		gl.conf[0] = []
	with open(gl.expandPath("//")+'players.json', 'r') as f:
		gl.conf[0] = json.load(f)
	checkConf()

def checkConf():
	defaultConf = [
			[
				'player1',
				'human',
				[
					[ 'accelerate', '122' ],
					[ 'reverse', '115' ],
					[ 'left', '113' ],
					[ 'right', '100' ],
					[ 'brake', '32' ],
					[ 'boost', '129' ],
					[ 'upGear', '101' ],
					[ 'downGear', '97' ]
				],
				'caisse',
				'rouepleine1'
			],
			[
				'player2',
				'human',
				[
					[ 'accelerate', '122' ],
					[ 'reverse', '115' ],
					[ 'left', '113' ],
					[ 'right', '100' ],
					[ 'brake', '32' ],
					[ 'boost', '129' ],
					[ 'upGear', '101' ],
					[ 'downGear', '97' ]
				],
				'caisse',
				'rouepleine1'
			],
			[
				'player3',
				'human',
				[
					[ 'accelerate', '122' ],
					[ 'reverse', '115' ],
					[ 'left', '113' ],
					[ 'right', '100' ],
					[ 'brake', '32' ],
					[ 'boost', '129' ],
					[ 'upGear', '101' ],
					[ 'downGear', '97' ]
				],
				'caisse',
				'rouepleine1'
			],
			[
				'player4',
				'human',
				[
					[ 'accelerate', '122' ],
					[ 'reverse', '115' ],
					[ 'left', '113' ],
					[ 'right', '100' ],
					[ 'brake', '32' ],
					[ 'boost', '129' ],
					[ 'upGear', '101' ],
					[ 'downGear', '97' ]
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
	nbElements = len(gl.conf[0][idPlayer])
	gl.conf[0][idPlayer].extend(defaultConf[idPlayer][nbElements:])

def savePlayer():
	with open(gl.expandPath("//")+'players.json', 'w') as f:
		json.dump(gl.conf[0], f, sort_keys=True, indent=4)
