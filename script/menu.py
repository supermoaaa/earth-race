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
	gl.status = "MenuPrincipal"
	gl.mouse.visible = True
	confParser.loadPlayer()
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
	gl.nbTours = 1
	gl.skin = 'themes/default'

	# mirror, Anisotropic, volume musique
	gl.generalConf = [True, rd.getAnisotropicFiltering(), 50]
	print(gl.lstRoue)
	print(gl.dispPlayers)
	print(gl.lstVoiture)
	print(gl.listMaps)
	print(gl.mapName)

	own["fond"] = FondGui()
	own["sys"] = MenuPrincipalGui(own["fond"].frame)
	own["fond"].retour_label.text = "Quitter"


	#chargement de l'audio du menu
	gl.device = aud.device()
	# load sound file (it can be a video file with audio)
	factory = aud.Factory('2748.wav')
	# if the audio is not too big and will be used often you can buffer it
	gl.factory_buffered = aud.Factory.buffer(factory)
	gl.device.volume = 0.3


		



