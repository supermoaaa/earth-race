from bge import logic as gl
from bge import render as rd
import os
from logs import log
import objects
import json
from scores import Scores


def lineParse(line):
	try:
		param = line.split("=")
		param[0] = param[0].strip()
		param = [param[0]] + param[1].split(" ")
		# delete return character
		try:
			param[-1] = param[-1].replace('\n', '')
		except:
			pass
		param.remove("")
		# try to parse a simple array
		try:
			param[1] = (''.join(param[1:])).split('[')[1].split(']')[0].split(',')
			param[1] = list(map(typeParse, param[1]))
		except:
			pass
		return param
	except IndexError e:
		log("error", "failed to parse line '" + str(line)+"'")

def typeParse(var):
	try:
		var = float(var)
	except:
		pass
	return var


def loadVehicle(vehicleType, endFunction):
	path = gl.expandPath("//") + "objects" + os.sep + \
		"vehicles" + os.sep + vehicleType + os.sep
	if (vehicleType not in gl.conf[1] or
			path + vehicleType + ".blend" not in objects.libList()):

		# load vehicle scene
		gl.conf[1][vehicleType] = []
		gl.conf[1][vehicleType].append(['loaded', False])
		#~ objects.libLoad(path+vehicleType+".blend", "Scene",
				#~ load_actions=True, load_scripts=True, async=False ).onFinish = fonc
		gl.LibLoad(path + vehicleType + ".blend", "Scene", load_actions=True,
				load_scripts=True, async=True).onFinish = endFunction

		# load vehicle properties
		propertieFile = open(path + vehicleType + ".cfg", "r")
		for line in propertieFile:
			param = lineParse(line)
			if param[0].endswith("Sound"):
				param[1] = path + param[1]
			gl.conf[1][vehicleType].append(param)

		gl.conf[1][vehicleType].append(['users', 1])
		propertieFile.close
		log("info", "loadVehicle " + vehicleType)
		log("debug", "vehicle conf : " + str(gl.conf[1][vehicleType]))
	else:
		for param in gl.conf[1][vehicleType]:
			if param[0] == "users":
				param[1] += 1


def setFinishLoadedVehicle(vehicleType):
	gl.conf[1][vehicleType][0][1] = True


def isLoadedVehicle(vehicleType):
	if vehicleType in gl.conf[1] and gl.conf[1][vehicleType][0][0] == 'loaded':
		return gl.conf[1][vehicleType][0][1]
	else:
		return False


def freeVehicle(vehicleType):
	if hasattr(gl, "conf"):
		path = gl.expandPath("//") + "objects" + os.sep + \
			"vehicles" + os.sep + vehicleType + os.sep
		for param in gl.conf[1][vehicleType]:
			if param[0] == "users":
				param[1] -= 1
				if param[1] == 0:
					objects.libFree(path + vehicleType + ".blend")
					del(gl.conf[1][vehicleType])
					log("info", "freeVehicle " + vehicleType)


def loadWheel(wheelsType, endFunction):
	path = gl.expandPath("//") + "objects" + os.sep + \
		"wheels" + os.sep + wheelsType + os.sep
	if (wheelsType not in gl.conf[2] or
			path + wheelsType + ".blend" not in objects.libList()):

		# load wheel scene
		gl.conf[2][wheelsType] = []
		gl.conf[2][wheelsType].append(['loaded', False])
		#~ objects.libLoad(path+wheelsType+".blend","Scene",
				#~ load_actions=True, load_scripts=True, async=True).onFinish = endFunction
		gl.LibLoad(path + wheelsType + ".blend", "Scene", load_actions=True,
				load_scripts=True, async=True).onFinish = endFunction

		# load wheel properties
		propertieFile = open(path + wheelsType + ".cfg", "r")
		for line in propertieFile:
			param = lineParse(line)
			if param[0].endswith("Sound"):
				param[1] = path + param[1]
			gl.conf[2][wheelsType].append(param)
		gl.conf[2][wheelsType].append(['users', 1])
		propertieFile.close
		log("info", "loadWheel " + wheelsType)
	else:
		for param in gl.conf[2][wheelsType]:
			if param[0] == "users":
				param[1] += 1


def setFinishLoadedWheel(wheelsType):
	gl.conf[2][wheelsType][0][1] = True


def isLoadedWheel(wheelsType):
	if wheelsType in gl.conf[2] and gl.conf[2][wheelsType][0][0] == 'loaded':
		return gl.conf[2][wheelsType][0][1]
	else:
		return False


def freeWheels(wheelsType):
	if hasattr(gl, "conf"):
		path = gl.expandPath("//") + "objects" + os.sep + \
			"wheels" + os.sep + wheelsType + os.sep
		for param in gl.conf[2][wheelsType]:
			if param[0] == "users":
				param[1] -= 1
				if param[1] == 0:
					objects.libFree(path + wheelsType + ".blend")
					del(gl.conf[2][wheelsType])
					log("info", "freeWheel " + wheelsType)


def loadPlayer():
	if not hasattr(gl, 'conf'):
		gl.conf = [[], {}, {}]
	else:
		gl.conf[0] = []
	with open(gl.expandPath("//") + 'players.json', 'r') as f:
		try:
			gl.conf[0] = json.load(f)
		except ValueError:
			log("error", "json players mal formaté")
	checkPlayerConf()


def checkPlayerConf():
	defaultConf = [
		[
			'player1',
			'human',
			[
				['accelerate', '122', False],
				['reverse', '115', False],
				['left', '113', False],
				['right', '100', False],
				['brake', '32', False],
				['boost', '129', False],
				['upGear', '101', True],
				['downGear', '97', True],
				['respawn', '114', True],
				['changeCam', '99', True]
			],
			'caisse',
			'rouepleine1'
		],
		[
			'player2',
			'human',
			[
				['accelerate', '146', False],
				['reverse', '144', False],
				['left', '143', False],
				['right', '145', False],
				['brake', '32', False],
				['boost', '129', False],
				['upGear', '101', True],
				['downGear', '97', True],
				['respawn', '114', True],
				['changeCam', '99', True]
			],
			'caisse',
			'rouepleine1'
		],
		[
			'player3',
			'human',
			[
				['accelerate', '122', False],
				['reverse', '115', False],
				['left', '113', False],
				['right', '100', False],
				['brake', '32', False],
				['boost', '129', False],
				['upGear', '101', True],
				['downGear', '97', True],
				['respawn', '114', True],
				['changeCam', '99', True]
			],
			'caisse',
			'rouepleine1'
		],
		[
			'player4',
			'human',
			[
				['accelerate', '122', False],
				['reverse', '115', False],
				['left', '113', False],
				['right', '100', False],
				['brake', '32', False],
				['boost', '129', False],
				['upGear', '101', True],
				['downGear', '97', True],
				['respawn', '114', True],
				['changeCam', '99', True]
			],
			'caisse',
			'rouepleine1'
		]
	]
	if not hasattr(gl, 'conf'):
		gl.conf = [[], {}, {}]
	nbPlayers = len(gl.conf[0])
	if nbPlayers == 0:
		gl.conf[0] = defaultConf
	elif nbPlayers == 1:
		gl.conf[0].extend(defaultConf[1:])
	elif nbPlayers == 2:
		gl.conf[0].extend(defaultConf[2:])
	elif nbPlayers == 3:
		gl.conf[0].extend(defaultConf[3:])
	else:
		checkPlayer(0, defaultConf)
		checkPlayer(1, defaultConf)
		checkPlayer(2, defaultConf)
		checkPlayer(3, defaultConf)


def checkPlayer(idPlayer, defaultConf):
	if len(gl.conf[0][idPlayer]) > 3:
		checkKeys(idPlayer, defaultConf)
	nbElements = len(gl.conf[0][idPlayer])
	gl.conf[0][idPlayer].extend(defaultConf[idPlayer][nbElements:])


def checkKeys(idPlayer, defaultConf):
	nbElements = len(gl.conf[0][idPlayer][2])
	gl.conf[0][idPlayer][2].extend(defaultConf[idPlayer][2][nbElements:])


def savePlayer():
	with open(gl.expandPath("//") + 'players.json', 'w') as f:
		json.dump(gl.conf[0], f, sort_keys=True, indent=4)


def loadConf():
	with open(gl.expandPath("//") + 'conf.json', 'r') as f:
		try:
			conf = json.load(f)
			gl.graphic = conf[0]
			gl.sound = conf[1]
			gl.skin = conf[2]
			gl.generalConf = conf[3]
		except (ValueError, IndexError):
			log("error", "json de configuration générale mal formaté")
	checkConf()


def checkConf():
	if not hasattr(gl, 'graphic'):
		gl.graphic = [True, rd.getAnisotropicFiltering(), 3]
	if not hasattr(gl, 'sound'):
		gl.sound = [50, 50, "electro"]
	if not hasattr(gl, 'skin'):
		gl.skin = 'themes/default'
	if not hasattr(gl, 'generalConf'):
		# mirror, Anisotropic, mist start, mist end, language
		gl.generalConf = [True, rd.getAnisotropicFiltering(),
				25, 50, 'sun', 'Francais']


def saveConf():
	with open(gl.expandPath("//") + 'conf.json', 'w') as f:
		json.dump([gl.graphic, gl.sound, gl.skin, gl.generalConf],
				f, sort_keys=True, indent=4)


def loadCounter():
	with open(gl.expandPath("//") + 'textInGame.json', 'r') as f:
		try:
			gl.counterPos = json.load(f)
		except ValueError:
			log("error", "json de configuration du counter mal formaté")
	if not hasattr(gl, 'counterPos'):
		gl.counterPos = [[0.81002893, 0.158075601, 40],
						[0.5, 0.932432, 40], ["under", 0.0, 0.08]]


def loadScores(mapName):
	scoresFile = gl.expandPath("//") + 'objects' + os.sep + \
		'maps' + os.sep + str(mapName) + os.sep + 'scores.json'
	gl.scores = Scores(mapName)
	if os.path.isfile(scoresFile):
		with open(scoresFile, 'r') as f:
			try:
				gl.scores.scores = json.load(f)
			except ValueError:
				log('error', 'json des scores mal formaté')


def saveScores():
	if hasattr(gl, 'scores'):
		confPath = os.path.join(gl.expandPath("//"), 'objects', 'maps',
				str(gl.scores.mapName), 'scores.json')
		with open(confPath, 'w') as f:
			json.dump(gl.scores.scores, f, sort_keys=True, indent=4)
