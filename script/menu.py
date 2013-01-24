# -- coding: utf-8 --

import sys
import os
import bgui
import bge
import time
from bge import logic as gl
from bge import render as rd
from bge import events as ev
import confParser
from vehicleLinker import vehicleLinker
import collections as coll


#sys.path.append(gl.expandPath("//"))

#fonctions non Bgui
####viewport 2 joueurs
def viewportP(playerCams, mode):

	width = rd.getWindowWidth()
	height = rd.getWindowHeight()

	# player cameras
	player1 = playerCams[0]
	player2 = playerCams[1]
	#vertical
	if mode == 2:
	
		# Player 1 viewport: left side
		left_1 = 0; bottom_1 = 0; right_1 = width/2; top_1 = height
		   
		#  Player 2 viewport: right side
		left_2 = width/2; bottom_2 = 0; right_2 = width; top_2 = height 
	
	#horizontal
	else:
		# Player 1 viewport: top half
		left_1 = 0; bottom_1 = height/2; right_1 = width; top_1 = height
		   
		#  Player 2 viewport: bottom half
		left_2 = 0; bottom_2 = 0; right_2 = width; top_2 = height/2


	player1.setViewport( int(left_1), int(bottom_1), int(right_1), int(top_1))
	player2.setViewport( int(left_2), int(bottom_2), int(right_2), int(top_2))
	player1.useViewport = True
	player2.useViewport = True 

####viewport 4 joueurs
def viewportPQuatre(playerCams):

	width = rd.getWindowWidth()
	height = rd.getWindowHeight()

	# player cameras
	player1 = playerCams[0]
	player2 = playerCams[1]
	player3 = playerCams[2]
	player4 = playerCams[3]

	# Player 1 viewport:  top left side
	left_1 = 0; bottom_1 = height/2; right_1 = width/2; top_1 = height
	   
	#  Player 2 viewport: top right side
	left_2 = width/2; bottom_2 = height/2; right_2 = width; top_2 = height 


	# Player 3 viewport: top half
	left_3 = 0; bottom_3 = 0; right_3 = width/2; top_3 = height/2
	   
	#  Player 4 viewport: bottom half
	left_4 = width/2; bottom_4 = 0; right_4 = width; top_4 = height/2

	player1.setViewport( int(left_1), int(bottom_1), int(right_1), int(top_1))
	player2.setViewport( int(left_2), int(bottom_2), int(right_2), int(top_2))
	player3.setViewport( int(left_3), int(bottom_3), int(right_3), int(top_3))
	player4.setViewport( int(left_4), int(bottom_4), int(right_4), int(top_4))
	player1.useViewport = True
	player2.useViewport = True
	player3.useViewport = True
	player4.useViewport = True
	
class MySys(bgui.System):
	"""
	A subclass to handle our game specific gui
	"""

	### fonctions de retour a la page

	def quitter(self, quitter_button):
		bge.logic.endGame()

	def retour(self, retour_button):
		if self.joueurSolo_menu.visible == True:
			gl.LibFree("carSelect.blend")
		self.options_menu.visible = False
		self.main_menu.visible = True
		self.multijouers_menu.visible = False
		self.joueurSolo_menu.visible = False
		self.telechargement_menu.visible = False
		if hasattr(self , 'voiture'):
			del self.voiture
	def retourMulti(self, retour_button):
		self.multijouers_menu.visible = True
		self.ecransplitter_menu.visible = False

	def retoursolo(self, retour_button):
		self.joueurSolo_menu.visible = True
		self.circuitSolo_menu.visible = False

	def retourSelVoitureDeuxJ(self, retourSelVoitureDeuxJ_button):
		if self.selectionVoitureDeuxJ_menu.visible == True:
			gl.LibFree("carSelect.blend")
		self.ecransplitter_menu.visible = True
		self.selectionVoitureDeuxJ_menu.visible = False
		if hasattr(self , 'voiture'):
			del self.voiture
		if hasattr(self , 'voitureDeux'):
			del self.voitureDeux

	def retourSelVoitureQuatreJ(self, retourSelVoitureQuatreJ_button):
		if self.selectionVoitureQuatreJ_menu.visible == True:
			gl.LibFree("carSelect.blend")
		self.ecransplitter_menu.visible = True
		self.selectionVoitureQuatreJ_menu.visible = False
		if hasattr(self , 'voiture'):
			del self.voiture
		if hasattr(self , 'voitureDeux'):
			del self.voitureDeux
		if hasattr(self , 'voitureTrois'):
			del self.voitureTrois
		if hasattr(self , 'voitureQuatre'):
			del self.voitureQuatre
		### fonctions du menu principal

	def optionsM(self, options_button):
		self.options_menu.visible = True
		self.main_menu.visible = False
		self.multijouers_menu.visible = False
		self.joueurSolo_menu.visible = False
		self.telechargement_menu.visible = False

	def multijoueurM(self, multijoueur_button):
		self.multijouers_menu.visible = True
		self.options_menu.visible = False
		self.main_menu.visible = False
		self.joueurSolo_menu.visible = False
		self.telechargement_menu.visible = False

	def telechargementM(self, multijoueur_button):
		self.multijouers_menu.visible = False
		self.options_menu.visible = False
		self.main_menu.visible = False
		self.joueurSolo_menu.visible = False
		self.telechargement_menu.visible = True

	def joueurSoloM(self, joueursolo_button):
		self.joueurSolo_menu.visible = True
		self.multijouers_menu.visible = False
		self.options_menu.visible = False
		self.main_menu.visible = False
		self.telechargement_menu.visible = False
		gl.LibLoad("carSelect.blend", "Scene")
		self.voiture_label.text = str(gl.conf[0][0][3])
		posObj = gl.getCurrentScene().objects['carpos1']
		self.Voiture = vehicleLinker(posObj = posObj, physic = False, parent = True)
		self.Voiture.setVehicle( str(gl.conf[0][0][3]) )
		self.Voiture.setWheels( str(gl.conf[0][0][4]) )

		### fonctions du menu multijouers
	def ecranSplitM(self, ecransplitter_button):
		self.multijouers_menu.visible = False
		self.ecransplitter_menu.visible = True
		gl.dispPlayers[0] = 1

		### fonctions du menu des options
	def affichageM(self, affichage_button):
		if self.affichage_menu.visible == True:
			pass
		else:
			self.affichage_menu.visible = True
			self.commande_menu.visible = False
			self.son_menu.visible = False
			self.options_joueurs.visible = False

	def commandeM(self, commande_button):
		if self.commande_menu.visible == True:
			pass
		else:
			self.commande_menu.visible = True
			self.affichage_menu.visible = False
			self.son_menu.visible = False
			self.options_joueurs.visible = False

	def sonM(self, son_menu):
		if self.son_menu.visible == True:
			pass
		else:
			self.son_menu.visible = True
			self.commande_menu.visible = False
			self.affichage_menu.visible = False
			self.options_joueurs.visible = False

	def joueursM(self, joueurs_button):
		if self.options_joueurs.visible == True:
			pass
		else:
			self.options_joueurs.visible = True
			self.son_menu.visible = False
			self.commande_menu.visible = False
			self.affichage_menu.visible = False

		### fonctions du menu son


	def volumeMup(self, flecheH_button):
		if gl.musiqueVolume == 100:
			gl.musiqueVolume = 100
		else:
			gl.musiqueVolume += 1
			#gl.musiqueVolume = float(Decimal(str(gl.musiqueVolume)).quantize(Decimal('0.1'), decimal.ROUND_UP))
			self.volumeG_label.text = str(gl.musiqueVolume)

	def volumeMdown(self, flecheB_button):
		if gl.musiqueVolume <= 0:
			gl.musiqueVolume = 0
		else:
			gl.musiqueVolume -= 1
			#gl.musiqueVolume = float(Decimal(str(gl.musiqueVolume)).quantize(Decimal('0.1'), decimal.ROUND_DOWN))
			self.volumeG_label.text = str(gl.musiqueVolume)

		### fonctions du menu nom des joueurs

	def joueur1_on_input_enter(self, joueur1_input):
		joueur1_input.deactivate()
		gl.conf[0][0][0] = joueur1_input.text
		confParser.savePlayer()

	def joueur2_on_input_enter(self, joueur2_input):
		joueur2_input.deactivate()
		gl.conf[0][1][0] = joueur2_input.text
		confParser.savePlayer()

	def joueur3_on_input_enter(self, joueur3_input):
		joueur3_input.deactivate()
		gl.conf[0][2][0] = joueur3_input.text
		confParser.savePlayer()

	def joueur4_on_input_enter(self, joueur4_input):
		joueur4_input.deactivate()
		gl.conf[0][3][0] = joueur4_input.text
		confParser.savePlayer()

		### fonctions du menu ecran spliter

	def deuxjoueursM(self, deuxjoueurs_button):
		self.deuxjoueurs_menu.visible = True
		self.troisjoueurs_menu.visible = False
		self.quatrejoueurs_menu.visible = False

	def troisjoueursM(self, troisjoueurs_button):
		self.deuxjoueurs_menu.visible = False
		self.troisjoueurs_menu.visible = True
		self.quatrejoueurs_menu.visible = False

	def quatrejoueursM(self, quatrejoueurs_button):
		self.deuxjoueurs_menu.visible = False
		self.troisjoueurs_menu.visible = False
		self.quatrejoueurs_menu.visible = True

	def ecranDeuxJM(self, disposition_button):
		if self.deuxjoueurs_ecranHorizontal.visible == True:
			self.deuxjoueurs_ecranHorizontal.visible = False
			self.deuxjoueurs_ecranVertical.visible = True
			gl.dispPlayers[0] = 2
		else:
			self.deuxjoueurs_ecranHorizontal.visible = True
			self.deuxjoueurs_ecranVertical.visible = False
			gl.dispPlayers[0] = 1

	def placementJoueurDeux(self, placementJoueur_button):
		if self.posJoueurHH_label.text == "JOUEUR 1":
			self.posJoueurHH_label.text = self.posJoueurVH_label.text = "JOUEUR 2"
			self.posJoueurHB_label.text = self.posJoueurVB_label.text = "JOUEUR 1"
		else:
			self.posJoueurHH_label.text = self.posJoueurVH_label.text = "JOUEUR 1"
			self.posJoueurHB_label.text = self.posJoueurVB_label.text = "JOUEUR 2"

	def validerDeuxJPos(self, validerplacementJoueur_button):
		self.ecransplitter_menu.visible = False
		self.selectionVoitureDeuxJ_menu.visible = True
		gl.LibLoad("carSelect.blend", "Scene")
		scene = gl.getCurrentScene()
		camPlayer1 = scene.objects['CameraPlayer1']
		camPlayer2 = scene.objects['CameraPlayer2']
		viewportP([camPlayer1, camPlayer2], gl.dispPlayers[0])
		
		posvUn = gl.getCurrentScene().objects['carpos1']
		self.Voiture = vehicleLinker(posObj = posvUn, physic = False, parent = True)
		self.Voiture.setVehicle( str(gl.conf[0][0][3]) )
		self.Voiture.setWheels( str(gl.conf[0][0][4]) )

		posvDeux = gl.getCurrentScene().objects['carpos2']
		self.VoitureDeux = vehicleLinker(posObj = posvDeux, physic = False, parent = True)
		self.VoitureDeux.setVehicle( str(gl.conf[0][1][3]) )
		self.VoitureDeux.setWheels( str(gl.conf[0][1][4]) )

	def validerQuatreJPos(self, validerplacementJoueur_button):
		self.ecransplitter_menu.visible = False
		self.selectionVoitureQuatreJ_menu.visible = True
		gl.LibLoad("carSelect.blend", "Scene")
		scene = gl.getCurrentScene()
		camPlayer1 = scene.objects['CameraPlayer1']
		camPlayer2 = scene.objects['CameraPlayer2']
		camPlayer3 = scene.objects['CameraPlayer3']
		camPlayer4 = scene.objects['CameraPlayer4']
		viewportPQuatre([camPlayer1, camPlayer2, camPlayer3, camPlayer4])

		posvUn = gl.getCurrentScene().objects['carpos1']
		self.Voiture = vehicleLinker(posObj = posvUn, physic = False, parent = True)
		self.Voiture.setVehicle( str(gl.conf[0][0][3]) )
		self.Voiture.setWheels( str(gl.conf[0][0][4]) )

		posvDeux = gl.getCurrentScene().objects['carpos2']
		self.VoitureDeux = vehicleLinker(posObj = posvDeux, physic = False, parent = True)
		self.VoitureDeux.setVehicle( str(gl.conf[0][1][3]) )
		self.VoitureDeux.setWheels( str(gl.conf[0][1][4]) )

		posvTrois = gl.getCurrentScene().objects['carpos3']
		self.VoitureTrois = vehicleLinker(posObj = posvTrois, physic = False, parent = True)
		self.VoitureTrois.setVehicle( str(gl.conf[0][2][3]) )
		self.VoitureTrois.setWheels( str(gl.conf[0][2][4]) )

		posvQuatre = gl.getCurrentScene().objects['carpos4']
		self.VoitureQuatre = vehicleLinker(posObj = posvQuatre, physic = False, parent = True)
		self.VoitureQuatre.setVehicle( str(gl.conf[0][3][3]) )
		self.VoitureQuatre.setWheels( str(gl.conf[0][3][4]) )

		### fonctions du menu choix des voitures 2 joueurs


		
		### fonctions du menu ecran selection voiture

	def circuitSolo(self, validerVoiture_button):
		self.joueurSolo_menu.visible = False
		self.circuitSolo_menu.visible = True
		if hasattr(self , 'voiture'):
			del self.voiture


	def testerVoiture(self, testerVoiture_button):
		del(self.Voiture)
		confParser.savePlayer()
		gl.mapName = "jungle"
		scene = gl.getCurrentScene()
		for lib in gl.LibList():
			gl.LibFree(lib)
		scene.replace('game')

	def leftwheels(self, flecheGRoue_button):
		gl.lstRoue.rotate(-1)

		gl.conf[0][0][4] = gl.lstRoue[gl.posRoueJun]
		self.Voiture.setWheels( str(gl.conf[0][0][4]) )

	def rightwheels(self, flecheRoue_button):
		gl.lstRoue.rotate(1)

		gl.conf[0][0][4] = gl.lstRoue[gl.posRoueJun]
		self.Voiture.setWheels( str(gl.conf[0][0][4]) )

	def leftcar(self, flecheG_button):
		gl.lstVoiture.rotate(-1)
		gl.conf[0][0][3] = gl.lstVoiture[gl.posVoitureJun]
		self.Voiture.setVehicle( str(gl.conf[0][0][3]) )
		self.voiture_label.text = str(gl.conf[0][0][3])

	def rightcar(self, fleche_button):
		gl.lstVoiture.rotate(1)
		gl.conf[0][0][3] = gl.lstVoiture[gl.posVoitureJun]
		self.Voiture.setVehicle( str(gl.conf[0][0][3]) )
		self.voiture_label.text = str(gl.conf[0][0][3])

		### fonctions du menu circuit solo
	def rightMap(self, flecheVdDR_button):
		gl.listMaps.rotate(1)
		gl.mapName = gl.listMaps[0]
		self.circuit_label.text = "nom du circuit:"+str(gl.mapName)

	def leftMap(self, flecheVdGA_button):
		gl.listMaps.rotate(-1)
		gl.mapName = gl.listMaps[0]
		self.circuit_label.text = "nom du circuit:"+str(gl.mapName)
		
	def rightTours(self, flecheToursDR_button):
		if gl.nbTours <= 8:
			gl.nbTours += 1
		else:
			gl.nbTours = 1
		self.nbToursSolo_label.text = str(gl.nbTours)

	def leftTours(self, flecheToursGA_button):
		if gl.nbTours >= 2:
			gl.nbTours -= 1
		else:
			gl.nbTours = 9
		self.nbToursSolo_label.text = str(gl.nbTours)



		### fonctions du menu commande
	def sauvegardeComUn(self, sauvegardeComUn_button):
		confParser.savePlayer()


	def __init__(self):
		# Initialize the system
		bgui.System.__init__(self, 'themes/default')
		self.clear_time = time.time()
		self.note_visible = False

		self.frame = bgui.Frame(self, 'frame', aspect=(4/3),
					options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
		self.frame.visible = False
#--------------menu principal----------------#
#
#
#
		self.main_menu = bgui.Frame(self, 'main_menu', border=1, size=[1.0, 1.0],
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
		self.main_menu.visible = True

		self.main_menu.img = bgui.Image(self.main_menu, 'image', 'menu.jpg', size=[1.0, 1.0],
			options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX|bgui.BGUI_CACHE)

############///////////frame info \\\\\\\\\\\\\\#################

		self.info_ecran = bgui.Frame(self.main_menu, 'info_ecran', sub_theme='ecran', border=1, size=[0.64, 0.75], pos=[0.06, 0.02],
				options=bgui.BGUI_DEFAULT)

		self.info_label = bgui.Label(self.info_ecran, 'info_label', text="bienvenue " + str(gl.conf[0][0][0]), pt_size=24, pos=[0.02, 0.84],
				options=bgui.BGUI_DEFAULT)

#############bouton joueursolo ############################
		self.joueursolo_button = bgui.ImageButton(self.main_menu, 'joueursolo', sub_theme='menu',
				size=[0.24, 0.08], pos=[0.75, 0.48])

		self.joueursolo_label = bgui.Label(self.joueursolo_button, 'joueursolo', text="JOUEUR SOLO", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		# Setup an on_click callback
		self.joueursolo_button.on_click = self.joueurSoloM
#############bouton multijoueur ############################
		self.multijoueur_button = bgui.ImageButton(self.main_menu, 'multijoueur', sub_theme='menu',
				size=[0.24, 0.08], pos=[0.75, 0.38])

		self.multijoueur_label = bgui.Label(self.multijoueur_button, 'multijoueur', text="MULTIJOUEURS", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		# Setup an on_click callback
		self.multijoueur_button.on_click = self.multijoueurM

#############bouton telechargements ############################
		self.telechargements_button = bgui.ImageButton(self.main_menu, 'telechargements', sub_theme='menu',
				size=[0.24, 0.08], pos=[0.75, 0.28])

		self.telechargements_label = bgui.Label(self.telechargements_button, 'telechargements', text="ADDONS", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		# Setup an on_click callback
		self.telechargements_button.on_click = self.telechargementM

#############bouton options############################
		self.options_button = bgui.ImageButton(self.main_menu, 'options', sub_theme='menu',
				size=[0.24, 0.08], pos=[0.75, 0.18])

		self.options_label = bgui.Label(self.options_button, 'options', text="OPTIONS", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
		# Setup an on_click callback
		self.options_button.on_click = self.optionsM

#############bouton quitter############################
		self.quitter_button = bgui.ImageButton(self.main_menu, 'quitter', sub_theme='menu',
				size=[0.24, 0.08], pos=[0.75, 0.08])

		self.quitter_label = bgui.Label(self.quitter_button, 'quitter', text="QUITTER", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
		# Setup an on_click callback
		self.quitter_button.on_click = self.quitter


#--------------menu multijouers----------------#
#
#
#
		self.multijouers_menu = bgui.Frame(self, 'multijouers_menu', border=1, size=[1.0, 1.0],
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		self.multijouers_menu.img = bgui.Image(self.multijouers_menu, 'image', 'menu.jpg', size=[1.0, 1.0],
			options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX|bgui.BGUI_CACHE)

#############bouton ecransplitter############################
		self.ecransplitter_button = bgui.ImageButton(self.multijouers_menu, 'ecransplitter', sub_theme='menu',
				size=[0.24, 0.08], pos=[0.4, 0.55])

		self.ecransplitter_label = bgui.Label(self.ecransplitter_button, 'ecransplitter', text="ECRAN SPLITTER", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		# Setup an on_click callback
		self.ecransplitter_button.on_click = self.ecranSplitM
#############bouton reseaulocal############################
		self.reseauLocal_button = bgui.ImageButton(self.multijouers_menu, 'reseauLocal', sub_theme='menu',
				size=[0.24, 0.08], pos=[0.4, 0.45])

		self.reseauLocal_label = bgui.Label(self.reseauLocal_button, 'reseauLocal', text="RESEAU LOCAL", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

#############bouton reseauinternet############################
		self.reseauInternet_button = bgui.ImageButton(self.multijouers_menu, 'reseauInternet', sub_theme='menu',
				size=[0.24, 0.08], pos=[0.4, 0.35])

		self.reseauInternet_label = bgui.Label(self.reseauInternet_button, 'reseauInternet', text="RESEAU INTERNET", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

#############bouton retour############################
		self.retour_button = bgui.ImageButton(self.multijouers_menu, 'retour', sub_theme='menu',
										size=[0.24, 0.08], pos=[0.75, 0.08])

		self.retour_label = bgui.Label(self.retour_button, 'retour', text="RETOUR", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

				# Setup an on_click callback
		self.retour_button.on_click = self.retour

		self.multijouers_menu.visible = False

#--------------menu joueurSolo----------------#
#
#
#
		self.joueurSolo_menu = bgui.Frame(self, 'joueurSolo_menu', sub_theme='solo', size=[1.0, 1.0],
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		self.voiture_label = bgui.Label(self.joueurSolo_menu, 'voiture_label', text="voiture", pt_size=44, pos=[0.45, 0.92],
				options=bgui.BGUI_DEFAULT)

#############bouton flecheG############################
		self.flecheG_button = bgui.ImageButton(self.joueurSolo_menu, 'flecheG', sub_theme='selFlecheG',
			size=[0.05, 0.38], pos=[0.18, 0.48])

		# Setup an on_click callback
		self.flecheG_button.on_click = self.leftcar

#############bouton fleche############################
		self.fleche_button = bgui.ImageButton(self.joueurSolo_menu, 'fleche', sub_theme='selFleche',
			size=[0.05, 0.38], pos=[0.78, 0.48])

		# Setup an on_click callback
		self.fleche_button.on_click = self.rightcar

#############bouton flecheGRoue############################
		self.flecheGRoue_button = bgui.ImageButton(self.joueurSolo_menu, 'flecheGRoue', sub_theme='selFlecheG',
			size=[0.05, 0.22], pos=[0.18, 0.25])

				# Setup an on_click callback
		self.flecheGRoue_button.on_click = self.leftwheels
#############bouton flecheRoue############################
		self.flecheRoue_button = bgui.ImageButton(self.joueurSolo_menu, 'flecheRoue', sub_theme='selFleche',
			size=[0.05, 0.22], pos=[0.78, 0.25])

		# Setup an on_click callback
		self.flecheRoue_button.on_click = self.rightwheels
		
#############bouton retour############################
		self.retour_button = bgui.ImageButton(self.joueurSolo_menu, 'retour', sub_theme='menu',
			size=[0.24, 0.08], pos=[0.75, 0.08])

		self.retour_label = bgui.Label(self.retour_button, 'retour', text="RETOUR", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

				# Setup an on_click callback
		self.retour_button.on_click = self.retour


#############bouton testerVoiture############################
		self.testerVoiture_button = bgui.ImageButton(self.joueurSolo_menu, 'testerVoiture', sub_theme='menu',
										size=[0.24, 0.08], pos=[0.15, 0.08])

		self.testerVoiture_label = bgui.Label(self.testerVoiture_button, 'testerVoiture', text="TESTER", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

				# Setup an on_click callback
		self.testerVoiture_button.on_click = self.testerVoiture

#############bouton validerVoiture############################
		self.validerVoiture_button = bgui.ImageButton(self.joueurSolo_menu, 'validerVoiture', sub_theme='menu',
										size=[0.24, 0.08], pos=[0.45, 0.08])

		self.retour_label = bgui.Label(self.validerVoiture_button, 'validerVoiture', text="VALIDER", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

				# Setup an on_click callback
		self.validerVoiture_button.on_click = self.circuitSolo

		self.joueurSolo_menu.visible = False

#--------------menu circuitSolo----------------#
#
#
#
		self.circuitSolo_menu = bgui.Frame(self, 'circuitSolo_menu', sub_theme='solo', size=[1.0, 1.0],
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		self.circuitSolo_menu.img = bgui.Image(self.circuitSolo_menu, 'image', 'menu.jpg', size=[1.0, 1.0],
			options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX|bgui.BGUI_CACHE)

#############bouton retour############################
		self.retour_button = bgui.ImageButton(self.circuitSolo_menu, 'retour', sub_theme='menu',
				size=[0.24, 0.08], pos=[0.75, 0.08])

		self.retour_label = bgui.Label(self.retour_button, 'retour', text="RETOUR", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

				# Setup an on_click callback
		self.retour_button.on_click = self.retoursolo

#############bouton validercircuitSolo############################
		self.validercircuitSolo_button = bgui.ImageButton(self.circuitSolo_menu, 'circuitSolo', sub_theme='menu',
				size=[0.24, 0.08], pos=[0.45, 0.08])

		self.retour_label = bgui.Label(self.validercircuitSolo_button, 'circuitSolo', text="VALIDER", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

				# Setup an on_click callback
		#self.validercircuitSolo_button.on_click = self.circuitSolo

############///////////selection_circuit video \\\\\\\\\\\\\\#################

		self.circuit_label = bgui.Label(self.circuitSolo_menu, 'circuitSolo_text', text="nom du circuit:"+str(gl.mapName), pt_size=30, pos=[0.15, 0.7],
				options=bgui.BGUI_DEFAULT)

		self.selection_circuit = bgui.Frame(self.circuitSolo_menu, 'selection_circuit', sub_theme='ecran', border=1, size=[0.2, 0.3], pos=[0.15, 0.38],
				options=bgui.BGUI_DEFAULT)

		self.selection_circuitVideo = bgui.Video(self.selection_circuit, 'selection_circuitVideo', 'vidNonTrouver.avi', play_audio=False, repeat=-1, size=[1, 1], pos=[0, 0], options=bgui.BGUI_DEFAULT)

		self.circuitSolo_menu.visible = False


#############bouton flecheVideoDR############################
		self.flecheVdDR_button = bgui.ImageButton(self.circuitSolo_menu, 'flecheVdDR', sub_theme='selFleche',
			size=[0.05, 0.30], pos=[0.35, 0.38])

		# Setup an on_click callback
		self.flecheVdDR_button.on_click = self.rightMap

#############bouton flecheVideoGA############################
		self.flecheVdGA_button = bgui.ImageButton(self.circuitSolo_menu, 'flecheVdGA', sub_theme='selFlecheG',
			size=[0.05, 0.30], pos=[0.1, 0.38])

		# Setup an on_click callback
		self.flecheVdGA_button.on_click = self.leftMap

############///////////selection_circuit nombre de tours \\\\\\\\\\\\\\#################

		self.nbTours_label = bgui.Label(self.circuitSolo_menu, 'circuitSolo_nbTours', text="nombre de tours:", pt_size=30, pos=[0.15, 0.3],
				options=bgui.BGUI_DEFAULT)

		self.fondNbToursSolo = bgui.Frame(self.circuitSolo_menu, 'fondNbToursSolo', sub_theme='fondDigit', border=1, size=[0.05, 0.05], pos=[0.18, 0.22],
				options=bgui.BGUI_DEFAULT)

		self.nbToursSolo_label = bgui.Label(self.fondNbToursSolo, 'nbToursSolo_label', sub_theme='fondDigit', text=str(gl.nbTours), pt_size=30,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

#############bouton flechetoursDR############################
		self.flecheToursDR_button = bgui.ImageButton(self.circuitSolo_menu, 'flecheToursDR', sub_theme='selFleche',
			size=[0.02, 0.05], pos=[0.23, 0.22])

		# Setup an on_click callback
		self.flecheToursDR_button.on_click = self.rightTours

#############bouton flechetoursGA############################
		self.flecheToursGA_button = bgui.ImageButton(self.circuitSolo_menu, 'flecheToursGA', sub_theme='selFlecheG',
			size=[0.02, 0.05], pos=[0.16, 0.22])

		# Setup an on_click callback
		self.flecheToursGA_button.on_click = self.leftTours
############/////////// grillePosJoueurs \\\\\\\\\\\\\\#################

		self.grillePosJoueurs = bgui.Frame(self.circuitSolo_menu, 'grillePosJoueurs', sub_theme='ecran', border=1, size=[0.19, 0.55], pos=[0.6, 0.22],
				options=bgui.BGUI_DEFAULT)

		self.grillePosJoueurs.img = bgui.Image(self.grillePosJoueurs , 'grilleDepart', 'grille de depart.jpg', size=[1.0, 1.0],
			options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX|bgui.BGUI_CACHE)

		self.grillePosJoueurs_label = bgui.Label(self.circuitSolo_menu, 'grillePosJoueurs_label', text="position des joueurs", pt_size=24, pos=[0.6, 0.78],
				options=bgui.BGUI_DEFAULT)

############|||||||position 1||||||||########################
		self.gPosJoueur1 = bgui.Frame(self.grillePosJoueurs, 'gPosJoueur1', sub_theme='ecran', border=3, size=[0.21, 0.16], pos=[0.16, 0.75],
				options=bgui.BGUI_DEFAULT)

		self.gPosJoueur1.img = bgui.Image(self.gPosJoueur1 , 'img1', 'human.png', size=[1.0, 1.0],
			options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX|bgui.BGUI_CACHE)

		# Setup an on_click callback
		#self.gPosJoueur1.on_click = self.leftTours


############|||||||position 2||||||||########################
		self.gPosJoueur2 = bgui.Frame(self.grillePosJoueurs, 'gPosJoueur2', sub_theme='ecran', border=3, size=[0.21, 0.16], pos=[0.64, 0.63],
				options=bgui.BGUI_DEFAULT)

		self.gPosJoueur2.img = bgui.Image(self.gPosJoueur2 , 'img2', 'none.png', size=[1.0, 1.0],
			options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX|bgui.BGUI_CACHE)

		# Setup an on_click callback
		#self.gPosJoueur2.on_click = self.leftTours

############|||||||position 3||||||||########################
		self.gPosJoueur3 = bgui.Frame(self.grillePosJoueurs, 'gPosJoueur3', sub_theme='ecran', border=3, size=[0.21, 0.16], pos=[0.16, 0.49],
				options=bgui.BGUI_DEFAULT)

		self.gPosJoueur3.img = bgui.Image(self.gPosJoueur3 , 'img3', 'none.png', size=[1.0, 1.0],
			options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX|bgui.BGUI_CACHE)

		# Setup an on_click callback
		#self.gPosJoueur3.on_click = self.leftTours

############|||||||position 4||||||||########################
		self.gPosJoueur4 = bgui.Frame(self.grillePosJoueurs, 'gPosJoueur4', sub_theme='ecran', border=3, size=[0.21, 0.16], pos=[0.64, 0.36],
				options=bgui.BGUI_DEFAULT)

		self.gPosJoueur4.img = bgui.Image(self.gPosJoueur4 , 'img4', 'none.png', size=[1.0, 1.0],
			options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX|bgui.BGUI_CACHE)

		# Setup an on_click callback
		#self.gPosJoueur4.on_click = self.leftTours

############|||||||position 5||||||||########################
		self.gPosJoueur5 = bgui.Frame(self.grillePosJoueurs, 'gPosJoueur5', sub_theme='ecran', border=3, size=[0.21, 0.16], pos=[0.16, 0.23],
				options=bgui.BGUI_DEFAULT)

		self.gPosJoueur5.img = bgui.Image(self.gPosJoueur5 , 'img5', 'none.png', size=[1.0, 1.0],
			options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX|bgui.BGUI_CACHE)

		# Setup an on_click callback
		#self.gPosJoueur5.on_click = self.leftTours

############|||||||position 6||||||||########################
		self.gPosJoueur6 = bgui.Frame(self.grillePosJoueurs, 'gPosJoueur6', sub_theme='ecran', border=3, size=[0.21, 0.16], pos=[0.64, 0.09],
				options=bgui.BGUI_DEFAULT)

		self.gPosJoueur6.img = bgui.Image(self.gPosJoueur6 , 'img6', 'none.png', size=[1.0, 1.0],
			options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX|bgui.BGUI_CACHE)

		# Setup an on_click callback
		#self.gPosJoueur5.on_click = self.leftTours
#--------------menu telechargement----------------#
#
#
#
		self.telechargement_menu = bgui.Frame(self, 'telechargement_menu', size=[1.0, 1.0],
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		self.telechargement_menu.img = bgui.Image(self.telechargement_menu, 'image', 'menu.jpg', size=[1.0, 1.0],
			options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX|bgui.BGUI_CACHE)

########--------------avertissementM----------------#
		self.avertissementM = bgui.Frame(self.telechargement_menu, 'avertissement_menu', border=1, size=[0.64, 0.75], pos=[0.02, 0.04],
				options=bgui.BGUI_DEFAULT)

		self.avertissementM_label = bgui.Label(self.avertissementM, 'avertissementM', text="section non operationnelle", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

#############bouton retour############################
		self.retour_button = bgui.ImageButton(self.telechargement_menu, 'retour', sub_theme='menu',
										size=[0.24, 0.08], pos=[0.75, 0.08])

		self.retour_label = bgui.Label(self.retour_button, 'retour', text="RETOUR", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

				# Setup an on_click callback
		self.retour_button.on_click = self.retour

		self.telechargement_menu.visible = False

#--------------menu options----------------#
#
#
#
		self.options_menu = bgui.Frame(self, 'options_menu', border=1, size=[1.0, 1.0],
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		self.options_menu.img = bgui.Image(self.options_menu, 'image', 'menu.jpg', size=[1.0, 1.0],
			options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX|bgui.BGUI_CACHE)


#############bouton affichage############################
		self.affichage_button = bgui.ImageButton(self.options_menu, 'affichage', sub_theme='menu',
				size=[0.24, 0.08], pos=[0.75, 0.70])

		self.affichage_label = bgui.Label(self.affichage_button, 'affichage', text="AFFICHAGE", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		# Setup an on_click callback
		self.affichage_button.on_click = self.affichageM
#############bouton commande############################
		self.commande_button = bgui.ImageButton(self.options_menu, 'commande', sub_theme='menu',
				size=[0.24, 0.08], pos=[0.75, 0.60])

		self.commande_label = bgui.Label(self.commande_button, 'commande', text="CONTROLE", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		# Setup an on_click callback
		self.commande_button.on_click = self.commandeM


#############bouton son############################
		self.son_button = bgui.ImageButton(self.options_menu, 'son', sub_theme='menu',
				size=[0.24, 0.08], pos=[0.75, 0.50])

		self.son_label = bgui.Label(self.son_button, 'son', text="AUDIO", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		# Setup an on_click callback
		self.son_button.on_click = self.sonM

#############bouton joueurs############################
		self.joueurs_button = bgui.ImageButton(self.options_menu, 'joueurs', sub_theme='menu',
				size=[0.24, 0.08], pos=[0.75, 0.40])

		self.joueurs_label = bgui.Label(self.joueurs_button, 'joueurs', text="JOUEURS", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		# Setup an on_click callback
		self.joueurs_button.on_click = self.joueursM


#############bouton retour############################
		self.retour_button = bgui.ImageButton(self.options_menu, 'retour', sub_theme='menu',
				size=[0.24, 0.08], pos=[0.75, 0.08])

		self.retour_label = bgui.Label(self.retour_button, 'retour', text="RETOUR", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

				# Setup an on_click callback
		self.retour_button.on_click = self.retour

		self.options_menu.visible = False


########--------------menu affichage----------------#
		self.affichage_menu = bgui.Frame(self.options_menu, 'affichage_menu', border=1, size=[0.64, 0.75], pos=[0.02, 0.04],
				options=bgui.BGUI_DEFAULT)

		self.affichage_label = bgui.Label(self.affichage_menu, 'affichage', text="AFFICHAGE", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

#############bouton activate mirror############################
		self.mirror_button = bgui.ImageButton(self.affichage_menu, 'mirrorbt', sub_theme='check',
				size=[0.04, 0.04], pos=[0.42, 0.80])

		##mirror label
		self.affichage_label = bgui.Label(self.affichage_menu, 'mirror', text="activation des reflets temp reel", pt_size=24, pos=[0.03, 0.80],
				options=bgui.BGUI_DEFAULT)



########--------------menu commande----------------#
		self.commande_menu = bgui.Frame(self.options_menu, 'commande_menu', border=1, size=[0.64, 0.75], pos=[0.02, 0.04],
				options=bgui.BGUI_DEFAULT)


#############bouton joueurUnCom############################
		self.joueurUnCom_button = bgui.ImageButton(self.commande_menu, 'joueurUn', sub_theme='menu',
				size=[0.22, 0.08], pos=[0.05, 0.90])

		self.affichage_label = bgui.Label(self.joueurUnCom_button, 'joueurUnCom', text="JOUEUR 1", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

#############bouton joueurDeuxCom############################
		self.joueurDeuxCom_button = bgui.ImageButton(self.commande_menu, 'joueurDeux', sub_theme='menu',
				size=[0.22, 0.08], pos=[0.28, 0.90])

		self.affichage_label = bgui.Label(self.joueurDeuxCom_button, 'joueurDeuxCom', text="JOUEUR 2", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

#############bouton joueurTroisCom############################
		self.joueurTroisCom_button = bgui.ImageButton(self.commande_menu, 'joueurTrois', sub_theme='menu',
				size=[0.22, 0.08], pos=[0.51, 0.90])

		self.affichage_label = bgui.Label(self.joueurTroisCom_button, 'joueurTroisCom', text="JOUEUR 3", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

#############bouton joueurQuatreCom############################
		self.joueurQuatreCom_button = bgui.ImageButton(self.commande_menu, 'joueurQuatre', sub_theme='menu',
				size=[0.22, 0.08], pos=[0.74, 0.90])

		self.affichage_label = bgui.Label(self.joueurQuatreCom_button, 'joueurQuatreCom', text="JOUEUR 4", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)



############///////////frame commande joueur 1 \\\\\\\\\\\\\\#################

		self.joueurUnCom_ecran = bgui.Frame(self.commande_menu, 'joueurUnCom_ecran', sub_theme='ecran', border=1, size=[0.64, 0.75], pos=[0.02, 0.02],
				options=bgui.BGUI_DEFAULT)

#############bouton speedUpUn############################
		self.speedUpUn_button = bgui.ImageButton(self.joueurUnCom_ecran, 'speedUpUn', sub_theme='touche',
				size=[0.1, 0.1], pos=[0.5, 0.75])

		self.speedUpUn_label = bgui.Label(self.speedUpUn_button, 'speedUpUn', text= ev.EventToString(int(gl.conf[0][0][2][6][1])), pt_size=14,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		#image boite de vitesse
		self.joueurUnCom_ecran.img = bgui.Image(self.joueurUnCom_ecran, 'boitevt', 'boite de vitesse.png', size=[0.1, 0.15], pos=[0.5, 0.52],
			options = bgui.BGUI_DEFAULT|bgui.BGUI_CACHE)

#############bouton speedDownUn############################
		self.speedDownUn_button = bgui.ImageButton(self.joueurUnCom_ecran, 'speedDownUn', sub_theme='touche',
				size=[0.1, 0.1], pos=[0.5, 0.35])

		self.speedDownUn_label = bgui.Label(self.speedDownUn_button, 'speedDownUn', text= ev.EventToString(int(gl.conf[0][0][2][7][1])), pt_size=14,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		#image voiture
		self.joueurUnCom_ecran.imgDeux = bgui.Image(self.joueurUnCom_ecran, 'voiture', 'voitureup.png', size=[0.1, 0.35], pos=[0.18, 0.44],
			options = bgui.BGUI_DEFAULT|bgui.BGUI_CACHE)

#############bouton sauvegardeComUn############################
		self.sauvegardeComUn_button = bgui.ImageButton(self.joueurUnCom_ecran, 'sauvegardeComUn', sub_theme='menu',
				size=[0.32, 0.08], pos=[0.65, 0.04])

		self.sauvegardeComUn_label = bgui.Label(self.sauvegardeComUn_button, 'sauvegardeComUn', text="SAUVERGARDER", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
		self.sauvegardeComUn_button.on_click = self.sauvegardeComUn




		self.commande_menu.visible = False





########--------------menu son----------------#
		self.son_menu = bgui.Frame(self.options_menu, 'son_menu', border=1, size=[0.64, 0.75], pos=[0.02, 0.04],
				options=bgui.BGUI_DEFAULT)

		self.flecheH_button = bgui.ImageButton(self.son_menu, 'volumeH', sub_theme='flecheH',
				size=[0.10, 0.08], pos=[0.65, 0.48])

		# Setup an on_click callback
		self.flecheH_button.on_active = self.volumeMup

		self.volumeG_fond = bgui.Frame(self.son_menu, 'affichage_menu', sub_theme='fondDigit', size=[0.10, 0.12], pos=[0.65, 0.36])
		self.volumeG_label = bgui.Label(self.volumeG_fond, 'volumeM', text=str(gl.musiqueVolume), sub_theme='Digital', pt_size=53,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		self.flecheB_button = bgui.ImageButton(self.son_menu, 'volumeB', sub_theme='flecheB',
				size=[0.10, 0.08], pos=[0.65, 0.28])

		# Setup an on_click callback
		self.flecheB_button.on_active = self.volumeMdown

		self.son_menu.visible = False


########--------------menu options_joueurs----------------#
		self.options_joueurs = bgui.Frame(self.options_menu, 'options_joueurs', border=1, size=[0.64, 0.75], pos=[0.02, 0.04],
				options=bgui.BGUI_DEFAULT)

#############input joueur 1############################
		self.joueur1_label = bgui.Label(self.options_joueurs, 'joueur1', text="le premier joueur s\'appelle:", pt_size=30, pos=[0.02, 0.8],
				options=bgui.BGUI_DEFAULT)

		self.joueur1_input = bgui.TextInput(self.options_joueurs, 'joueur1_input', str(gl.conf[0][0][0]), pt_size=30, size=[.2, .05], pos=[0.02, 0.73],
			input_options = bgui.BGUI_INPUT_NONE, options = bgui.BGUI_DEFAULT)
		self.joueur1_input.activate()
		self.joueur1_input.on_enter_key = self.joueur1_on_input_enter

#############input joueur 2############################
		self.joueur2_label = bgui.Label(self.options_joueurs, 'joueur2', text="le second joueur s\'appelle:", pt_size=30, pos=[0.02, 0.6],
				options=bgui.BGUI_DEFAULT)

		self.joueur2_input = bgui.TextInput(self.options_joueurs, 'joueur2_input', str(gl.conf[0][1][0]), pt_size=30, size=[.2, .05], pos=[0.02, 0.53],
			input_options = bgui.BGUI_INPUT_NONE, options = bgui.BGUI_DEFAULT)
		self.joueur2_input.activate()
		self.joueur2_input.on_enter_key = self.joueur2_on_input_enter

#############input joueur 3############################
		self.joueur3_label = bgui.Label(self.options_joueurs, 'joueur3', text="le troisieme joueur s\'appelle:", pt_size=30, pos=[0.02, 0.4],
				options=bgui.BGUI_DEFAULT)

		self.joueur3_input = bgui.TextInput(self.options_joueurs, 'joueur3_input', str(gl.conf[0][2][0]), pt_size=30, size=[.2, .05], pos=[0.02, 0.33],
			input_options = bgui.BGUI_INPUT_NONE, options = bgui.BGUI_DEFAULT)
		self.joueur3_input.activate()
		self.joueur3_input.on_enter_key = self.joueur3_on_input_enter

#############input joueur 4############################
		self.joueur4_label = bgui.Label(self.options_joueurs, 'joueur4', text="le quatrieme joueur s\'appelle:", pt_size=30, pos=[0.02, 0.2],
				options=bgui.BGUI_DEFAULT)

		self.joueur4_input = bgui.TextInput(self.options_joueurs, 'joueur4_input', str(gl.conf[0][3][0]), pt_size=30, size=[.2, .05], pos=[0.02, 0.13],
			input_options = bgui.BGUI_INPUT_NONE, options = bgui.BGUI_DEFAULT)
		self.joueur4_input.activate()
		self.joueur4_input.on_enter_key = self.joueur4_on_input_enter


		self.options_joueurs.visible = False



#--------------menu ecransplitter----------------#
#
#
#
		self.ecransplitter_menu = bgui.Frame(self, 'ecransplitter_menu', size=[1.0, 1.0],
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		self.ecransplitter_menu.img = bgui.Image(self.ecransplitter_menu, 'image', 'menu.jpg', size=[1.0, 1.0],
			options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX|bgui.BGUI_CACHE)

#############bouton deuxjoueurs############################
		self.deuxjoueurs_button = bgui.ImageButton(self.ecransplitter_menu, 'deuxjoueurs', sub_theme='menu',
				size=[0.14, 0.08], pos=[0.20, 0.70])

		self.deuxjoueurs_label = bgui.Label(self.deuxjoueurs_button, 'deuxjoueurs', text="2 JOUEURS", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		# Setup an on_click callback
		self.deuxjoueurs_button.on_click = self.deuxjoueursM

#############bouton troisjoueurs############################
		self.troisjoueurs_button = bgui.ImageButton(self.ecransplitter_menu, 'troisjoueurs', sub_theme='menu',
				size=[0.14, 0.08], pos=[0.35, 0.70])

		self.troisjoueurs_label = bgui.Label(self.troisjoueurs_button, 'troisjoueurs', text="3 JOUEURS", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		# Setup an on_click callback
		self.troisjoueurs_button.on_click = self.troisjoueursM

#############bouton quatrejoueurs############################
		self.quatrejoueurs_button = bgui.ImageButton(self.ecransplitter_menu, 'quatrejoueurs', sub_theme='menu',
				size=[0.14, 0.08], pos=[0.50, 0.70])

		self.quatrejoueurs_label = bgui.Label(self.quatrejoueurs_button, 'quatrejoueurs', text="4 JOUEURS", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		# Setup an on_click callback
		self.quatrejoueurs_button.on_click = self.quatrejoueursM

#############bouton retour############################
		self.retour_button = bgui.ImageButton(self.ecransplitter_menu, 'retour', sub_theme='menu',
			size=[0.24, 0.08], pos=[0.75, 0.08])

		self.retour_label = bgui.Label(self.retour_button, 'retour', text="RETOUR", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

				# Setup an on_click callback
		self.retour_button.on_click = self.retourMulti

		self.ecransplitter_menu.visible = False



########--------------menu deuxjoueurs----------------#
		self.deuxjoueurs_menu = bgui.Frame(self.ecransplitter_menu, 'deuxjoueurs_menu', border=1, size=[0.64, 0.75], pos=[0.02, 0.04],
				options=bgui.BGUI_DEFAULT)

#############bouton disposition############################
		self.disposition_button = bgui.ImageButton(self.deuxjoueurs_menu, 'disposition', sub_theme='menu',
				size=[0.22, 0.08], pos=[0.75, 0.60])

		# Setup an on_click callback
		self.disposition_button.on_click = self.ecranDeuxJM

		self.disposition_label = bgui.Label(self.disposition_button, 'disposition', text="DISPOSITION", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

#############bouton placementJoueur############################
		self.placementJoueur_button = bgui.ImageButton(self.deuxjoueurs_menu, 'placementJoueur', sub_theme='menu',
				size=[0.22, 0.08], pos=[0.75, 0.50])

		# Setup an on_click callback
		self.placementJoueur_button.on_click = self.placementJoueurDeux
		
		self.placementJoueur_label = bgui.Label(self.placementJoueur_button, 'placementJoueur', text="PLACE J", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

#############bouton valider############################
		self.validerplacementJoueur_button = bgui.ImageButton(self.deuxjoueurs_menu, 'validerplacementJoueur', sub_theme='menu',
				size=[0.22, 0.08], pos=[0.75, 0.40])

		# Setup an on_click callback
		self.validerplacementJoueur_button.on_click = self.validerDeuxJPos
		
		self.validerplacementJoueur_label = bgui.Label(self.validerplacementJoueur_button, 'validerplacementJoueur', text="VALIDER", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

############///////////frame ecran 2 joueurs\\\\\\\\\\\\\\#################

		self.deuxjoueurs_ecran = bgui.Frame(self.deuxjoueurs_menu, 'deuxjoueurs_ecran', sub_theme='ecran', border=1, size=[0.70, 0.75], pos=[0.02, 0.08],
				options=bgui.BGUI_DEFAULT)

		#Horizontal
		self.deuxjoueurs_ecranHorizontal = bgui.Frame(self.deuxjoueurs_ecran, 'deuxjoueursUn_ecran', sub_theme='ecran', border=1, size=[1.0, 1.0], pos=[0.0, 0.0],
				options=bgui.BGUI_DEFAULT)



		self.deuxjoueurs_ecranHorizontal.img = bgui.Image(self.deuxjoueurs_ecranHorizontal, 'image1', 'ecranJoueur.png', size=[1.0, 0.5], pos=[0.0, 0.0],
				options=bgui.BGUI_DEFAULT)

		self.deuxjoueurs_ecranHorizontal.img2 = bgui.Image(self.deuxjoueurs_ecranHorizontal, 'image2', 'ecranJoueur.png', size=[1.0, 0.5], pos=[0.0, 0.5],
				options=bgui.BGUI_DEFAULT)			

		self.posJoueurHH_label = bgui.Label(self.deuxjoueurs_ecranHorizontal, 'posJoueurHH', text="JOUEUR 1", pt_size=24, pos=[0.5, 0.9],
				options=bgui.BGUI_DEFAULT)

		self.posJoueurHB_label = bgui.Label(self.deuxjoueurs_ecranHorizontal, 'posJoueurHB', text="JOUEUR 2", pt_size=24, pos=[0.5, 0.4],
				options=bgui.BGUI_DEFAULT)


		#Vertical
		self.deuxjoueurs_ecranVertical = bgui.Frame(self.deuxjoueurs_ecran, 'deuxjoueursDeux_ecran', sub_theme='ecran', border=1, size=[1.0, 1.0], pos=[0.0, 0.0],
				options=bgui.BGUI_DEFAULT)

		self.deuxjoueurs_ecranVertical.img = bgui.Image(self.deuxjoueurs_ecranVertical, 'image1', 'ecranJoueur.png', size=[0.5, 1.0], pos=[0.0, 0.0],
				options=bgui.BGUI_DEFAULT)

		self.deuxjoueurs_ecranVertical.img2 = bgui.Image(self.deuxjoueurs_ecranVertical, 'image2', 'ecranJoueur.png', size=[0.5, 1.0], pos=[0.5, 0.0],
				options=bgui.BGUI_DEFAULT)

		self.posJoueurVH_label = bgui.Label(self.deuxjoueurs_ecranVertical, 'posJoueurVH', text="JOUEUR 1", pt_size=24, pos=[0.25, 0.9],
				options=bgui.BGUI_DEFAULT)

		self.posJoueurVB_label = bgui.Label(self.deuxjoueurs_ecranVertical, 'posJoueurVB', text="JOUEUR 2", pt_size=24, pos=[0.75, 0.9],
				options=bgui.BGUI_DEFAULT)
				
		self.deuxjoueurs_ecranVertical.visible = False

########--------------menu troisjoueurs----------------#
		self.troisjoueurs_menu = bgui.Frame(self.ecransplitter_menu, 'troisjoueurs_menu', border=1, size=[0.64, 0.75], pos=[0.02, 0.04],
				options=bgui.BGUI_DEFAULT)

#############bouton dispositiontrois############################
		self.dispositiontrois_button = bgui.ImageButton(self.troisjoueurs_menu, 'disposition', sub_theme='menu',
				size=[0.22, 0.08], pos=[0.75, 0.60])

		# Setup an on_click callback
		#self.dispositiontrois_button.on_click = self.ecrantroisJM

		self.disposition_label = bgui.Label(self.dispositiontrois_button, 'disposition', text="DISPOSITION", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

#############bouton placementJoueurtrois############################
		self.placementJoueurtrois_button = bgui.ImageButton(self.troisjoueurs_menu, 'placementJoueur', sub_theme='menu',
				size=[0.22, 0.08], pos=[0.75, 0.50])

		# Setup an on_click callback
		#self.placementJoueur_button.on_click = self.placementJoueurDeux
		
		self.placementJoueurtrois_label = bgui.Label(self.placementJoueurtrois_button, 'placementJoueur', text="PLACE J", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		self.troisjoueurs_menu.visible = False

########--------------menu quatrejoueurs----------------#
		self.quatrejoueurs_menu = bgui.Frame(self.ecransplitter_menu, 'quatrejoueurs_menu', border=1, size=[0.64, 0.75], pos=[0.02, 0.04],
				options=bgui.BGUI_DEFAULT)


#############bouton placementJoueurquatre############################
		self.placementJoueurQuatre_button = bgui.ImageButton(self.quatrejoueurs_menu, 'placementJoueur', sub_theme='menu',
				size=[0.22, 0.08], pos=[0.75, 0.50])

		# Setup an on_click callback
		#self.placementJoueurQuatre_button.on_click = self.placementJoueurQuatre
		
		self.placementJoueurquatre_label = bgui.Label(self.placementJoueurQuatre_button, 'placementJoueur', text="PLACE J", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

#############bouton valider############################
		self.validerplacementquatreJoueur_button = bgui.ImageButton(self.quatrejoueurs_menu, 'validerplacementquatreJoueur', sub_theme='menu',
				size=[0.22, 0.08], pos=[0.75, 0.40])

		# Setup an on_click callback
		self.validerplacementquatreJoueur_button.on_click = self.validerQuatreJPos
		
		self.validerplacementquatreJoueur_label = bgui.Label(self.validerplacementquatreJoueur_button, 'validerplacementquatreJoueur', text="VALIDER", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

############///////////frame ecran 4 joueurs\\\\\\\\\\\\\\#################

		self.quatrejoueurs_ecran = bgui.Frame(self.quatrejoueurs_menu, 'quatrejoueurs_ecran', sub_theme='ecran', border=1, size=[0.70, 0.75], pos=[0.02, 0.08],
				options=bgui.BGUI_DEFAULT)

		self.quatrejoueurs_ecran.img1 = bgui.Image(self.quatrejoueurs_ecran, 'image1', 'ecranJoueur.png', size=[0.5, 0.5], pos=[0.0, 0.5],
				options=bgui.BGUI_DEFAULT)

		self.posJoueurHG_label = bgui.Label(self.quatrejoueurs_ecran, 'posJoueurHG', text="JOUEUR 1", pt_size=24, pos=[0.25, 0.9],
				options=bgui.BGUI_DEFAULT)

		self.quatrejoueurs_ecran.img2 = bgui.Image(self.quatrejoueurs_ecran, 'image2', 'ecranJoueur.png', size=[0.5, 0.5], pos=[0.5, 0.5],
				options=bgui.BGUI_DEFAULT)

		self.posJoueurHD_label = bgui.Label(self.quatrejoueurs_ecran, 'posJoueurHD', text="JOUEUR 2", pt_size=24, pos=[0.75, 0.9],
				options=bgui.BGUI_DEFAULT)

		self.quatrejoueurs_ecran.img3 = bgui.Image(self.quatrejoueurs_ecran, 'image3', 'ecranJoueur.png', size=[0.5, 0.5], pos=[0.0, 0.0],
				options=bgui.BGUI_DEFAULT)

		self.posJoueurBG_label = bgui.Label(self.quatrejoueurs_ecran, 'posJoueurBG', text="JOUEUR 3", pt_size=24, pos=[0.25, 0.4],
				options=bgui.BGUI_DEFAULT)

		self.quatrejoueurs_ecran.img4 = bgui.Image(self.quatrejoueurs_ecran, 'image4', 'ecranJoueur.png', size=[0.5, 0.5], pos=[0.5, 0.0],
				options=bgui.BGUI_DEFAULT)

		self.posJoueurBD_label = bgui.Label(self.quatrejoueurs_ecran, 'posJoueurBD', text="JOUEUR 4", pt_size=24, pos=[0.75, 0.4],
				options=bgui.BGUI_DEFAULT)

		self.quatrejoueurs_menu.visible = False

#--------------menu selectionVoitureDeuxJ----------------#
#
#
#
		self.selectionVoitureDeuxJ_menu = bgui.Frame(self, 'selectionVoitureDeuxJ_menu', border=1, size=[1.0, 1.0],
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

#############bouton retourSelVoitureDeuxJ############################
		self.retourSelVoitureDeuxJ_button = bgui.ImageButton(self.selectionVoitureDeuxJ_menu, 'retourSelVoitureDeuxJ', sub_theme='menu',
				size=[0.24, 0.08], pos=[0.75, 0.08])

		self.retourSelVoitureDeuxJ_label = bgui.Label(self.retourSelVoitureDeuxJ_button, 'retour', text="RETOUR", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
		# Setup an on_click callback
		self.retourSelVoitureDeuxJ_button.on_click = self.retourSelVoitureDeuxJ

		self.selectionVoitureDeuxJ_menu.visible = False

#--------------menu selectionVoitureQuatreJ----------------#
#
#
#
		self.selectionVoitureQuatreJ_menu = bgui.Frame(self, 'selectionVoitureQuatreJ_menu', border=1, size=[1.5, 1.0],
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

#############bouton retourSelVoitureQuatreJ############################
		self.retourSelVoitureQuatreJ_button = bgui.ImageButton(self.selectionVoitureQuatreJ_menu, 'retourSelVoitureQuatreJ', sub_theme='menu',
				size=[0.24, 0.08], pos=[0.75, 0.08])

		self.retourSelVoitureQuatreJ_label = bgui.Label(self.retourSelVoitureQuatreJ_button, 'retour', text="RETOUR", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
		# Setup an on_click callback
		self.retourSelVoitureQuatreJ_button.on_click = self.retourSelVoitureQuatreJ

		self.selectionVoitureQuatreJ_menu.visible = False


		# Create a keymap for keyboard input
		self.keymap = {getattr(bge.events, val): getattr(bgui, val) for val in dir(bge.events) if val.endswith('KEY') or val.startswith('PAD')}


		# Now setup the scene callback so we can draw
		bge.logic.getCurrentScene().post_draw.append(self.render)

	def main(self):
		"""A high-level method to be run every frame"""

		#self.update()

		# Handle the mouse
		mouse = bge.logic.mouse

		pos = list(mouse.position)
		pos[0] *= bge.render.getWindowWidth()
		pos[1] = bge.render.getWindowHeight() - (bge.render.getWindowHeight() * pos[1])

		mouse_state = bgui.BGUI_MOUSE_NONE
		mouse_events = mouse.events

		if mouse_events[bge.events.LEFTMOUSE] == bge.logic.KX_INPUT_JUST_ACTIVATED:
			mouse_state = bgui.BGUI_MOUSE_CLICK
		elif mouse_events[bge.events.LEFTMOUSE] == bge.logic.KX_INPUT_JUST_RELEASED:
			mouse_state = bgui.BGUI_MOUSE_RELEASE
		elif mouse_events[bge.events.LEFTMOUSE] == bge.logic.KX_INPUT_ACTIVE:
			mouse_state = bgui.BGUI_MOUSE_ACTIVE

		self.update_mouse(pos, mouse_state)

		# Handle the keyboard
		keyboard = bge.logic.keyboard

		key_events = keyboard.events
		is_shifted = key_events[bge.events.LEFTSHIFTKEY] == bge.logic.KX_INPUT_ACTIVE or \
					key_events[bge.events.RIGHTSHIFTKEY] == bge.logic.KX_INPUT_ACTIVE

		for key, state in keyboard.events.items():
			if state == bge.logic.KX_INPUT_JUST_ACTIVATED:
				self.update_keyboard(self.keymap[key], is_shifted)

		# Now setup the scene callback so we can draw
		bge.logic.getCurrentScene().pre_draw = [self.render]




def main(cont):
	own = cont.owner
	mouse = bge.logic.mouse

	if not hasattr(gl , 'musiqueVolume'):
		gl.musiqueVolume = 50
		confParser.loadPlayer()
		#print(gl.conf[0][0][2][6][1])
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
		print(gl.lstRoue)
		print(gl.dispPlayers)
		print(gl.lstVoiture)
		print(gl.listMaps)
		print(gl.mapName)

	if 'sys' not in own:
		# Create our system and show the mouse
		own['sys'] = MySys()
		mouse.visible = True
	else:
		own['sys'].main()
