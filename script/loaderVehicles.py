from bge import logic as gl
from bge import render as render
from time import time
from datetime import timedelta
import confParser as conf
from vehicleLinker import vehicleLinker
from logs import log
import objects
import writeOnScreen
import sound


def addVehicleLoader(source, playerId, playerName,
					vehicleType, wheelsType, shadowObj=None):
	scene = gl.getCurrentScene()
	child = scene.addObject('Car', source, 0)
	child['id'] = playerId
	child['playerName'] = playerName
	child['vehicleType'] = vehicleType
	child['wheelsType'] = wheelsType
	child['gear'] = 1
	child['kph'] = 0.0
	child['mph'] = 0.0
	child['accelerate'] = 0.0
	child['reverse'] = 0.0
	child['brake'] = 0.0
	child['boost'] = 0.0
	child['left'] = 0.0
	child['right'] = 0.0
	child['respawn'] = 0.0
	child['upGear'] = False
	child['downGear'] = False
	child['changeCam'] = 0.0
	child['simulate'] = False
	child['arrived'] = False
	child['cam'] = child.childrenRecursive['Camera']
	child['car'] = vehicleLinker(posObj=child, vehicle_type=vehicleType,
								wheels_type=wheelsType, camera_object=child['cam'], shadowObj=shadowObj)
	gl.cars.append([child['id'], child])
	log("debug", child.get('id'))
	return child


def autoViewport(linker, playerName):
	if not hasattr(gl, "dispPlayers") or playerName in gl.dispPlayers:
		scene = gl.getCurrentScene()
		if not hasattr(gl, "dispPlayers") or gl.dispPlayers[0] == 0:
			#~ gl.getCurrentScene().active_camera = linker.camera.camera
			camCompteur = scene.objects.get('Camera 1')
			camCompteur.setViewport(
				0, 0, render.getWindowWidth(), render.getWindowHeight())
			gl.camsCompteur.append(camCompteur)
		else:
			mode = gl.dispPlayers[0]
			playerId = gl.dispPlayers.index(playerName)
			if (mode == 1 or mode == 4) and playerId == 1:
				__addCam(linker, 'Camera 1', 0, render.getWindowHeight() / 2,
						render.getWindowWidth(), render.getWindowHeight())  # en haut
			elif (mode == 1 or mode == 3) and playerId == 1:
				__addCam(linker, 'Camera 2',
							0, 0, render.getWindowWidth(), render.getWindowHeight() / 2)  # en bas
			elif (mode == 2 or mode == 5) and playerId == 0:
				__addCam(linker, 'Camera 1',
							0, 0, render.getWindowWidth() / 2, render.getWindowHeight())  # à gauche
			elif (mode == 2 or mode == 6) and playerId == 1:
				__addCam(linker, 'Camera 2', render.getWindowWidth() / 2, 0,
						render.getWindowWidth(), render.getWindowHeight())  # à droite
			elif (mode == 3 or mode == 6 or mode == 7) and playerId == 0:
				__addCam(linker, 'Camera 1', 0, render.getWindowHeight() / 2,
						render.getWindowWidth() / 2, render.getWindowHeight())  # en haut à gauche
			elif (mode == 3 or mode == 5 or mode == 7) and playerId == 1:
				__addCam(linker, 'Camera 2',
						render.getWindowHeight() / 2, render.getWindowHeight() / 2,
						render.getWindowWidth(), render.getWindowHeight())  # en haut à droite
			elif (((mode == 4 or mode == 6) and playerId == 1) or
					(mode == 7 and playerId == 2)):
				__addCam(linker, 'Camera ' + str(playerId + 1),
						0, 0, render.getWindowWidth() / 2,
						render.getWindowHeight() / 2)  # en bas à gauche
			elif (((mode == 4 or mode == 5) and playerId == 2) or
					(mode == 7 and playerId == 3)):
				__addCam(linker, 'Camera ' + str(playerId + 1),
						render.getWindowWidth() / 2, render.getWindowHeight() / 2,
						render.getWindowWidth(), render.getWindowHeight())  # en bas à droite


def compteurOnTop():
	for camCompteur in gl.camsCompteur:
		camCompteur.useViewport = True
		camCompteur.setOnTop()


def __addCam(linker, camCompteurName, left, bottom, right, top):
	try:
		linker.camera.setParams(
			viewPort=[left, bottom, right, top], far=gl.generalConf[2])
	except:
		linker.camera.setParams(viewPort=[left, bottom, right, top])
	camCompteur = gl.getCurrentScene().objects.get(camCompteurName)
	camCompteur.setViewport(left, bottom, right, top)
	gl.camsCompteur.append(camCompteur)


def setGraphism():
	try:
		render.setAnisotropicFiltering(gl.generalConf[0])
	except:
		pass
	try:
		render.setMistStart(gl.generalConf[1])
	except:
		pass
	try:
		# the far param is set on camera in self.__adCam
		render.setMistEnd(gl.generalConf[2])
	except:
		pass


def speedometer(playerId, gear, speed, camera):
	scene = gl.getCurrentScene()
	speedometerId = str(playerId + 1)
	ob = scene.objects.get('gear Counter ' + speedometerId)
	if not hasattr(ob, 'bflFactory'):
		ob['bflFactory'] = writeOnScreen.bflFactory(
			gl.counterPos[0][0], gl.counterPos[0][1], gl.counterPos[0][2], camera)
	if gear == 0:
		ob['bflFactory'].write('r')
	else:
		ob['bflFactory'].write(str(gear))
	scene.objects.get('pointer Counter ' + speedometerId)['kmh'] = int(speed)
	cursor = scene.objects.get('pointer Counter ' + speedometerId)
	rot = cursor.localOrientation.to_euler()
	speed = abs(speed)
	if speed > 340:
		speed = 340
	rot[2] = float((-speed + 156) / 297 * 0.876470588 * 6.28318531)
	cursor.localOrientation = rot.to_matrix()


def load():
	cont = gl.getCurrentController()
	own = cont.owner
	if gl.generalConf[4] == 'rain':
		own['rain'] = True
	#~ log("debug","load"+str(own['id']))
	if own['simulate'] is False and own['load'] is False:
		# graphisme
		setGraphism()
		# score
		conf.loadScores(gl.mapName)
		# vehicules
		gl.cars = []
		gl.objectsCars = []
		gl.camsCompteur = []
		gl.keys = [[]]
		objects.libLoad(gl.expandPath("//") + "counter.blend", "Scene")
		# conf.loadPlayer() #rechargement des configurations players
		placeCars(own)
		gl.carArrived = []
		own['load'] = True
	elif own['load'] is True:
		waitAndStart(own)
	else:
		countDownStart(own)  # to end it
		keyMapper()
		sound.musicPlayer()
		checkArrived()


def waitAndStart(own):
	own['load'] = False
	for actualCar in gl.cars:
		if actualCar[1]['car'].isLoaded() is False:
			own['load'] = True
	if own['load'] is False:
		if not 'delay' in own:
			# to avoid a bug on float in blender
			own['delay'] = int(time() * 100)
			own['load'] = True
		elif time() - (own['delay'] / 100) > 2:
			countDownStart(own)
		else:
			own['load'] = True
	if own['load'] is False:
		del(own['delay'])


def countDownStart(own):
	if not 'countdownStartTimeStamp' in own and own['simulate'] is False:
		compteurOnTop()
		gl.addScene('countdown')
		# to avoid a bug on float in blender
		own['countdownStartTimeStamp'] = int(time() * 100)
		own['load'] = True
		for actualCar in gl.cars:
			actualCar[1]['car'].startCam()
			actualCar[1]['car'].startSound()
	elif 'countdownStartTimeStamp' in own:
		compteurOnTop()
		count = time() - (own['countdownStartTimeStamp'] / 100)
		if count < 3:
			setCount(int(count))
			own['load'] = True
		elif int(count) == 3 and own['simulate'] is False:
			setCount(int(count))
			own['simulate'] = True
			for actualCar in gl.cars:
				actualCar[1]['car'].start()
				log("debug", 'start car ' +
					str(actualCar[1]['id']) + ' ' + str(actualCar[1]['vehicleType']))
				actualCar[1]['simulate'] = True
		elif count >= 4:
			try:
				gl.getSceneList()[1].end()
				log('debug', "stop countdown scene")
			except:
				log('error', "can't stop the countdown scene")
			del(own['countdownStartTimeStamp'])


def setCount(countdown):
	if countdown <= 3:
		countdownObject = gl.getSceneList()[1].objects.get('countdown')
		countdownObject['DFrame'] = countdown


def placeCars(own):
	i = 0
	j = 0
	x = False
	scene = gl.getCurrentScene()
	while i < len(gl.conf[0]):
		if (gl.conf[0][j][1] == 'human' and
				((not hasattr(gl, "dispPlayers") and i == 0) or
				gl.conf[0][j][0] in gl.dispPlayers) or
				gl.conf[0][j][0] == 'AI'):
			child = addVehicleLoader(own, j, gl.conf[0][i][0], gl.conf[0][i][3],
					gl.conf[0][i][4], scene.lights.get('sun'))
			child['AI'] = child.childrenRecursive['AI']
			child['AI'].removeParent()
			if gl.conf[0][j][1] == 'human':
				autoViewport(child['car'], gl.conf[0][i][0])
			if x:
				own.localPosition[0] += 2
				own.localPosition[1] += 2
				x = False
			else:
				own.localPosition[0] -= 2
				own.localPosition[1] += 2
				x = True
			j = j + 1
		i = i + 1
	del x


def placeStart(position, orientation, scaling):
	# set car loader
	gl.getCurrentScene().objects.get('Loader').position = position
	gl.getCurrentScene().objects.get('Loader').orientation = orientation
	gl.getCurrentScene().objects.get('Loader').scaling = scaling

	# start car loader
	gl.getCurrentScene().objects.get('Loader')['start'] = True


def keyMapper():
	keyboard = gl.keyboard
	ACTIVE = gl.KX_INPUT_ACTIVE
	JUST_ACTIVATED = gl.KX_INPUT_JUST_ACTIVATED
	for actualCar in gl.cars:  # for each car
		# if just arrived
		if (actualCar[1]['arrived'] and
				actualCar[0] not in [carArrived[0] for carArrived in gl.carArrived]):
			gl.carArrived.append([actualCar[0],
					actualCar[1]['playerName'], actualCar[1]['car'].getRaceDuration()])
		else:
			# for each actions
			for currentKey in gl.conf[0][int(actualCar[1]['id'])][2]:
				if currentKey[2] is False and keyboard.events[int(currentKey[1])] == ACTIVE:
					log("debug", str(actualCar[1])
						+ ' : ' + str(currentKey[0]))
					actualCar[1][currentKey[0]] = 1
				elif (currentKey[2] is True and
						keyboard.events[int(currentKey[1])] == JUST_ACTIVATED):
					actualCar[1][currentKey[0]] = 1
				else:
					actualCar[1][currentKey[0]] = 0


def checkArrived():
	scene = gl.getCurrentScene()
	nbCar = len(gl.cars)
	if len(gl.carArrived) == nbCar:
		for car in gl.carArrived:
			gl.scores.newScore(car[1], car[2])
		conf.saveScores()
		if gl.mapName == 'anneauDeTest':
			with open('menustat', 'w') as f:
				f.write(gl.mapName)
			f.closed
			gl.restartGame()
		else:
			scene.replace('stat')


def __writer(saver, name, position, camera, text, lastText=None):
	if position[0] != 'under' or lastText is not None:
		writerName = 'bflFactory' + str(name)
		if not hasattr(saver, writerName):
			if position[0] == "under":
				x = lastText.localX
				y = lastText.localY - lastText.localSize - position[1]
			else:
				x = position[0]
				y = position[1]
			size = position[2]
			saver[writerName] = writeOnScreen.bflFactory(x, y, size, camera)
		return saver[writerName].write(text)


def writeChekpoints(own, lastText=None):
	if own['car'].car is not None:
		text = "checkpoints : " + \
			str(own['car'].car.nextIdCheckpoint - 1) + \
			"/" + str(len(gl.checkpoints) - 1)
		return __writer(own, 'Checkpoints', gl.counterPos[1],
				own['car'].camera, text, lastText)


def writeLaps(own, lastText=None):
	if own['car'].car is not None:
		text = "laps : " + str(own['car'].car.nbLaps) + "/" + str(gl.nbLaps)
		return __writer(own, 'Laps', gl.counterPos[2],
				own['car'].camera, text, lastText)


def writeTime(own, lastText=None):
	if own['car'].car is not None and hasattr(own['car'].car, 'startTime'):
		duration = timedelta(seconds=time() - own['car'].car.startTime)
		duration = str(duration).split('.')[0]
		text = "time : " + str(duration)
		return __writer(own, 'Time', gl.counterPos[3],
				own['car'].camera, text, lastText)


def simulate():
	cont = gl.getCurrentController()
	own = cont.owner
	log("debug", "owner : " + str(own) + " id : " + str(own['id']))
	own['car'].simulate()
	speedometer(own['id'], own['gear'], own['kph'], own['car'].camera)
	lastText = writeChekpoints(own)
	lastText = writeLaps(own, lastText)
	writeTime(own, lastText)
	log("debug", str(int(own['kph'])) + ' kph')


def respawn(car):
	if car is not None and 'creator' in car:
		car['creator'].respawn()
