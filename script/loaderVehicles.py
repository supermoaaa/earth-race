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
	child['simulate'] = False
	child['arrived'] = False
	child['cam'] = child.children['Camera']
	child['car'] = vehicleLinker( posObj = child, vehicle_type = vehicleType, wheels_type = wheelsType, camera_object = child['cam'] )
	gl.cars.append([child['id'],child])
	logs.log("debug",child.get('id'))
	return child

def autoViewport( cam, playerName ):
	if not hasattr(gl,"dispPlayers") or playerName in gl.dispPlayers:
		gl.cams.append(cam)
		scene = gl.getCurrentScene()
		if not hasattr(gl,"dispPlayers") or gl.dispPlayers[0]==0:
			gl.getCurrentScene().active_camera = cam
			camCompteur = scene.objects.get('Camera 1')
			camCompteur.setViewport( 0, 0, render.getWindowWidth(),render.getWindowHeight() )
			camCompteur.useViewport = True
			camCompteur.setOnTop()
		else:
			mode=gl.dispPlayers[0]
			id=gl.dispPlayers.index(playerName)
			if (mode==1 or mode==4) and id==1:
				cam.setViewport( 0, render.getWindowHeight/2, render.getWindowWidth, render.getWindowHeight ) #en haut
				scene.objects.get('Camera 1').setViewport( 0, render.getWindowHeight/2, render.getWindowWidth, render.getWindowHeight )
			elif (mode==1 or mode==3) and id==1:
				cam.setViewport( 0, 0, render.getWindowWidth, render.getWindowHeight/2 ) #en bas
				scene.objects.get('Camera 2').setViewport( 0, 0, render.getWindowWidth, render.getWindowHeight/2 )
			elif (mode==2 or mode==5) and id==0:
				cam.setViewport( 0, 0, render.getWindowWidth/2, render.getWindowHeight ) #à gauche
				scene.objects.get('Camera 1').setViewport( 0, 0, render.getWindowWidth/2, render.getWindowHeight )
			elif (mode==2 or mode==6) and id==1:
				cam.setViewport( render.getWindowWidth/2, 0, render.getWindowWidth, render.getWindowHeight ) #à droite
				scene.objects.get('Camera 2').setViewport( render.getWindowWidth/2, 0, render.getWindowWidth, render.getWindowHeight )
			elif (mode==3 or mode==6 or mode==7) and id==0:
				cam.setViewport( 0, render.getWindowHeight/2, render.getWindowWidth/2, render.getWindowHeight ) #en haut à gauche
				scene.objects.get('Camera 1').setViewport( 0, render.getWindowHeight/2, render.getWindowWidth/2, render.getWindowHeight )
			elif (mode==3 or mode==5 or mode==7) and id==1:
				cam.setViewport( render.getWindowHeight/2, render.getWindowHeight/2, render.getWindowWidth, render.getWindowHeight ) #en haut à droite
				scene.objects.get('Camera 2').setViewport( render.getWindowHeight/2, render.getWindowHeight/2, render.getWindowWidth, render.getWindowHeight )
			elif ((mode==4 or mode==6) and id==1) or (mode==7 and id==2):
				cam.setViewport( 0, 0, render.getWindowWidth/2, render.getWindowHeight/2 ) #en bas à gauche
				scene.objects.get('Camera '+str(id+1)).setViewport( 0, 0, render.getWindowWidth/2, render.getWindowHeight/2 )
			elif ((mode==4 or mode==5) and id==2) or (mode==7 and id==3):
				cam.setViewport( render.getWindowWidth/2, render.getWindowHeight/2, render.getWindowWidth, render.getWindowHeight ) #en bas à droite
				scene.objects.get('Camera '+str(id+1)).setViewport( render.getWindowWidth/2, render.getWindowHeight/2, render.getWindowWidth, render.getWindowHeight )
			if ((mode==1 or mode==2) and id==1) or ((mode==3 or mode==4 or mode==5 or mode==6) and id==2) or (mode==7 and id==3):
				j=0
				while j < len(gl.cams):
					gl.cams[j].useViewport = True
					camCompteur = scene.objects.get('Camera '+str(j+1))
					camCompteur.useViewport = True
					camCompteur.setOnTop()

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
		render.setMistEnd(gl.generalConf[2])
		i=0
		while i < len(gl.cams):
			gl.cams[i].lens(gl.generalConf[2])
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
	#~ logs.log("debug","load"+str(own['id']))
	if own['simulate']==False and own['load']==False:
		# graphisme
		setGraphism()
		# vehicules
		gl.cars = []
		gl.objectsCars = []
		gl.cams = []
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
				child['AI']=child.children['AI']
				child['AI'].removeParent()
				if gl.conf[0][j][1]=='human':
					autoViewport( child['cam'], gl.conf[0][i][0] )
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
					if currentKey[0] != 'upGear' and currentKey[0] != 'downGear' and keyboard.events[int(currentKey[1])] == ACTIVE:
						logs.log("debug", str(actualCar[1]) + ' : ' + str(currentKey[0]) )
						actualCar[1][currentKey[0]] = 1
					elif (currentKey[0] == 'upGear' or currentKey[0] == 'downGear') and keyboard.events[int(currentKey[1])] == JUST_ACTIVATED:
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
