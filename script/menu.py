# -- coding: utf-8 --


from os import path, sep, listdir
from menugui import *


cont = gl.getCurrentController()
own = cont.owner



####################################################
#
# Initialisation du gui
#
def main():

	gl.mouse.visible = True
	confParser.loadConf()
	confParser.loadPlayer()
	confParser.loadCounter()
	mainDir = gl.expandPath("//")
	gl.word =[]
	listLangue = listdir(path.expanduser(mainDir+"lang"))

	with open(mainDir+"lang"+sep+gl.generalConf[5]+".txt", 'r') as f:
		for element in f.readlines():
			gl.word.append(element.rstrip('\n'))
	
	
	listVt = listdir(path.expanduser(mainDir+"objects"+sep+"vehicles"))
	try:
		listVt.remove('.svn')
	except:
		pass


	listRoue = listdir(path.expanduser(mainDir+"objects"+sep+"wheels"))
	try:
		listRoue.remove('.svn')
	except:
		pass

	listMaps = listdir(path.expanduser(mainDir+"objects"+sep+"maps"))
	listMaps.remove('anneauDeTest')
	try:
		listMaps.remove('.svn')
	except:
		pass

	listRadio = listdir(path.expanduser(mainDir+"music"))
	try:
		listRadio.remove('.svn')
	except:
		pass

	gl.currentRadio = listRadio.index(gl.sound[2])
	gl.listeRadio = deque(listRadio)
	gl.mapName = listMaps[0]
	gl.listMaps = deque(listMaps)
	gl.posVoitureJun = listVt.index(str(gl.conf[0][0][3]))
	gl.lstVoiture = deque(listVt)
	gl.posRoueJun = listRoue.index(str(gl.conf[0][0][4]))
	gl.lstRoue = deque(listRoue)
	gl.dispPlayers=[0, gl.conf[0][0][0]]
	gl.nbLaps = 1
	gl.CurrentColor = [0.1, 0.3, 0.5, 1.0]
	gl.skin = 'themes/default'
	gl.IA =[]

	logs.log("info", gl.lstRoue)
	logs.log("info", gl.dispPlayers)
	logs.log("info", gl.lstVoiture)
	logs.log("info", gl.listMaps)
	logs.log("info", gl.mapName)

	#chargement de l'audio du menu
	gl.device = aud.device()
	# load sound file (it can be a video file with audio)
	factory = aud.Factory('2748.wav')
	# if the audio is not too big and will be used often you can buffer it
	gl.factory_buffered = aud.Factory.buffer(factory)
	gl.device.volume = gl.sound[1]


	if hasattr(gl, 'menuStat'):
		gl.status = "MenuselectionVoiture1J"
		own["fond"] = FondGui()
		own["sys"] = jouerSoloGui(own["fond"].frame)
		own["fond"].retour_label.text = "Retour"
		own["fond"].frame.img.visible = False
		gl.LibLoad(gl.expandPath("//")+"carSelect.blend", "Scene")
		own["sys"].voiture_label.text = str(gl.conf[0][0][3])
		own["sys"].roue_label.text = str(gl.conf[0][0][4])
		gl.voiture = vehicleLinker(posObj = gl.getCurrentScene().objects['carpos1'], physic = False, parent = True)
		gl.voiture.setVehicle( str(gl.conf[0][0][3]) )
		gl.voiture.setWheels( str(gl.conf[0][0][4]) )
		gl.getCurrentScene().active_camera = gl.getCurrentScene().objects['CameraPlayer1']
		gl.colorCar1 = gl.getCurrentScene().addObject("color ramp", "car1")
		gl.colorGlass1 = gl.getCurrentScene().addObject("color ramp", "glass1")
		delattr(gl, 'menuStat')

	else:
		gl.status = "MenuPrincipal"
		own["fond"] = FondGui()
		own["sys"] = MenuPrincipalGui(own["fond"].frame)
		own["fond"].retour_label.text = "Quitter"
		logs.log("info", "menu ok")











