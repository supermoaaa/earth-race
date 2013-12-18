from bge import logic as gl
from bge import events as events
from bge import render as render
from time import time
from datetime import timedelta
import datetime
import confParser as conf
from vehicleLinker import vehicleLinker
from logs import log
import objects
import writeOnScreen

def addVehicleLoader( source, id, playerName, vehicleType, wheelsType, shadowObj=None ):
	scene = gl.getCurrentScene()
	child = scene.addObject( 'Car', source, 0 )
	child['id'] = id
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
	child['car'] = vehicleLinker( posObj = child, vehicle_type = vehicleType, wheels_type = wheelsType, camera_object = child['cam'], shadowObj = shadowObj )
	gl.cars.append([child['id'],child])
	log("debug",child.get('id'))
	return child

def autoViewport( linker, playerName ):
	if not hasattr(gl,"dispPlayers") or playerName in gl.dispPlayers:
		scene = gl.getCurrentScene()
		if not hasattr(gl,"dispPlayers") or gl.dispPlayers[0]==0:
			#~ gl.getCurrentScene().active_camera = linker.camera.camera
			camCompteur = scene.objects.get('Camera 1')
			camCompteur.setViewport( 0, 0, render.getWindowWidth(),render.getWindowHeight() )
			gl.camsCompteur.append(camCompteur)
		else:
			mode=gl.dispPlayers[0]
			id=gl.dispPlayers.index(playerName)
			if (mode==1 or mode==4) and id==1:
				self.__addCam( linker, 'Camera 1',
					0, render.getWindowHeight()/2, render.getWindowWidth(), render.getWindowHeight() ) #en haut
			elif (mode==1 or mode==3) and id==1:
				self.__addCam( linker, 'Camera 2',
					0, 0, render.getWindowWidth(), render.getWindowHeight()/2 ) #en bas
			elif (mode==2 or mode==5) and id==0:
				self.__addCam( linker, 'Camera 1',
					0, 0, render.getWindowWidth()/2, render.getWindowHeight() ) #à gauche
			elif (mode==2 or mode==6) and id==1:
				self.__addCam( linker, 'Camera 2',
					render.getWindowWidth()/2, 0, render.getWindowWidth(), render.getWindowHeight() ) #à droite
			elif (mode==3 or mode==6 or mode==7) and id==0:
				self.__addCam( linker, 'Camera 1',
					0, render.getWindowHeight()/2, render.getWindowWidth()/2, render.getWindowHeight() ) #en haut à gauche
			elif (mode==3 or mode==5 or mode==7) and id==1:
				self.__addCam( linker, 'Camera 2',
					render.getWindowHeight()/2, render.getWindowHeight()/2, render.getWindowWidth(), render.getWindowHeight() ) #en haut à droite
			elif ((mode==4 or mode==6) and id==1) or (mode==7 and id==2):
				self.__addCam( linker, 'Camera '+str(id+1),
					0, 0, render.getWindowWidth()/2, render.getWindowHeight()/2 ) #en bas à gauche
			elif ((mode==4 or mode==5) and id==2) or (mode==7 and id==3):
				self.__addCam( linker, 'Camera '+str(id+1),
					render.getWindowWidth()/2, render.getWindowHeight()/2, render.getWindowWidth(), render.getWindowHeight() ) #en bas à droite

def compteurOnTop():
	for camCompteur in gl.camsCompteur:
		camCompteur.useViewport = True
		camCompteur.setOnTop()

def __addCam( linker, camCompteurName, left, bottom, right, top ):
	try:
		linker.camera.setParams( viewPort = [left, bottom, right, top], far = gl.generalConf[2] )
	except:
		linker.camera.setParams( viewPort = [left, bottom, right, top] )
	camCompteur = scene.objects.get(camCompteurName)
	camCompteur.setViewport( left, bottom, right, top )
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
		render.setMistEnd(gl.generalConf[2]) #the far param is set on camera in self.__adCam
	except:
		pass

def speedometer( id, gear, speed, camera):
	scene = gl.getCurrentScene()
	id=str(id+1)
	ob = scene.objects.get('gear Counter '+id)
	if not hasattr(ob, 'bflFactory'):
		ob['bflFactory'] = writeOnScreen.bflFactory( gl.counterPos[0][0], gl.counterPos[0][1], gl.counterPos[0][2], camera )
	if gear==0:
		ob['bflFactory'].write( 'r' )
	else:
		ob['bflFactory'].write( str(gear) )
	scene.objects.get('pointer Counter '+id)['kmh'] = int(speed)
	cursor = scene.objects.get('pointer Counter '+id)
	rot = cursor.localOrientation.to_euler()
	speed = abs(speed)
	if speed>340:
		speed=340
	rot[2] = float((-speed + 156) / 297 * 0.876470588 * 6.28318531)
	cursor.localOrientation = rot.to_matrix()

def load():
	cont = gl.getCurrentController()
	own = cont.owner
	if gl.generalConf[4] == 'rain':
		own['rain'] = True
	#~ log("debug","load"+str(own['id']))
	if own['simulate']==False and own['load']==False:
		# graphisme
		setGraphism()
		# score
		conf.loadScores(gl.mapName)
		# vehicules
		gl.cars = []
		gl.objectsCars = []
		gl.camsCompteur = []
		gl.keys = [[]]
		objects.libLoad(gl.expandPath("//")+"counter.blend", "Scene")
		#conf.loadPlayer() #rechargement des configurations players
		placeCars(own)
		gl.carArrived=[]
		own['load']=True
	elif own['load']==True:
		waitAndStart(own)
	else:
		countDownStart(own) #to end it
		keyMapper()
		checkArrived()

def waitAndStart(own):
	own['load']=False
	for actualCar in gl.cars:
		if actualCar[1]['car'].isLoaded()==False:
			own['load']=True
	if own['load']==False:
		if not 'delay' in own:
			own['delay'] = int(time()*100) # to avoid a bug on float in blender
			own['load']=True
		elif time()-(own['delay']/100)>2:
			countDownStart(own)
		else:
			own['load']=True
	if own['load']==False:
		del(own['delay'])

def countDownStart(own):
	if not 'countdownStartTimeStamp' in own and own['simulate']==False:
		compteurOnTop()
		gl.addScene('countdown')
		own['countdownStartTimeStamp'] = int(time()*100) # to avoid a bug on float in blender
		own['load'] = True
		for actualCar in gl.cars:
			actualCar[1]['car'].startCam()
	elif 'countdownStartTimeStamp' in own:
		compteurOnTop()
		count = time()-(own['countdownStartTimeStamp']/100)
		if count <3:
			setCount(int(count))
			own['load'] = True
		elif int(count) == 3 and own['simulate'] == False:
			setCount(int(count))
			own['simulate']=True
			for actualCar in gl.cars:
				actualCar[1]['car'].start()
				log("debug",'start car '+str(actualCar[1]['id'])+' '+str(actualCar[1]['vehicleType']))
				actualCar[1]['simulate']=True
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
	while i < len(gl.conf[0]) :
		if gl.conf[0][j][1]=='human' and ( (not hasattr(gl,"dispPlayers") and i==0) or gl.conf[0][j][0] in gl.dispPlayers) or gl.conf[0][j][0]=='AI':
			child=addVehicleLoader( own, j, gl.conf[0][i][0], gl.conf[0][i][3], gl.conf[0][i][4], scene.lights.get('sun') )
			child['AI']=child.childrenRecursive['AI']
			child['AI'].removeParent()
			if gl.conf[0][j][1]=='human':
				autoViewport( child['car'], gl.conf[0][i][0] )
			if x:
				own.localPosition[0] += 2
				own.localPosition[1] += 2
				x = False
			else:
				own.localPosition[0] -= 2
				own.localPosition[1] += 2
				x = True
			j = j+1
		i = i+1
	del x

def placeStart(position,orientation,scaling):
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
	for actualCar in gl.cars: # for each car
		if actualCar[1]['arrived'] and actualCar[0] not in [carArrived[0] for carArrived in gl.carArrived]: # if just arrived
			gl.carArrived.append([ actualCar[0], actualCar[1]['playerName'], actualCar[1]['car'].getRaceDuration() ])
		else:
			for currentKey in gl.conf[0][int(actualCar[1]['id'])][2]: # for each actions
				if currentKey[2] == False and keyboard.events[int(currentKey[1])] == ACTIVE:
					log("debug", str(actualCar[1]) + ' : ' + str(currentKey[0]) )
					actualCar[1][currentKey[0]] = 1
				elif currentKey[2] == True and keyboard.events[int(currentKey[1])] == JUST_ACTIVATED:
					actualCar[1][currentKey[0]] = 1
				else:
					actualCar[1][currentKey[0]] = 0

def checkArrived():
	scene = gl.getCurrentScene()
	nbCar=len(gl.cars)
	if len(gl.carArrived)==nbCar:
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

def __writer( saver, name, position, camera, text, lastText = None):
	if position[0]!='under' or lastText!=None:
		writerName = 'bflFactory'+str(name)
		if not hasattr(saver, writerName):
			if position[0]=="under":
				x = lastText.localX
				y = lastText.localY - lastText.localSize - position[1]
			else:
				x = position[0]
				y = position[1]
			size = position[2]
			saver[writerName] = writeOnScreen.bflFactory( x, y, size, camera )
		return saver[writerName].write(text)

def writeChekpoints(own, lastText = None):
	if own['car'].car != None:
		text = "checkpoints : " + str(own['car'].car.nextIdCheckpoint-1)+"/"+str(len(gl.checkpoints)-1)
		return __writer( own, 'Checkpoints', gl.counterPos[1], own['car'].camera, text, lastText)

def writeLaps( own, lastText = None ):
	if own['car'].car != None:
		text = "laps : " + str(own['car'].car.nbLaps)+"/"+str(gl.nbLaps)
		return __writer( own, 'Laps', gl.counterPos[2], own['car'].camera, text, lastText)

def writeTime( own, lastText = None):
	if own['car'].car != None and hasattr(own['car'].car, 'startTime'):
		duration = timedelta(seconds=time()-own['car'].car.startTime)
		duration = str(duration).split('.')[0]
		text = "time : " + str(duration)
		return __writer( own, 'Time', gl.counterPos[3], own['car'].camera, text, lastText)

def simulate():
	cont = gl.getCurrentController()
	own = cont.owner
	log("debug","owner : " + str(own) + " id : " + str(own['id']) )
	own['car'].simulate()
	speedometer( own['id'], own['gear'], own['kph'], own['car'].camera )
	lastText = writeChekpoints(own)
	lastText = writeLaps(own,lastText)
	writeTime(own,lastText)
	log("debug", str(int(own['kph'])) + ' kph' )

def respawn(car):
	if car != None and 'creator' in car:
		car['creator'].respawn()
