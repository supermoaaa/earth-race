from bge import logic as gl
from bge import events as events
from bge import render as render
import confParser as conf
from vehicleLinker import vehicleLinker
import objects
import logs

def addVehicleLoader( source, id, vehicleType, wheelsType ):
	scene = gl.getCurrentScene()
	child = scene.addObject( 'Car', source, 0 )
	child['id'] = id
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
	child['gear'] = 0
	child['cam'] = child.childrenRecursive['Camera']
	child['car'] = vehicleLinker( posObj = child, vehicle_type = vehicleType, wheels_type = wheelsType, camera_object = child['cam'] )
	gl.cars.append([child['id'],child])
	logs.log("debug",child.get('id'))
	return child

def autoViewport( linker, playerName ):
	if not hasattr(gl,"dispPlayers") or playerName in gl.dispPlayers:
		scene = gl.getCurrentScene()
		if not hasattr(gl,"dispPlayers") or gl.dispPlayers[0]==0:
			gl.getCurrentScene().active_camera = linker.camera.camera
			camCompteur = scene.objects.get('Camera 1')
			camCompteur.setViewport( 0, 0, render.getWindowWidth(),render.getWindowHeight() )
			camCompteur.useViewport = True
			camCompteur.setOnTop()
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
			if ((mode==1 or mode==2) and id==1) or ((mode==3 or mode==4 or mode==5 or mode==6) and id==2) or (mode==7 and id==3):
				j=0
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

def speedometer( id, gear, speed):
	scene = gl.getCurrentScene()
	id=str(id+1)
	scene.objects.get('gear Counter '+id)['DFrame'] = gear
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
	scene = gl.getCurrentScene()
	if gl.generalConf[4] == 'rain':
		own['rain'] = True
	#~ logs.log("debug","load"+str(own['id']))
	if own['simulate']==False and own['load']==False:
		# graphisme
		setGraphism()
		# vehicules
		gl.cars = []
		gl.objectsCars = []
		gl.camsCompteur = []
		vehicles = []
		wheels = []
		gl.keys = [[]]
		i = 0
		j = 0
		x = False
		objects.libLoad(gl.expandPath("//")+"counter.blend", "Scene")
		#conf.loadPlayer() #rechargement des configurations players
		while i < len(gl.conf[0]) :
			if gl.conf[0][j][1]=='human' and ( (not hasattr(gl,"dispPlayers") and i==0) or gl.conf[0][j][0] in gl.dispPlayers) or gl.conf[0][j][0]=='AI':
				child=addVehicleLoader( own, j, gl.conf[0][i][3], gl.conf[0][i][4] )
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
		gl.carArrived=[]
		own['load']=True
	elif own['load']==True:
		own['load']=False
		for actualCar in gl.cars:
			if actualCar[1]['car'].isLoaded()==False:
				own['load']=True
		if own['load']==False:
			own['simulate']=True
			for actualCar in gl.cars:
				actualCar[1]['car'].start()
				logs.log("debug",'start car '+str(actualCar[1]['id'])+' '+str(actualCar[1]['vehicleType']))
				actualCar[1]['simulate']=True
	else:
		keyboard = gl.keyboard
		ACTIVE = gl.KX_INPUT_ACTIVE
		JUST_ACTIVATED = gl.KX_INPUT_JUST_ACTIVATED
		nbCar=len(gl.cars)
		for actualCar in gl.cars: # for each car
			if actualCar[1]['arrived'] and actualCar[0] not in gl.carArrived: # if just arrived
				gl.carArrived.append([ actualCar[0], actualCar[1]['car'].getRaceDuration() ])
			else:
				for currentKey in gl.conf[0][int(actualCar[1]['id'])][2]: # for each actions
					if currentKey[2] == False and keyboard.events[int(currentKey[1])] == ACTIVE:
						logs.log("debug", str(actualCar[1]) + ' : ' + str(currentKey[0]) )
						actualCar[1][currentKey[0]] = 1
					elif currentKey[2] == True and keyboard.events[int(currentKey[1])] == JUST_ACTIVATED:
						actualCar[1][currentKey[0]] = 1
					else:
						actualCar[1][currentKey[0]] = 0
		if len(gl.carArrived)==nbCar:
			if gl.mapName == 'anneauDeTest':
				with open('menustat', 'w') as f:
					f.write(gl.mapName)
				f.closed
				gl.restartGame()
			else:
				scene.replace('stat')

def placeStart(position,orientation,scaling):
	# set car loader
	gl.getCurrentScene().objects.get('Loader').position = position
	gl.getCurrentScene().objects.get('Loader').orientation = orientation
	gl.getCurrentScene().objects.get('Loader').scaling = scaling

	# set camera
	gl.getCurrentScene().objects.get('Camera').position = position
	gl.getCurrentScene().objects.get('Camera').localPosition[1] -= 20
	gl.getCurrentScene().objects.get('Camera').position[2] += 6

	# start car loader
	gl.getCurrentScene().objects.get('Loader')['start'] = True

def simulate():
	cont = gl.getCurrentController()
	own = cont.owner
	if own['simulate']:
		logs.log("debug","owner : " + str(own) + " id : " + str(own['id']) )
		own['car'].simulate()
	speedometer( own['id'], own['gear'], own['kph'])
	logs.log("debug", str(int(own['kph'])) + ' kph' )
