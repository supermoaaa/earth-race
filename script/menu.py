# -- coding: utf-8 --

import sys
import os
import time
from menugui import *

cont = gl.getCurrentController()
own = cont.owner



####################################################
#
# Initialisation du gui
#
def main():

	gl.mouse.visible = True
	confParser.loadPlayer()
	confParser.loadCounter()
	mainDir = gl.expandPath("//")
	listVt = os.listdir(os.path.expanduser(mainDir+"objects"+os.sep+"vehicles"))
	try:
		listVt.remove('.svn')
	except:
		pass


	listRoue = os.listdir(os.path.expanduser(mainDir+"objects"+os.sep+"wheels"))
	try:
		listRoue.remove('.svn')
	except:
		pass

	listMaps = os.listdir(os.path.expanduser(mainDir+"objects"+os.sep+"maps"))
	listMaps.remove('anneauDeTest')
	try:
		listMaps.remove('.svn')
	except:
		pass

	gl.mapName = listMaps[0]
	gl.listMaps = coll.deque(listMaps)
	gl.posVoitureJun = listVt.index(str(gl.conf[0][0][3]))
	gl.lstVoiture = coll.deque(listVt)
	gl.posRoueJun = listRoue.index(str(gl.conf[0][0][4]))
	gl.lstRoue = coll.deque(listRoue)
	gl.dispPlayers=[0, gl.conf[0][0][0]]
	gl.nbLaps = 1
	gl.skin = 'themes/default'

	# mirror, Anisotropic, mist start, mist end
	gl.generalConf = [True, rd.getAnisotropicFiltering(), 25, 50, 'sun']

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
	gl.device.volume = 0.3

	if hasattr(gl, 'menuStat'):
		gl.status = "MenuselectionVoiture1J"
		own["fond"] = FondGui()
		own["sys"] = jouerSoloGui(own["fond"].frame)
		own["fond"].retour_label.text = "Retour"
		own["fond"].frame.img.visible = False
		gl.LibLoad("carSelect.blend", "Scene")
		own["sys"].voiture_label.text = str(gl.conf[0][0][3])
		own["sys"].roue_label.text = str(gl.conf[0][0][4])
		gl.voiture = vehicleLinker(posObj = gl.getCurrentScene().objects['carpos1'], physic = False, parent = True)
		gl.voiture.setVehicle( str(gl.conf[0][0][3]) )
		gl.voiture.setWheels( str(gl.conf[0][0][4]) )
		delattr(gl, 'menuStat')

	else:
		gl.status = "MenuPrincipal"
		own["fond"] = FondGui()
		own["sys"] = MenuPrincipalGui(own["fond"].frame)
		own["fond"].retour_label.text = "Quitter"
		logs.log("info", "menu ok")











