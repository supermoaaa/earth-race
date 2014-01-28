import bgui
import aud
from bge import render as rd
from bge import events as ev
from bge import logic as gl
import confParser
import collections as coll
import logs
from vehicleLinker import vehicleLinker

class BaseGui(bgui.System):
	"""
	Classe de base pour le gui (pour conserver la meme methode main)
	"""
	def __init__(self, ch):
		bgui.System.__init__(self, ch)

		self.dialogue = None
		self.ouvert = True


	def main(self):
		"""A high-level method to be run every frame"""

		#self.update()


		# Handle the mouse
		mouse = gl.mouse

		pos = list(mouse.position)
		pos[0] *= rd.getWindowWidth()
		pos[1] = rd.getWindowHeight() - (rd.getWindowHeight() * pos[1])

		mouse_state = bgui.BGUI_MOUSE_NONE
		mouse_events = mouse.events

		if mouse_events[ev.LEFTMOUSE] == gl.KX_INPUT_JUST_ACTIVATED:
			mouse_state = bgui.BGUI_MOUSE_CLICK
			handle_buffered = gl.device.play(gl.factory_buffered)
		elif mouse_events[ev.LEFTMOUSE] == gl.KX_INPUT_JUST_RELEASED:
			mouse_state = bgui.BGUI_MOUSE_RELEASE
		elif mouse_events[ev.LEFTMOUSE] == gl.KX_INPUT_ACTIVE:
			mouse_state = bgui.BGUI_MOUSE_ACTIVE

		self.update_mouse(pos, mouse_state)

		# Handle the keyboard
		keyboard = gl.keyboard

		key_events = keyboard.events
		is_shifted = key_events[ev.LEFTSHIFTKEY] == gl.KX_INPUT_ACTIVE or \
					key_events[ev.RIGHTSHIFTKEY] == gl.KX_INPUT_ACTIVE

		for key, state in keyboard.events.items():
			if state == gl.KX_INPUT_JUST_ACTIVATED:
				self.update_keyboard(self.keymap[key], is_shifted)

		# Now setup the scene callback so we can draw
		gl.getCurrentScene().post_draw = [self.render]

class FondGui(BaseGui):
	"""
	Fond des pages du menu
	"""
	def __init__(self):
		# Initiate the system
		BaseGui.__init__(self, gl.skin)

		# Fenetre principale
		self.mainframe = bgui.Frame(self, 'window', border=0, size=[1, 1], pos=[0, 0])

		# Fond
		self.frame = bgui.Frame(self.mainframe, 'fond', size=[1, 1], pos=[0, 0], options =  bgui.BGUI_CENTERED | bgui.BGUI_DEFAULT)
		self.frame.img = bgui.Image(self.frame, 'menuItems/menu.jpg', size=[1.0, 1.0],
			options = bgui.BGUI_DEFAULT|bgui.BGUI_CACHE)


#############bouton quitter/retour############################
		if gl.status == "MenuEcranSpliter" :
			self.retour_button = bgui.ImageButton(self.frame, 'quitter', sub_theme='menu', size=[0.10, 0.05], pos=[0.45, 0.44])
			self.retour_label = bgui.Label(self.retour_button, 'retour', text="RETOUR", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		else:
			self.retour_button = bgui.ImageButton(self.frame, 'quitter', sub_theme='menu', size=[0.24, 0.08], pos=[0.75, 0.08])
			self.retour_label = bgui.Label(self.retour_button, 'retour', text="RETOUR", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		# Setup an on_click callback
		self.retour_button.on_click = self.retour_clic


		# Autres attributs
		self.action = None

		# Keymap pour la correspondance entre bge.events et bgui
		self.keymap = {getattr(ev, val): getattr(bgui, val) for val in dir(ev) if (val.endswith('KEY') or val.startswith('PAD')) and hasattr(bgui, val)}


	def retour_clic(self, widget) :
		"""Methode appelée lors du clic sur le bouton Retour"""
		self.action = "retour"
		self.ouvert = False

	def detruire(self) :
		"""Détruit les widgets"""
		self.frame.parent._remove_widget(self.frame)

	def reinit(self) :
		"""Remet les repères d'ouverture et d'action à leur valeur par défaut"""
		self.ouvert = True
		self.action = None

	def main(self) :
		"""Refresh des events et de l'affichage"""
		BaseGui.main(self)

class MenuOptionsGui(BaseGui):
	"""
	Gui pour le menu des options
	"""
	def __init__(self, parent):
		# Initiate the system
		BaseGui.__init__(self, gl.skin)

		# Cadre général
		self.frame = bgui.Frame(parent, 'frame', size=[1, 1], pos=[0, 0],
			sub_theme="Invisible", options =  bgui.BGUI_CENTERED | bgui.BGUI_DEFAULT)

#############bouton affichage############################
		self.affichage_button = bgui.ImageButton(self.frame, 'affichage', sub_theme='menu', size=[0.24, 0.08], pos=[0.45, 0.60])
		self.affichage_label = bgui.Label(self.affichage_button, 'affichage', text="AFFICHAGE", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		# Setup an on_click callback
		self.affichage_button.on_click = self.affichageM
#############bouton commande############################
		self.commande_button = bgui.ImageButton(self.frame, 'commande', sub_theme='menu', size=[0.24, 0.08], pos=[0.45, 0.50])
		self.commande_label = bgui.Label(self.commande_button, 'commande', text="CONTROLE", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		# Setup an on_click callback
		self.commande_button.on_click = self.commandeM


#############bouton son############################
		self.son_button = bgui.ImageButton(self.frame, 'son', sub_theme='menu', size=[0.24, 0.08], pos=[0.45, 0.40])
		self.son_label = bgui.Label(self.son_button, 'son', text="AUDIO", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		# Setup an on_click callback
		self.son_button.on_click = self.sonM

#############bouton joueurs############################
		self.joueurs_button = bgui.ImageButton(self.frame, 'joueurs', sub_theme='menu', size=[0.24, 0.08], pos=[0.45, 0.30])
		self.joueurs_label = bgui.Label(self.joueurs_button, 'joueurs', text="JOUEURS", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		# Setup an on_click callback
		self.joueurs_button.on_click = self.joueursM


		# Autres attributs
		self.action = None



	def detruire(self) :
		"""Détruit les widgets"""
		self.frame.parent._remove_widget(self.frame)

	def affichageM(self, widget) :
		self.detruire()
		self.action = "Affichage"
		self.ouvert = False

	def joueursM(self, widget) :
		self.detruire()
		self.action = "joueurs"
		self.ouvert = False

	def sonM(self, widget) :
		self.detruire()
		self.action = "son"
		self.ouvert = False

	def commandeM(self, widget) :
		self.detruire()
		self.action = "commandes"
		self.ouvert = False

	def main(self) :
		"""Refresh des events et de l'affichage"""
		BaseGui.main(self)

class MenuSelectionCircuitGui(BaseGui):
	"""
	Gui pour la selection dy circuit
	"""
	def __init__(self, parent):
		# Initiate the system
		BaseGui.__init__(self, gl.skin)

		# Fond
		self.frame = bgui.Frame(parent, 'fond', size=[1, 1], pos=[0, 0],
			sub_theme="Invisible", options =  bgui.BGUI_CENTERED | bgui.BGUI_DEFAULT)

#############bouton validercircuit############################
		self.validercircuit_button = bgui.ImageButton(self.frame, 'circuitD', sub_theme='menu', size=[0.24, 0.08], pos=[0.45, 0.08])
		self.retour_label = bgui.Label(self.validercircuit_button, 'circuitD', text="VALIDER", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

				# Setup an on_click callback
		self.validercircuit_button.on_click = self.departSolo

#############bouton ajouter ia############################
		self.ajouterIA_button = bgui.ImageButton(self.frame, 'ajouterIA', sub_theme='menu', size=[0.12, 0.06], pos=[0.82, 0.68])
		self.ajouterIA_label = bgui.Label(self.ajouterIA_button, 'ajouterIA', text="ajouter IA", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

				# Setup an on_click callback
		#self.ajouterIA_button.on_click = self.departSolo

#############bouton enlever ia############################
		self.enleverIA_button = bgui.ImageButton(self.frame, 'enleverIA', sub_theme='menu', size=[0.12, 0.06], pos=[0.82, 0.6])
		self.enleverIA_label = bgui.Label(self.enleverIA_button, 'enleverIA', text="enlever IA", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

				# Setup an on_click callback
		#self.enleverIA_button.on_click = self.departSolo

############///////////selection_circuit video \\\\\\\\\\\\\\#################

		self.circuit_label = bgui.Label(self.frame, 'circuit_text', text="nom du circuit:"+str(gl.mapName), pt_size=30, pos=[0.15, 0.8], options=bgui.BGUI_DEFAULT)
		self.selection_circuit = bgui.Frame(self.frame, 'selection_circuit', sub_theme='ecran', border=1, size=[0.2, 0.3], pos=[0.15, 0.48], options=bgui.BGUI_DEFAULT)
		self.selection_circuitVideo = bgui.Video(self.selection_circuit, 'menuItems/vidNonTrouver.avi', play_audio=False, repeat=-1, size=[1, 1], pos=[0, 0], options=bgui.BGUI_DEFAULT)



#############bouton flecheVideoDR############################
		self.flecheVdDR_button = bgui.ImageButton(self.frame, 'flecheVdDR', sub_theme='selFleche', size=[0.05, 0.30], pos=[0.35, 0.48])

		# Setup an on_click callback
		self.flecheVdDR_button.on_click = self.rightMap

#############bouton flecheVideoGA############################
		self.flecheVdGA_button = bgui.ImageButton(self.frame, 'flecheVdGA', sub_theme='selFlecheG', size=[0.05, 0.30], pos=[0.1, 0.48])

		# Setup an on_click callback
		self.flecheVdGA_button.on_click = self.leftMap

############///////////selection_circuit nombre de tours \\\\\\\\\\\\\\#################

		self.nbToursText_label = bgui.Label(self.frame, 'circuit_nbTours', text="nombre de tours:", pt_size=30, pos=[0.11, 0.38], options=bgui.BGUI_DEFAULT)
		self.fondNbTours = bgui.Frame(self.frame, 'fondNbTours', sub_theme='fondDigit', border=1, size=[0.05, 0.05], pos=[0.14, 0.32], options=bgui.BGUI_DEFAULT)
		self.nbTours_label = bgui.Label(self.fondNbTours, 'nbTours_label', sub_theme='fondDigit', text=str(gl.nbLaps), pt_size=30, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

#############bouton flechetoursDR############################
		self.flecheToursDR_button = bgui.ImageButton(self.frame, 'flecheToursDR', sub_theme='selFleche',
			size=[0.02, 0.05], pos=[0.19, 0.32])

		# Setup an on_click callback
		self.flecheToursDR_button.on_click = self.rightTours

#############bouton flechetoursGA############################
		self.flecheToursGA_button = bgui.ImageButton(self.frame, 'flecheToursGA', sub_theme='selFlecheG',
			size=[0.02, 0.05], pos=[0.12, 0.32])

		# Setup an on_click callback
		self.flecheToursGA_button.on_click = self.leftTours

############///////////climat \\\\\\\\\\\\\\#################

		self.climatText_label = bgui.Label(self.frame, 'climatTextL', text="climat:", pt_size=30, pos=[0.11, 0.26], options=bgui.BGUI_DEFAULT)
		self.climatText = bgui.Frame(self.frame, 'climatText', sub_theme='Invisible', border=1, size=[0.06, 0.07], pos=[0.13, 0.18], options=bgui.BGUI_DEFAULT)
		self.climatText.img = bgui.Image(self.climatText , 'menuItems/' + gl.generalConf[4] + '.png', size=[1.0, 1.0], options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX|bgui.BGUI_CACHE)

#############bouton flecheClimatDR############################
		self.flecheClimatDR_button = bgui.ImageButton(self.frame, 'flecheClimatDR', sub_theme='selFleche',
			size=[0.02, 0.07], pos=[0.19, 0.18])

		# Setup an on_click callback
		self.flecheClimatDR_button.on_click = self.rightClimat

#############bouton flechetoursGA############################
		self.flecheClimatGA_button = bgui.ImageButton(self.frame, 'flecheClimatGA', sub_theme='selFlecheG',
			size=[0.02, 0.07], pos=[0.11, 0.18])

		# Setup an on_click callback
		self.flecheClimatGA_button.on_click = self.leftClimat

############/////////// grillePosJoueurs \\\\\\\\\\\\\\#################

		self.grillePosJoueurs = bgui.Frame(self.frame, 'grillePosJoueurs', sub_theme='ecran', border=1, size=[0.19, 0.55], pos=[0.6, 0.22], options=bgui.BGUI_DEFAULT)
		self.grillePosJoueurs.img = bgui.Image(self.grillePosJoueurs , 'menuItems/grille de depart.jpg', size=[1.0, 1.0], options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX|bgui.BGUI_CACHE)
		self.grillePosJoueurs_label = bgui.Label(self.frame, 'grillePosJoueurs_label', text="position des joueurs", pt_size=24, pos=[0.6, 0.78], options=bgui.BGUI_DEFAULT)

############|||||||position 1||||||||########################
		self.gPosJoueur1 = bgui.Frame(self.grillePosJoueurs, 'gPosJoueur1', sub_theme='ecran', border=3, size=[0.21, 0.16], pos=[0.16, 0.75], options=bgui.BGUI_DEFAULT)
		self.gPosJoueur1.img = bgui.Image(self.gPosJoueur1 , 'menuItems/departjoueurs.png', size=[1.0, 1.0], texco=[(0.5, 0.5), (1, 0.5), (1, 1), (0.5, 1)], options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX|bgui.BGUI_CACHE)



############|||||||position 2||||||||########################
		self.gPosJoueur2 = bgui.Frame(self.grillePosJoueurs, 'gPosJoueur2', sub_theme='ecran', border=3, size=[0.21, 0.16], pos=[0.64, 0.63], options=bgui.BGUI_DEFAULT)
		self.gPosJoueur2.img = bgui.Image(self.gPosJoueur2 , 'menuItems/departjoueurs.png', size=[1.0, 1.0], texco=[(0.5, 0.5), (1, 0.5), (1, 1), (0.5, 1)], options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX|bgui.BGUI_CACHE)


############|||||||position 3||||||||########################
		self.gPosJoueur3 = bgui.Frame(self.grillePosJoueurs, 'gPosJoueur3', sub_theme='ecran', border=3, size=[0.21, 0.16], pos=[0.16, 0.49], options=bgui.BGUI_DEFAULT)
		self.gPosJoueur3.img = bgui.Image(self.gPosJoueur3 , 'menuItems/departjoueurs.png', size=[1.0, 1.0], texco=[(0.5, 0.5), (1, 0.5), (1, 1), (0.5, 1)], options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX|bgui.BGUI_CACHE)


############|||||||position 4||||||||########################
		self.gPosJoueur4 = bgui.Frame(self.grillePosJoueurs, 'gPosJoueur4', sub_theme='ecran', border=3, size=[0.21, 0.16], pos=[0.64, 0.36], options=bgui.BGUI_DEFAULT)
		self.gPosJoueur4.img = bgui.Image(self.gPosJoueur4 , 'menuItems/departjoueurs.png', size=[1.0, 1.0], texco=[(0.5, 0.5), (1, 0.5), (1, 1), (0.5, 1)], options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX|bgui.BGUI_CACHE)



############|||||||position 5||||||||########################
		self.gPosJoueur5 = bgui.Frame(self.grillePosJoueurs, 'gPosJoueur5', sub_theme='ecran', border=3, size=[0.21, 0.16], pos=[0.16, 0.23], options=bgui.BGUI_DEFAULT)
		self.gPosJoueur5.img = bgui.Image(self.gPosJoueur5 , 'menuItems/departjoueurs.png', size=[1.0, 1.0], texco=[(0.5, 0.5), (1, 0.5), (1, 1), (0.5, 1)], options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX|bgui.BGUI_CACHE)



############|||||||position 6||||||||########################
		self.gPosJoueur6 = bgui.Frame(self.grillePosJoueurs, 'gPosJoueur6', sub_theme='ecran', border=3, size=[0.21, 0.16], pos=[0.64, 0.09], options=bgui.BGUI_DEFAULT)
		self.gPosJoueur6.img = bgui.Image(self.gPosJoueur6 , 'menuItems/departjoueurs.png', size=[1.0, 1.0], texco=[(0.5, 0.5), (1, 0.5), (1, 1), (0.5, 1)], options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX|bgui.BGUI_CACHE)



		### fonctions du menu circuit solo
	def rightMap(self, widget):
		gl.listMaps.rotate(1)
		gl.mapName = gl.listMaps[0]
		self.circuit_label.text = "nom du circuit:"+str(gl.mapName)

	def leftMap(self, widget):
		gl.listMaps.rotate(-1)
		gl.mapName = gl.listMaps[0]
		self.circuit_label.text = "nom du circuit:"+str(gl.mapName)

	def rightTours(self, widget):
		if gl.nbLaps <= 8:
			gl.nbLaps += 1
		else:
			gl.nbLaps = 1
		self.nbTours_label.text = str(gl.nbLaps)

	def leftTours(self, widget):
		if gl.nbLaps >= 2:
			gl.nbLaps -= 1
		else:
			gl.nbLaps = 9
		self.nbTours_label.text = str(gl.nbLaps)

	def rightClimat(self, widget):
		if gl.generalConf[4] == 'sun':
			gl.generalConf[4] = 'cloud'
		elif gl.generalConf[4] == 'cloud':
			gl.generalConf[4] = 'rain'
		elif gl.generalConf[4] == 'rain':
			gl.generalConf[4] = 'sun'
		self.climatText.img.update_image('menuItems/' + gl.generalConf[4] + '.png')

	def leftClimat(self, widget):
		if gl.generalConf[4] == 'sun':
			gl.generalConf[4] = 'rain'
		elif gl.generalConf[4] == 'rain':
			gl.generalConf[4] = 'cloud'
		elif gl.generalConf[4] == 'cloud':
			gl.generalConf[4] = 'sun'
		self.climatText.img.update_image('menuItems/' + gl.generalConf[4] + '.png')

	def departSolo(self, widget):
		rd.showMouse(0)
		self.action = "depart"
		self.ouvert = False


	def detruire(self) :
		"""Détruit les widgets"""
		self.frame.parent._remove_widget(self.frame)


	def main(self) :
		"""Refresh des events et de l'affichage"""
		BaseGui.main(self)

class MenuEcranSpliterGui(BaseGui):
	"""
	Gui pour la gestion multijoueurs ecran spliter
	"""
	def __init__(self, parent):

		# Initiate the system
		BaseGui.__init__(self, gl.skin)

		# Cadre général
		self.frame = bgui.Frame(parent, 'cadre', size=[1, 1], pos=[0, 0],
			sub_theme="Invisible", options =  bgui.BGUI_CENTERED | bgui.BGUI_DEFAULT)


#############bouton nombreJoueurs############################
		self.nombreJoueurs_button = bgui.ImageButton(self.frame, 'nombreJoueurs', sub_theme='menu', size=[0.22, 0.08], pos=[0.55, 0.58])
		self.nombreJoueurs_label = bgui.Label(self.nombreJoueurs_button, 'nombreJoueurs', text= str(len(gl.dispPlayers)) + " JOUEURS", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		# Setup an on_click callback
		self.nombreJoueurs_button.on_release = self.nombreJoueur


#############bouton disposition############################
		self.disposition_button = bgui.ImageButton(self.frame, 'disposition', sub_theme='menu', size=[0.22, 0.08], pos=[0.55, 0.38])
		self.disposition_label = bgui.Label(self.disposition_button, 'disposition', text="DISPOSITION", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		# Setup an on_click callback
		self.disposition_button.on_click = self.ecranDisposition

#############bouton placementJoueur############################
		self.placementJoueur_button = bgui.ImageButton(self.frame, 'placementJoueur', sub_theme='menu', size=[0.22, 0.08], pos=[0.55, 0.48])
		self.placementJoueur_label = bgui.Label(self.placementJoueur_button, 'placementJoueur', text="PLACE J", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		# Setup an on_click callback
		self.placementJoueur_button.on_click = self.placementJoueurs

#############bouton valider############################
		self.validerplacementJoueur_button = bgui.ImageButton(self.frame, 'validerplacementJoueur', sub_theme='menu', size=[0.22, 0.08], pos=[0.55, 0.28])
		self.validerplacementJoueur_label = bgui.Label(self.validerplacementJoueur_button, 'validerplacementJoueur', text="VALIDER", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		# Setup an on_click callback
		self.validerplacementJoueur_button.on_click = self.valider



		#Horizontal
		self.deuxjoueurs_ecranHorizontal = bgui.Frame(self.frame, 'deuxjoueurs_ecranHorizontal', sub_theme='ecran', border=1, size=[0.4, 0.45], pos=[0.13, 0.19], options=bgui.BGUI_DEFAULT)
		self.deuxjoueurs_ecranHorizontal.img = bgui.Image(self.deuxjoueurs_ecranHorizontal, 'menuItems/ecranJoueur.png', size=[1.0, 0.5], pos=[0.0, 0.0], options=bgui.BGUI_DEFAULT)
		self.deuxjoueurs_ecranHorizontal.img2 = bgui.Image(self.deuxjoueurs_ecranHorizontal, 'menuItems/ecranJoueur.png', size=[1.0, 0.5], pos=[0.0, 0.5], options=bgui.BGUI_DEFAULT)
		self.posJoueurHH_label = bgui.Label(self.deuxjoueurs_ecranHorizontal, 'posJoueurHH', text=str(gl.conf[0][0][0]), pt_size=24, pos=[0.5, 0.9], options=bgui.BGUI_DEFAULT)
		self.posJoueurHB_label = bgui.Label(self.deuxjoueurs_ecranHorizontal, 'posJoueurHB', text=str(gl.conf[0][1][0]), pt_size=24, pos=[0.5, 0.4], options=bgui.BGUI_DEFAULT)


		#Vertical
		self.deuxjoueurs_ecranVertical = bgui.Frame(self.frame, 'deuxjoueurs_ecranVertical', sub_theme='ecran', border=1, size=[0.4, 0.45], pos=[0.13, 0.19], options=bgui.BGUI_DEFAULT)
		self.deuxjoueurs_ecranVertical.img = bgui.Image(self.deuxjoueurs_ecranVertical, 'menuItems/ecranJoueur.png', size=[0.5, 1.0], pos=[0.0, 0.0], options=bgui.BGUI_DEFAULT)
		self.deuxjoueurs_ecranVertical.img2 = bgui.Image(self.deuxjoueurs_ecranVertical, 'menuItems/ecranJoueur.png', size=[0.5, 1.0], pos=[0.5, 0.0], options=bgui.BGUI_DEFAULT)
		self.posJoueurVH_label = bgui.Label(self.deuxjoueurs_ecranVertical, 'posJoueurVH', text=str(gl.conf[0][0][0]), pt_size=24, pos=[0.25, 0.9], options=bgui.BGUI_DEFAULT)
		self.posJoueurVB_label = bgui.Label(self.deuxjoueurs_ecranVertical, 'posJoueurVB', text=str(gl.conf[0][1][0]), pt_size=24, pos=[0.75, 0.9], options=bgui.BGUI_DEFAULT)

		self.deuxjoueurs_ecranVertical.visible = False

############///////////frame ecran 4 joueurs\\\\\\\\\\\\\\#################

		self.quatrejoueurs_ecran = bgui.Frame(self.frame, 'quatrejoueurs_ecran', sub_theme='ecran', border=1, size=[0.4, 0.45], pos=[0.13, 0.19], options=bgui.BGUI_DEFAULT)
		self.quatrejoueurs_ecran.z_index = 1

		self.quatrejoueurs_ecran.img1 = bgui.Image(self.quatrejoueurs_ecran, 'menuItems/ecranJoueur.png', size=[0.5, 0.5], pos=[0.0, 0.5], options=bgui.BGUI_DEFAULT)
		self.posJoueurHG_label = bgui.Label(self.quatrejoueurs_ecran, 'posJoueurHG', text=str(gl.conf[0][0][0]), pt_size=24, pos=[0.25, 0.9], options=bgui.BGUI_DEFAULT)

		self.quatrejoueurs_ecran.img2 = bgui.Image(self.quatrejoueurs_ecran, 'menuItems/ecranJoueur.png', size=[0.5, 0.5], pos=[0.5, 0.5], options=bgui.BGUI_DEFAULT)
		self.posJoueurHD_label = bgui.Label(self.quatrejoueurs_ecran, 'posJoueurHD', text=str(gl.conf[0][1][0]), pt_size=24, pos=[0.75, 0.9], options=bgui.BGUI_DEFAULT)

		self.quatrejoueurs_ecran.img3 = bgui.Image(self.quatrejoueurs_ecran, 'menuItems/ecranJoueur.png', size=[0.5, 0.5], pos=[0.0, 0.0], options=bgui.BGUI_DEFAULT)
		self.posJoueurBG_label = bgui.Label(self.quatrejoueurs_ecran, 'posJoueurBG', text=str(gl.conf[0][2][0]), pt_size=24, pos=[0.25, 0.4], options=bgui.BGUI_DEFAULT)

		self.quatrejoueurs_ecran.img4 = bgui.Image(self.quatrejoueurs_ecran, 'menuItems/ecranJoueur.png', size=[0.5, 0.5], pos=[0.5, 0.0], options=bgui.BGUI_DEFAULT)
		self.posJoueurBD_label = bgui.Label(self.quatrejoueurs_ecran, 'posJoueurBD', text=str(gl.conf[0][3][0]), pt_size=24, pos=[0.75, 0.4], options=bgui.BGUI_DEFAULT)

		#cache 3 joueurs
		self.cacheTroisJoueursHG_ecran = bgui.Frame(self.quatrejoueurs_ecran, 'cacheTroisJoueursHG_ecran', sub_theme='ecran', border=1, size=[0.5, 0.5], pos=[0.0, 0.5], options=bgui.BGUI_DEFAULT)
		self.cacheTroisJoueursHG_ecran.z_index = 2

		self.cacheTroisJoueursHD_ecran = bgui.Frame(self.quatrejoueurs_ecran, 'cacheTroisJoueursHD_ecran', sub_theme='ecran', border=1, size=[0.5, 0.5], pos=[0.5, 0.5], options=bgui.BGUI_DEFAULT)
		self.cacheTroisJoueursHD_ecran.z_index = 2

		self.cacheTroisJoueursBG_ecran = bgui.Frame(self.quatrejoueurs_ecran, 'cacheTroisJoueursBG_ecran', sub_theme='ecran', border=1, size=[0.5, 0.5], pos=[0.0, 0.0], options=bgui.BGUI_DEFAULT)
		self.cacheTroisJoueursBG_ecran.z_index = 2

		self.cacheTroisJoueursBD_ecran = bgui.Frame(self.quatrejoueurs_ecran, 'cacheTroisJoueursBD_ecran', sub_theme='ecran', border=1, size=[0.5, 0.5], pos=[0.5, 0.0], options=bgui.BGUI_DEFAULT)
		self.cacheTroisJoueursBD_ecran.z_index = 2
		self.quatrejoueurs_ecran.visible = False


	def detruire(self) :
		"""Détruit les widgets"""
		self.frame.parent._remove_widget(self.frame)

	def ecranDisposition(self, widget):
		if gl.dispPlayers[0] == 1:
			gl.dispPlayers[0] = 2
			self.deuxjoueurs_ecranHorizontal.visible = False
			self.deuxjoueurs_ecranVertical.visible = True

		elif gl.dispPlayers[0] == 2:
			self.deuxjoueurs_ecranHorizontal.visible = True
			self.deuxjoueurs_ecranVertical.visible = False
			gl.dispPlayers[0] = 1

		elif gl.dispPlayers[0] == 4:
			gl.dispPlayers[0] = 5
			self.cacheTroisJoueursHD_ecran.visible = True
			self.cacheTroisJoueursHG_ecran.visible = False

		elif gl.dispPlayers[0] == 5:
			gl.dispPlayers[0] = 6
			self.cacheTroisJoueursBD_ecran.visible = True
			self.cacheTroisJoueursHD_ecran.visible = False

		elif gl.dispPlayers[0] == 6:
			gl.dispPlayers[0] = 7
			self.cacheTroisJoueursBG_ecran.visible = True
			self.cacheTroisJoueursBD_ecran.visible = False

		elif gl.dispPlayers[0] == 7:
			gl.dispPlayers[0] = 4
			self.cacheTroisJoueursHG_ecran.visible = True
			self.cacheTroisJoueursBG_ecran.visible = False

	def placementJoueurs(self, widget):
		if gl.dispPlayers[0] == 1 or 2:
			if self.posJoueurHH_label.text == str(gl.conf[0][0][0]):
				self.posJoueurHH_label.text = self.posJoueurVH_label.text = gl.dispPlayers[1] = str(gl.conf[0][1][0])
				self.posJoueurHB_label.text = self.posJoueurVB_label.text = gl.dispPlayers[2] = str(gl.conf[0][0][0])

			else:
				self.posJoueurHH_label.text = self.posJoueurVH_label.text = gl.dispPlayers[1] = str(gl.conf[0][0][0])
				self.posJoueurHB_label.text = self.posJoueurVB_label.text = gl.dispPlayers[2] = str(gl.conf[0][1][0])

		if gl.dispPlayers[0] == 3:
			gl.lstPlayers.rotate(1)
			print(gl.lstPlayers)
			self.posJoueurHG_label.text = gl.lstPlayers[0]
			self.posJoueurHD_label.text = gl.lstPlayers[1]
			self.posJoueurBG_label.text = gl.lstPlayers[2]
			self.posJoueurBD_label.text = gl.lstPlayers[3]
			del gl.dispPlayers[1:]
			gl.dispPlayers.append(gl.lstPlayers[0])
			gl.dispPlayers.append(gl.lstPlayers[1])
			gl.dispPlayers.append(gl.lstPlayers[2])
			gl.dispPlayers.append(gl.lstPlayers[3])
			#print(gl.dispPlayers)

		if gl.dispPlayers[0] == 4:
			gl.lstPlayers.rotate(1)
			self.posJoueurHD_label.text = gl.lstPlayers[0]
			self.posJoueurBG_label.text = gl.lstPlayers[1]
			self.posJoueurBD_label.text = gl.lstPlayers[2]
			del gl.dispPlayers[1:]
			gl.dispPlayers.append(gl.lstPlayers[0])
			gl.dispPlayers.append(gl.lstPlayers[1])
			gl.dispPlayers.append(gl.lstPlayers[2])
			#print(gl.dispPlayers)

		if gl.dispPlayers[0] == 5:
			gl.lstPlayers.rotate(1)
			self.posJoueurHG_label.text = gl.lstPlayers[0]
			self.posJoueurBG_label.text = gl.lstPlayers[1]
			self.posJoueurBD_label.text = gl.lstPlayers[2]
			del gl.dispPlayers[1:]
			gl.dispPlayers.append(gl.lstPlayers[0])
			gl.dispPlayers.append(gl.lstPlayers[1])
			gl.dispPlayers.append(gl.lstPlayers[2])
			#print(gl.dispPlayers)

		if gl.dispPlayers[0] == 6:
			gl.lstPlayers.rotate(1)
			self.posJoueurHG_label.text = gl.lstPlayers[0]
			self.posJoueurBG_label.text = gl.lstPlayers[1]
			self.posJoueurHD_label.text = gl.lstPlayers[2]
			del gl.dispPlayers[1:]
			gl.dispPlayers.append(gl.lstPlayers[0])
			gl.dispPlayers.append(gl.lstPlayers[1])
			gl.dispPlayers.append(gl.lstPlayers[2])
			#print(gl.dispPlayers)

		if gl.dispPlayers[0] == 7:
			gl.lstPlayers.rotate(1)
			self.posJoueurHG_label.text = gl.lstPlayers[0]
			self.posJoueurBD_label.text = gl.lstPlayers[1]
			self.posJoueurHD_label.text = gl.lstPlayers[2]
			del gl.dispPlayers[1:]
			gl.dispPlayers.append(gl.lstPlayers[0])
			gl.dispPlayers.append(gl.lstPlayers[1])
			gl.dispPlayers.append(gl.lstPlayers[2])
			#print(gl.dispPlayers)

	def nombreJoueur(self, widget):
		if len(gl.dispPlayers) == 3:
			gl.dispPlayers.append(gl.conf[0][2][0])
			self.nombreJoueurs_label.text = str(len(gl.dispPlayers)-1) + " JOUEURS"
			self.cacheTroisJoueursHD_ecran.visible = self.cacheTroisJoueursBG_ecran.visible = self.cacheTroisJoueursBD_ecran.visible = False
			self.cacheTroisJoueursHG_ecran.visible = self.quatrejoueurs_ecran.visible = True
			self.deuxjoueurs_ecranHorizontal.visible = self.deuxjoueurs_ecranVertical.visible = False
			gl.dispPlayers[0] = 4
			gl.lstPlayers = coll.deque(gl.dispPlayers[1:])

		elif len(gl.dispPlayers) == 4:
			gl.dispPlayers.append(gl.conf[0][3][0])
			self.nombreJoueurs_label.text = str(len(gl.dispPlayers)-1) + " JOUEURS"
			self.cacheTroisJoueursHG_ecran.visible = self.cacheTroisJoueursHD_ecran.visible = self.cacheTroisJoueursBG_ecran.visible = self.cacheTroisJoueursBD_ecran.visible = False
			gl.dispPlayers[0] = 3
			gl.lstPlayers = coll.deque(gl.dispPlayers[1:])

		elif len(gl.dispPlayers) == 5:
			gl.dispPlayers.remove(gl.conf[0][3][0])
			gl.dispPlayers.remove(gl.conf[0][2][0])
			self.nombreJoueurs_label.text = str(len(gl.dispPlayers)-1) + " JOUEURS"
			self.quatrejoueurs_ecran.visible = False
			self.deuxjoueurs_ecranHorizontal.visible = True
			gl.dispPlayers[0] = 1
			gl.lstPlayers = coll.deque(gl.dispPlayers[1:])

	def valider(self, widget):
		#self.detruire()
		self.action = "valider"
		self.ouvert = False

	def main(self) :
		"""Refresh des events et de l'affichage"""
		BaseGui.main(self)

class MenuTelechargementGui(BaseGui):
	"""
	Gui pour la visualisation d'un serveur
	:note: Ne pas oublier de retirer le bouton Retour !
	"""
	def __init__(self, parent):
		# Initiate the system
		BaseGui.__init__(self, gl.skin)

		# Cadre général
		self.frame = bgui.Frame(parent, 'cadre', size=[1, 1], pos=[0, 0],
			sub_theme="Invisible", options =  bgui.BGUI_CENTERED | bgui.BGUI_DEFAULT)


		# Titre
		self.titre = bgui.Label(self.frame, 'titre', text="TELECHARGEMENT", pt_size=32, pos=[0, .935],
			options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)




	def detruire(self) :
		"""Détruit les widgets"""
		self.frame.parent._remove_widget(self.frame)

	def main(self) :
		"""Refresh des events et de l'affichage"""
		BaseGui.main(self)

class MenuMultijoueursGui(BaseGui):
	"""
	Gui le choix du type de multijoueurs
	"""
	def __init__(self, parent):
		# Initiate the system
		BaseGui.__init__(self, gl.skin)

		# Cadre général
		self.frame = bgui.Frame(parent, 'cadre', size=[1, 1], pos=[0, 0],
			sub_theme="Invisible", options =  bgui.BGUI_CENTERED | bgui.BGUI_DEFAULT)


#############bouton ecransplitter############################
		self.ecransplitter_button = bgui.ImageButton(self.frame, 'ecransplitter', sub_theme='menu', size=[0.24, 0.08], pos=[0.4, 0.55])
		self.ecransplitter_label = bgui.Label(self.ecransplitter_button, 'ecransplitter', text="ECRAN SPLITTER", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		# Setup an on_click callback
		self.ecransplitter_button.on_click = self.ecranSplitM

#############bouton reseaulocal############################
		self.reseauLocal_button = bgui.ImageButton(self.frame, 'reseauLocal', sub_theme='menu', size=[0.24, 0.08], pos=[0.4, 0.45])
		self.reseauLocal_label = bgui.Label(self.reseauLocal_button, 'reseauLocal', text="RESEAU LOCAL", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

#############bouton reseauinternet############################
		self.reseauInternet_button = bgui.ImageButton(self.frame, 'reseauInternet', sub_theme='menu', size=[0.24, 0.08], pos=[0.4, 0.35])
		self.reseauInternet_label = bgui.Label(self.reseauInternet_button, 'reseauInternet', text="RESEAU INTERNET", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		# Autres attributs
		self.action = None



	def detruire(self) :
		"""Détruit les widgets"""
		self.frame.parent._remove_widget(self.frame)

	def ecranSplitM(self, widget) :
		self.detruire()
		self.action = "MenuEcranSpliter"
		self.ouvert = False

	def main(self) :
		"""Refresh des events et de l'affichage"""
		BaseGui.main(self)

class MenuPrincipalGui(BaseGui):
	"""
	Gui pour la liste des profils
	"""
	def __init__(self, parent):
		# Initiate the system
		BaseGui.__init__(self, gl.skin)

		# Fond
		self.frame = bgui.Frame(parent, 'fond', size=[1, 1], pos=[0, 0],
			sub_theme="Invisible", options =  bgui.BGUI_CENTERED | bgui.BGUI_DEFAULT)

############///////////frame info \\\\\\\\\\\\\\#################

		self.info_ecran = bgui.Frame(self.frame, 'info_ecran', sub_theme='Invisible', border=1, size=[0.44, 0.75], pos=[0.06, 0.02], options=bgui.BGUI_DEFAULT)
		self.info_label = bgui.Label(self.info_ecran, 'info_label', text="bienvenue " + str(gl.conf[0][0][0]), pt_size=24, pos=[0.02, 0.84], options=bgui.BGUI_DEFAULT)

#############bouton joueursolo ############################
		self.joueursolo_button = bgui.ImageButton(self.frame, 'joueursolo', sub_theme='menu', size=[0.24, 0.08], pos=[0.75, 0.48])
		self.joueursolo_label = bgui.Label(self.joueursolo_button, 'joueursolo', text="JOUEUR SOLO", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		# Setup an on_click callback
		self.joueursolo_button.on_click = self.joueurSoloM

#############bouton multijoueur ############################
		self.multijoueur_button = bgui.ImageButton(self.frame, 'multijoueur', sub_theme='menu', size=[0.24, 0.08], pos=[0.75, 0.38])
		self.multijoueur_label = bgui.Label(self.multijoueur_button, 'multijoueur', text="MULTIJOUEURS", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		# Setup an on_click callback
		self.multijoueur_button.on_click = self.multijoueurM

#############bouton telechargements ############################
		self.telechargements_button = bgui.ImageButton(self.frame, 'telechargements', sub_theme='menu', size=[0.24, 0.08], pos=[0.75, 0.28])
		self.telechargements_label = bgui.Label(self.telechargements_button, 'telechargements', text="ADDONS", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		# Setup an on_click callback
		self.telechargements_button.on_click = self.telechargementM

#############bouton options############################
		self.options_button = bgui.ImageButton(self.frame, 'options', sub_theme='menu', size=[0.24, 0.08], pos=[0.75, 0.18])
		self.options_label = bgui.Label(self.options_button, 'options', text="OPTIONS", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
		# Setup an on_click callback
		self.options_button.on_click = self.optionsM


		# Autres attributs
		self.action = None
		self.selection = None


	def detruire(self) :
		"""Détruit les widgets"""
		self.frame.parent._remove_widget(self.frame)

	def joueurSoloM(self, widget) :
		self.detruire()
		self.action = "joueurSolo"
		self.ouvert = False

	def multijoueurM(self, widget) :
		self.detruire()
		self.action = "MenuMultijoueurs"
		self.ouvert = False

	def telechargementM(self, widget) :
		self.detruire()
		self.action = "MenuTelechargement"
		self.ouvert = False

	def optionsM(self, widget) :
		self.detruire()
		self.action = "MenuOptions"
		self.ouvert = False

	def main(self) :
		"""Refresh des events et de l'affichage"""
		BaseGui.main(self)

class jouerSoloGui(BaseGui):
	"""
	Gui pour le choix de la voiture en mode 1 joueur
	"""
	def __init__(self, parent):
		# Initiate the system
		BaseGui.__init__(self, gl.skin)

		# Cadre général
		self.frame = bgui.Frame(parent, 'cadre', size=[1, 1], pos=[0, 0],
			sub_theme="Invisible", options =  bgui.BGUI_CENTERED | bgui.BGUI_DEFAULT)

		self.introVoiture_label = bgui.Label(self.frame, 'introVoiture_label', text="Voiture:", pt_size=31, pos=[0.67, 0.82], options=bgui.BGUI_DEFAULT)
		self.voiture_label = bgui.Label(self.frame, 'voiture_label', sub_theme='MenuInfo', text="voiture", pt_size=31, pos=[0.73, 0.82], options=bgui.BGUI_DEFAULT)

		self.introRoue_label = bgui.Label(self.frame, 'introRoue_label', text="Roue:", pt_size=31, pos=[0.67, 0.78], options=bgui.BGUI_DEFAULT)
		self.roue_label = bgui.Label(self.frame, 'roue_label', sub_theme='MenuInfo', text="Roue", pt_size=31, pos=[0.73, 0.78], options=bgui.BGUI_DEFAULT)

		
#############bouton testSound############################
		self.Sound_label = bgui.Label(self.frame, 'Sound', text="Sound:", pt_size=31, pos=[0.67, 0.58], options=bgui.BGUI_DEFAULT)
		self.testSound_button = bgui.ImageButton(self.frame, 'testSound', sub_theme='menu', size=[0.10, 0.05], pos=[0.73, 0.58])
		self.testSound_label = bgui.Label(self.testSound_button, 'testSound', text="play", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

				# Setup an on_click callback
		self.testSound_button.on_click = self.testSound

#############bouton flecheG############################
		self.flecheG_button = bgui.ImageButton(self.frame, 'flecheG', sub_theme='selFlecheG', size=[0.05, 0.38], pos=[0.05, 0.48])

		# Setup an on_click callback
		self.flecheG_button.on_click = self.leftcar

#############bouton fleche############################
		self.fleche_button = bgui.ImageButton(self.frame, 'fleche', sub_theme='selFleche', size=[0.05, 0.38], pos=[0.57, 0.48])

		# Setup an on_click callback
		self.fleche_button.on_click = self.rightcar

#############bouton flecheGRoue############################
		self.flecheGRoue_button = bgui.ImageButton(self.frame, 'flecheGRoue', sub_theme='selFlecheG', size=[0.05, 0.22], pos=[0.05, 0.25])

		# Setup an on_click callback
		self.flecheGRoue_button.on_click = self.leftwheels
#############bouton flecheRoue############################
		self.flecheRoue_button = bgui.ImageButton(self.frame, 'flecheRoue', sub_theme='selFleche', size=[0.05, 0.22], pos=[0.57, 0.25])

		# Setup an on_click callback
		self.flecheRoue_button.on_click = self.rightwheels

#############bouton testerVoiture############################
		self.testerVoiture_button = bgui.ImageButton(self.frame, 'testerVoiture', sub_theme='menu', size=[0.24, 0.08], pos=[0.15, 0.08])
		self.testerVoiture_label = bgui.Label(self.testerVoiture_button, 'testerVoiture', text="TESTER", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

				# Setup an on_click callback
		self.testerVoiture_button.on_click = self.testerVoiture

#############bouton validerVoiture############################
		self.validerVoiture_button = bgui.ImageButton(self.frame, 'validerVoiture', sub_theme='menu', size=[0.24, 0.08], pos=[0.45, 0.08])
		self.valider_label = bgui.Label(self.validerVoiture_button, 'validerVoiture', text="VALIDER", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

				# Setup an on_click callback
		self.validerVoiture_button.on_click = self.circuitMenu


		# Autres attributs
		self.action = None



	def detruire(self) :
		"""Détruit les widgets"""
		self.frame.parent._remove_widget(self.frame)

	def leftwheels(self, widget):
		gl.lstRoue.rotate(-1)

		gl.conf[0][0][4] = gl.lstRoue[gl.posRoueJun]
		gl.voiture.setWheels( str(gl.conf[0][0][4]) )
		self.roue_label.text = str(gl.conf[0][0][4])

	def rightwheels(self, widget):
		gl.lstRoue.rotate(1)

		gl.conf[0][0][4] = gl.lstRoue[gl.posRoueJun]
		gl.voiture.setWheels( str(gl.conf[0][0][4]) )
		self.roue_label.text = str(gl.conf[0][0][4])

	def leftcar(self, widget):
		gl.lstVoiture.rotate(-1)
		gl.conf[0][0][3] = gl.lstVoiture[gl.posVoitureJun]
		gl.voiture.setVehicle( str(gl.conf[0][0][3]) )
		self.voiture_label.text = str(gl.conf[0][0][3])

	def rightcar(self, widget):
		gl.lstVoiture.rotate(1)
		gl.conf[0][0][3] = gl.lstVoiture[gl.posVoitureJun]
		gl.voiture.setVehicle( str(gl.conf[0][0][3]) )
		self.voiture_label.text = str(gl.conf[0][0][3])

	def testSound(self, widget):
		if self.testSound_label.text == "play":
			gl.voiture.startSound()
			self.testSound_label.text = "stop"
		elif self.testSound_label.text == "stop":
			gl.voiture.stopSound()
			self.testSound_label.text = "play"
		
	def testerVoiture(self, widget):
		rd.showMouse(0)
		gl.dispPlayers=[0, gl.conf[0][0][0]]
		del(gl.voiture)
		confParser.savePlayer()
		gl.mapName = "anneauDeTest"
		scene = gl.getCurrentScene()
		for lib in gl.LibList():
			gl.LibFree(lib)
		scene.replace('game')

	def circuitMenu(self, widget):
		self.detruire()
		self.action = "MenuSelectionCircuit"
		self.ouvert = False

	def main(self) :
		"""Refresh des events et de l'affichage"""
		BaseGui.main(self)

class MenuAffichageGui(BaseGui):
	"""
	Gui pour l'affichage
	"""
	def __init__(self, parent):
		# Initiate the system
		BaseGui.__init__(self, gl.skin)

		# Fond
		self.frame = bgui.Frame(parent, 'cadre', size=[1, 1], pos=[0, 0],
			sub_theme="Invisible", options =  bgui.BGUI_CENTERED | bgui.BGUI_DEFAULT)

#############bouton activate mirror############################
		self.mirror_button = bgui.ImageButton(self.frame, 'mirrorbt', sub_theme='check', size=[0.04, 0.04], pos=[0.42, 0.80])
				# Setup an on_click callback
		self.mirror_button.on_click = self.enableMirror
		##mirror label
		self.affichage_label = bgui.Label(self.frame, 'mirror', text="activation des reflets temp reel", pt_size=24, pos=[0.03, 0.80], options=bgui.BGUI_DEFAULT)


#############bouton activate AnisotropicFiltering############################
		self.AnisotropicFiltering_button = bgui.Frame(self.frame, 'AnisotropicFiltering_button', border=1, size=[0.04, 0.04], pos=[0.42, 0.70], options=bgui.BGUI_DEFAULT)
		self.AnisotropicFiltering_label_value = bgui.Label(self.AnisotropicFiltering_button, 'AnisotropicFiltering', text=str(gl.generalConf[1]), pt_size=20, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

				# Setup an on_click callback
		self.AnisotropicFiltering_button.on_click = self.AnisotropicFilteringLevel

		##label AnisotropicFiltering
		self.AnisotropicFiltering_label = bgui.Label(self.frame, 'AnisotropicFiltering', text="Anisotropic Filtering", pt_size=24, pos=[0.03, 0.70], options=bgui.BGUI_DEFAULT)

	def detruire(self) :
		"""Détruit les widgets"""
		self.frame.parent._remove_widget(self.frame)

	def enableMirror(self, widget):
		print(self.mirror_button.state)


	def AnisotropicFilteringLevel(self, widget):
		if gl.generalConf[1] >= 16:
			gl.generalConf[1] = 1
		else:
			gl.generalConf[1] = gl.generalConf[1]*2
		self.AnisotropicFiltering_label_value.text = str(gl.generalConf[1])

	def main(self) :
		"""Refresh des events et de l'affichage"""
		BaseGui.main(self)

class MenuNomsJoueursGui(BaseGui):
	"""
	Gui pour le choix du nom des joueurs
	"""
	def __init__(self, parent):
		# Initiate the system
		BaseGui.__init__(self, gl.skin)

		# Fond
		self.frame = bgui.Frame(parent, 'cadre', size=[1, 1], pos=[0, 0],
			sub_theme="Invisible", options =  bgui.BGUI_CENTERED | bgui.BGUI_DEFAULT)

#############input joueur 1############################
		self.joueur1_label = bgui.Label(self.frame, 'joueur1', text="le premier joueur s\'appelle:", pt_size=30, pos=[0.02, 0.8], options=bgui.BGUI_DEFAULT)
		self.joueur1_input = bgui.TextInput(self.frame, 'joueur1_input', str(gl.conf[0][0][0]), pt_size=30, size=[.2, .05], pos=[0.02, 0.73], input_options = bgui.BGUI_INPUT_NONE, options = bgui.BGUI_DEFAULT)
		self.joueur1_input.activate()
		self.joueur1_input.on_enter_key = self.joueur1_on_input_enter

#############input joueur 2############################
		self.joueur2_label = bgui.Label(self.frame, 'joueur2', text="le second joueur s\'appelle:", pt_size=30, pos=[0.02, 0.6], options=bgui.BGUI_DEFAULT)
		self.joueur2_input = bgui.TextInput(self.frame, 'joueur2_input', str(gl.conf[0][1][0]), pt_size=30, size=[.2, .05], pos=[0.02, 0.53], input_options = bgui.BGUI_INPUT_NONE, options = bgui.BGUI_DEFAULT)
		self.joueur2_input.activate()
		self.joueur2_input.on_enter_key = self.joueur2_on_input_enter

#############input joueur 3############################
		self.joueur3_label = bgui.Label(self.frame, 'joueur3', text="le troisieme joueur s\'appelle:", pt_size=30, pos=[0.02, 0.4], options=bgui.BGUI_DEFAULT)
		self.joueur3_input = bgui.TextInput(self.frame, 'joueur3_input', str(gl.conf[0][2][0]), pt_size=30, size=[.2, .05], pos=[0.02, 0.33],input_options = bgui.BGUI_INPUT_NONE, options = bgui.BGUI_DEFAULT)
		self.joueur3_input.activate()
		self.joueur3_input.on_enter_key = self.joueur3_on_input_enter

#############input joueur 4############################
		self.joueur4_label = bgui.Label(self.frame, 'joueur4', text="le quatrieme joueur s\'appelle:", pt_size=30, pos=[0.02, 0.2], options=bgui.BGUI_DEFAULT)
		self.joueur4_input = bgui.TextInput(self.frame, 'joueur4_input', str(gl.conf[0][3][0]), pt_size=30, size=[.2, .05], pos=[0.02, 0.13], input_options = bgui.BGUI_INPUT_NONE, options = bgui.BGUI_DEFAULT)
		self.joueur4_input.activate()
		self.joueur4_input.on_enter_key = self.joueur4_on_input_enter

	def detruire(self) :
		"""Détruit les widgets"""
		self.frame.parent._remove_widget(self.frame)

	def joueur1_on_input_enter(self, widget):
		widget.deactivate()
		gl.conf[0][0][0] = widget.text
		confParser.savePlayer()

	def joueur2_on_input_enter(self, widget):
		widget.deactivate()
		gl.conf[0][1][0] = widget.text
		confParser.savePlayer()

	def joueur3_on_input_enter(self, widget):
		widget.deactivate()
		gl.conf[0][2][0] = widget.text
		confParser.savePlayer()

	def joueur4_on_input_enter(self, widget):
		widget.deactivate()
		gl.conf[0][3][0] = widget.text
		confParser.savePlayer()

	def main(self) :
		"""Refresh des events et de l'affichage"""
		BaseGui.main(self)

class MenuCommandesGui(BaseGui):
	"""
	Gui pour le choix du nom des joueurs
	"""
	def __init__(self, parent):
		# Initiate the system
		BaseGui.__init__(self, gl.skin)

		# Fond
		self.frame = bgui.Frame(parent, 'cadre', size=[1, 1], pos=[0, 0],
			sub_theme="Invisible", options =  bgui.BGUI_CENTERED | bgui.BGUI_DEFAULT)

		# nom du joueur en cour

		self.intituler_joueur_label = bgui.Label(self.frame, 'intituler_joueur', text="nom du joueur courant: ", pt_size=45, pos=[0.05, 0.85], options=bgui.BGUI_DEFAULT)
		self.joueur_label = bgui.Label(self.frame, 'joueur', text=gl.configurablePlayers[0], pt_size=36, pos=[0.1, 0.8], options=bgui.BGUI_DEFAULT)

		# changement de joueur

#############bouton flechejoueurDR############################
		self.flechejoueurDR_button = bgui.ImageButton(self.frame, 'flechejoueurDR', sub_theme='selFleche',
			size=[0.02, 0.05], pos=[0.2, 0.79])

		# Setup an on_click callback
		self.flechejoueurDR_button.on_click = self.rightjoueur

#############bouton flechejoueurGA############################
		self.flechejoueurGA_button = bgui.ImageButton(self.frame, 'flechejoueurGA', sub_theme='selFlecheG',
			size=[0.02, 0.05], pos=[0.04, 0.79])

		# Setup an on_click callback
		self.flechejoueurGA_button.on_click = self.leftjoueur


		# intituler des touches

		self.accelerateur_label = bgui.Label(self.frame, 'accelerateur', text="  accelerateur: ", pt_size=40, pos=[0.15, 0.65], options=bgui.BGUI_DEFAULT)
		self.frein_label = bgui.Label(self.frame, 'frein', text="    frein: ", pt_size=40, pos=[0.15, 0.60], options=bgui.BGUI_DEFAULT)
		self.droite_label = bgui.Label(self.frame, 'droite', text="    droite: ", pt_size=40, pos=[0.15, 0.55], options=bgui.BGUI_DEFAULT)
		self.gauche_label = bgui.Label(self.frame, 'gauche', text="    gauche: ", pt_size=40, pos=[0.15, 0.50], options=bgui.BGUI_DEFAULT)
		self.freinMain_label = bgui.Label(self.frame, 'freinMain', text="frein a main: ", pt_size=40, pos=[0.15, 0.45], options=bgui.BGUI_DEFAULT)
		self.nitro_label = bgui.Label(self.frame, 'nitro', text="    nitro: ", pt_size=40, pos=[0.15, 0.40], options=bgui.BGUI_DEFAULT)
		self.passerVitesse_label = bgui.Label(self.frame, 'passerVitesse', text="passer Vitesse: ", pt_size=40, pos=[0.15, 0.35], options=bgui.BGUI_DEFAULT)
		self.retrograder_label = bgui.Label(self.frame, 'retrograder', text="retrograder: ", pt_size=40, pos=[0.15, 0.30], options=bgui.BGUI_DEFAULT)
		self.respawn_label = bgui.Label(self.frame, 'respawn', text="reapparaitre: ", pt_size=40, pos=[0.15, 0.25], options=bgui.BGUI_DEFAULT)
		self.upcam_label = bgui.Label(self.frame, 'upcam', text="changer de camera: ", pt_size=40, pos=[0.15, 0.20], options=bgui.BGUI_DEFAULT)

		# touche courante

		self.cur_accelerateur_label = bgui.Label(self.frame, 'cur_accelerateur', text=ev.EventToString(int(gl.conf[0][0][2][0][1])), pt_size=40, pos=[0.35, 0.65], options=bgui.BGUI_DEFAULT)
		self.cur_accelerateur_label.state = 0
		self.cur_frein_label = bgui.Label(self.frame, 'cur_frein', text=ev.EventToString(int(gl.conf[0][0][2][1][1])), pt_size=40, pos=[0.35, 0.60], options=bgui.BGUI_DEFAULT)
		self.cur_frein_label.state = 0
		self.cur_droite_label = bgui.Label(self.frame, 'cur_droite', text=ev.EventToString(int(gl.conf[0][0][2][2][1])), pt_size=40, pos=[0.35, 0.55], options=bgui.BGUI_DEFAULT)
		self.cur_droite_label.state = 0
		self.cur_gauche_label = bgui.Label(self.frame, 'cur_gauche', text=ev.EventToString(int(gl.conf[0][0][2][3][1])), pt_size=40, pos=[0.35, 0.50], options=bgui.BGUI_DEFAULT)
		self.cur_gauche_label.state = 0
		self.cur_freinMain_label = bgui.Label(self.frame, 'cur_freinMain', text=ev.EventToString(int(gl.conf[0][0][2][4][1])), pt_size=40, pos=[0.35, 0.45], options=bgui.BGUI_DEFAULT)
		self.cur_freinMain_label.state = 0
		self.cur_nitro_label = bgui.Label(self.frame, 'cur_nitro', text=ev.EventToString(int(gl.conf[0][0][2][5][1])), pt_size=40, pos=[0.35, 0.40], options=bgui.BGUI_DEFAULT)
		self.cur_nitro_label.state = 0
		self.cur_passerVitesse_label = bgui.Label(self.frame, 'cur_passerVitesse', text=ev.EventToString(int(gl.conf[0][0][2][6][1])), pt_size=40, pos=[0.35, 0.35], options=bgui.BGUI_DEFAULT)
		self.cur_passerVitesse_label.state = 0
		self.cur_retrograder_label = bgui.Label(self.frame, 'cur_retrograder', text=ev.EventToString(int(gl.conf[0][0][2][7][1])), pt_size=40, pos=[0.35, 0.30], options=bgui.BGUI_DEFAULT)
		self.cur_retrograder_label.state = 0
		self.cur_respawn_label = bgui.Label(self.frame, 'cur_respawn', text=ev.EventToString(int(gl.conf[0][0][2][8][1])), pt_size=40, pos=[0.35, 0.25], options=bgui.BGUI_DEFAULT)
		self.cur_respawn_label.state = 0
		self.cur_upcam_label = bgui.Label(self.frame, 'cur_upcam', text=ev.EventToString(int(gl.conf[0][0][2][9][1])), pt_size=40, pos=[0.35, 0.20], options=bgui.BGUI_DEFAULT)
		self.cur_upcam_label.state = 0

		# bouton modifier

		self.ModifierAccelerateur_button = bgui.ImageButton(self.frame, 'ModifierAccelerateur', sub_theme='menu', size=[0.14, 0.04], pos=[0.56, 0.65])
		self.ModifierAccelerateur_label = bgui.Label(self.ModifierAccelerateur_button, 'ModifierAccelerateur', text="MODIFIER", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

				# Setup an on_click callback
		self.ModifierAccelerateur_button.on_click = self.ModifierAccelerateur


		self.Modifierfrein_button = bgui.ImageButton(self.frame, 'Modifierfrein', sub_theme='menu', size=[0.14, 0.04], pos=[0.56, 0.60])
		self.Modifierfrein_label = bgui.Label(self.Modifierfrein_button, 'Modifierfrein', text="MODIFIER", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

				# Setup an on_click callback
		self.Modifierfrein_button.on_click = self.Modifierfrein


		self.Modifierdroite_button = bgui.ImageButton(self.frame, 'Modifierdroite', sub_theme='menu', size=[0.14, 0.04], pos=[0.56, 0.55])
		self.Modifierdroite_label = bgui.Label(self.Modifierdroite_button, 'Modifierdroite', text="MODIFIER", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

				# Setup an on_click callback
		self.Modifierdroite_button.on_click = self.Modifierdroite

		self.Modifiergauche_button = bgui.ImageButton(self.frame, 'Modifiergauche', sub_theme='menu', size=[0.14, 0.04], pos=[0.56, 0.50])
		self.Modifiergauche_label = bgui.Label(self.Modifiergauche_button, 'Modifiergauche', text="MODIFIER", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

				# Setup an on_click callback
		self.Modifiergauche_button.on_click = self.Modifiergauche

		self.ModifierfreinMain_button = bgui.ImageButton(self.frame, 'ModifierfreinMain', sub_theme='menu', size=[0.14, 0.04], pos=[0.56, 0.45])
		self.ModifierfreinMain_label = bgui.Label(self.ModifierfreinMain_button, 'ModifierfreinMain', text="MODIFIER", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

				# Setup an on_click callback
		self.ModifierfreinMain_button.on_click = self.ModifierfreinMain

		self.Modifiernitro_button = bgui.ImageButton(self.frame, 'Modifiernitro', sub_theme='menu', size=[0.14, 0.04], pos=[0.56, 0.40])
		self.Modifiernitro_label = bgui.Label(self.Modifiernitro_button, 'Modifiernitro', text="MODIFIER", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

				# Setup an on_click callback
		self.Modifiernitro_button.on_click = self.Modifiernitro

		self.ModifierpasserVitesse_button = bgui.ImageButton(self.frame, 'ModifierpasserVitesse', sub_theme='menu', size=[0.14, 0.04], pos=[0.56, 0.35])
		self.ModifierpasserVitesse_label = bgui.Label(self.ModifierpasserVitesse_button, 'ModifierpasserVitesse', text="MODIFIER", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

				# Setup an on_click callback
		self.ModifierpasserVitesse_button.on_click = self.ModifierpasserVitesse

		self.Modifierretrograder_button = bgui.ImageButton(self.frame, 'Modifierretrograder', sub_theme='menu', size=[0.14, 0.04], pos=[0.56, 0.30])
		self.Modifierretrograder_label = bgui.Label(self.Modifierretrograder_button, 'Modifierretrograder', text="MODIFIER", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

				# Setup an on_click callback
		self.Modifierretrograder_button.on_click = self.Modifierretrograder

		self.Modifierrespawn_button = bgui.ImageButton(self.frame, 'Modifierrespawn', sub_theme='menu', size=[0.14, 0.04], pos=[0.56, 0.25])
		self.Modifierrespawn_label = bgui.Label(self.Modifierrespawn_button, 'Modifierrespawn', text="MODIFIER", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

				# Setup an on_click callback
		self.Modifierrespawn_button.on_click = self.Modifierrespawn

		self.Modifierupcam_button = bgui.ImageButton(self.frame, 'Modifierupcam', sub_theme='menu', size=[0.14, 0.04], pos=[0.56, 0.20])
		self.Modifierupcam_label = bgui.Label(self.Modifierupcam_button, 'Modifierupcam', text="MODIFIER", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

				# Setup an on_click callback
		self.Modifierupcam_button.on_click = self.Modifierupcam

	def rightjoueur(self, widget):
		if self.joueur_label.text == gl.configurablePlayers[0]:
			self.joueur_label.text = gl.configurablePlayers[1]
			self.cur_accelerateur_label.text = ev.EventToString(int(gl.conf[0][1][2][0][1]))
			self.cur_frein_label.text = ev.EventToString(int(gl.conf[0][1][2][1][1]))
			self.cur_droite_label.text = ev.EventToString(int(gl.conf[0][1][2][2][1]))
			self.cur_gauche_label.text = ev.EventToString(int(gl.conf[0][1][2][3][1]))
			self.cur_freinMain_label.text = ev.EventToString(int(gl.conf[0][1][2][4][1]))
			self.cur_nitro_label.text = ev.EventToString(int(gl.conf[0][1][2][5][1]))
			self.cur_passerVitesse_label.text = ev.EventToString(int(gl.conf[0][1][2][6][1]))
			self.cur_retrograder_label.text = ev.EventToString(int(gl.conf[0][1][2][7][1]))
			self.cur_upcam_label.text = ev.EventToString(int(gl.conf[0][1][2][8][1]))

		elif self.joueur_label.text == gl.configurablePlayers[1]:
			self.joueur_label.text = gl.configurablePlayers[2]
			self.cur_accelerateur_label.text = ev.EventToString(int(gl.conf[0][2][2][0][1]))
			self.cur_frein_label.text = ev.EventToString(int(gl.conf[0][2][2][1][1]))
			self.cur_droite_label.text = ev.EventToString(int(gl.conf[0][2][2][2][1]))
			self.cur_gauche_label.text = ev.EventToString(int(gl.conf[0][2][2][3][1]))
			self.cur_freinMain_label.text = ev.EventToString(int(gl.conf[0][2][2][4][1]))
			self.cur_nitro_label.text = ev.EventToString(int(gl.conf[0][2][2][5][1]))
			self.cur_passerVitesse_label.text = ev.EventToString(int(gl.conf[0][2][2][6][1]))
			self.cur_retrograder_label.text = ev.EventToString(int(gl.conf[0][2][2][7][1]))
			self.cur_upcam_label.text = ev.EventToString(int(gl.conf[0][2][2][8][1]))

		elif self.joueur_label.text == gl.configurablePlayers[2]:
			self.joueur_label.text = gl.configurablePlayers[3]
			self.cur_accelerateur_label.text = ev.EventToString(int(gl.conf[0][3][2][0][1]))
			self.cur_frein_label.text = ev.EventToString(int(gl.conf[0][3][2][1][1]))
			self.cur_droite_label.text = ev.EventToString(int(gl.conf[0][3][2][2][1]))
			self.cur_gauche_label.text = ev.EventToString(int(gl.conf[0][3][2][3][1]))
			self.cur_freinMain_label.text = ev.EventToString(int(gl.conf[0][3][2][4][1]))
			self.cur_nitro_label.text = ev.EventToString(int(gl.conf[0][3][2][5][1]))
			self.cur_passerVitesse_label.text = ev.EventToString(int(gl.conf[0][3][2][6][1]))
			self.cur_retrograder_label.text = ev.EventToString(int(gl.conf[0][3][2][7][1]))
			self.cur_upcam_label.text = ev.EventToString(int(gl.conf[0][3][2][8][1]))

		elif self.joueur_label.text == gl.configurablePlayers[3]:
			self.joueur_label.text = gl.configurablePlayers[0]
			self.cur_accelerateur_label.text = ev.EventToString(int(gl.conf[0][0][2][0][1]))
			self.cur_frein_label.text = ev.EventToString(int(gl.conf[0][0][2][1][1]))
			self.cur_droite_label.text = ev.EventToString(int(gl.conf[0][0][2][2][1]))
			self.cur_gauche_label.text = ev.EventToString(int(gl.conf[0][0][2][3][1]))
			self.cur_freinMain_label.text = ev.EventToString(int(gl.conf[0][0][2][4][1]))
			self.cur_nitro_label.text = ev.EventToString(int(gl.conf[0][0][2][5][1]))
			self.cur_passerVitesse_label.text = ev.EventToString(int(gl.conf[0][0][2][6][1]))
			self.cur_retrograder_label.text = ev.EventToString(int(gl.conf[0][0][2][7][1]))
			self.cur_upcam_label.text = ev.EventToString(int(gl.conf[0][0][2][8][1]))

	def leftjoueur(self, widget):
		if self.joueur_label.text == gl.configurablePlayers[0]:
			self.joueur_label.text = gl.configurablePlayers[3]
			self.cur_accelerateur_label.text = ev.EventToString(int(gl.conf[0][3][2][0][1]))
			self.cur_frein_label.text = ev.EventToString(int(gl.conf[0][3][2][1][1]))
			self.cur_droite_label.text = ev.EventToString(int(gl.conf[0][3][2][2][1]))
			self.cur_gauche_label.text = ev.EventToString(int(gl.conf[0][3][2][3][1]))
			self.cur_freinMain_label.text = ev.EventToString(int(gl.conf[0][3][2][4][1]))
			self.cur_nitro_label.text = ev.EventToString(int(gl.conf[0][3][2][5][1]))
			self.cur_passerVitesse_label.text = ev.EventToString(int(gl.conf[0][3][2][6][1]))
			self.cur_retrograder_label.text = ev.EventToString(int(gl.conf[0][3][2][7][1]))
			self.cur_upcam_label.text = ev.EventToString(int(gl.conf[0][3][2][8][1]))

		elif self.joueur_label.text == gl.configurablePlayers[1]:
			self.joueur_label.text = gl.configurablePlayers[0]
			self.cur_accelerateur_label.text = ev.EventToString(int(gl.conf[0][0][2][0][1]))
			self.cur_frein_label.text = ev.EventToString(int(gl.conf[0][0][2][1][1]))
			self.cur_droite_label.text = ev.EventToString(int(gl.conf[0][0][2][2][1]))
			self.cur_gauche_label.text = ev.EventToString(int(gl.conf[0][0][2][3][1]))
			self.cur_freinMain_label.text = ev.EventToString(int(gl.conf[0][0][2][4][1]))
			self.cur_nitro_label.text = ev.EventToString(int(gl.conf[0][0][2][5][1]))
			self.cur_passerVitesse_label.text = ev.EventToString(int(gl.conf[0][0][2][6][1]))
			self.cur_retrograder_label.text = ev.EventToString(int(gl.conf[0][0][2][7][1]))
			self.cur_upcam_label.text = ev.EventToString(int(gl.conf[0][0][2][8][1]))

		elif self.joueur_label.text == gl.configurablePlayers[2]:
			self.joueur_label.text = gl.configurablePlayers[1]
			self.cur_accelerateur_label.text = ev.EventToString(int(gl.conf[0][1][2][0][1]))
			self.cur_frein_label.text = ev.EventToString(int(gl.conf[0][1][2][1][1]))
			self.cur_droite_label.text = ev.EventToString(int(gl.conf[0][1][2][2][1]))
			self.cur_gauche_label.text = ev.EventToString(int(gl.conf[0][1][2][3][1]))
			self.cur_freinMain_label.text = ev.EventToString(int(gl.conf[0][1][2][4][1]))
			self.cur_nitro_label.text = ev.EventToString(int(gl.conf[0][1][2][5][1]))
			self.cur_passerVitesse_label.text = ev.EventToString(int(gl.conf[0][1][2][6][1]))
			self.cur_retrograder_label.text = ev.EventToString(int(gl.conf[0][1][2][7][1]))
			self.cur_upcam_label.text = ev.EventToString(int(gl.conf[0][1][2][8][1]))

		elif self.joueur_label.text == gl.configurablePlayers[3]:
			self.joueur_label.text = gl.configurablePlayers[2]
			self.cur_accelerateur_label.text = ev.EventToString(int(gl.conf[0][2][2][0][1]))
			self.cur_frein_label.text = ev.EventToString(int(gl.conf[0][2][2][1][1]))
			self.cur_droite_label.text = ev.EventToString(int(gl.conf[0][2][2][2][1]))
			self.cur_gauche_label.text = ev.EventToString(int(gl.conf[0][2][2][3][1]))
			self.cur_freinMain_label.text = ev.EventToString(int(gl.conf[0][2][2][4][1]))
			self.cur_nitro_label.text = ev.EventToString(int(gl.conf[0][2][2][5][1]))
			self.cur_passerVitesse_label.text = ev.EventToString(int(gl.conf[0][2][2][6][1]))
			self.cur_retrograder_label.text = ev.EventToString(int(gl.conf[0][2][2][7][1]))
			self.cur_upcam_label.text = ev.EventToString(int(gl.conf[0][2][2][8][1]))


	def ModifierAccelerateur(self, widget):
		if self.cur_accelerateur_label.state == 0:
			self.cur_accelerateur_label.color = 0.95,0.23,1.0,1
			self.cur_accelerateur_label.state = 1
			self.cur_respawn_label.color = self.cur_upcam_label.color = self.cur_retrograder_label.color = self.cur_passerVitesse_label.color = self.cur_nitro_label.color = self.cur_freinMain_label.color = self.cur_gauche_label.color = self.cur_droite_label.color = self.cur_frein_label.color = 0.95,0.23,0.0,1
			self.cur_respawn_label.state = self.cur_upcam_label.state = self.cur_retrograder_label.state = self.cur_passerVitesse_label.state = self.cur_nitro_label.state = self.cur_freinMain_label.state = self.cur_frein_label.state = self.cur_droite_label.state = self.cur_frein_label.state = 0

		elif self.cur_accelerateur_label.state == 1:
			self.cur_accelerateur_label.color = 0.95,0.23,0.0,1
			self.cur_accelerateur_label.state = 0

	def Modifierfrein(self, widget):
		if self.cur_frein_label.state == 0:
			self.cur_frein_label.color = 0.95,0.23,1.0,1
			self.cur_frein_label.state = 1
			self.cur_respawn_label.color = self.cur_upcam_label.color = self.cur_retrograder_label.color = self.cur_passerVitesse_label.color = self.cur_nitro_label.color = self.cur_freinMain_label.color = self.cur_gauche_label.color = self.cur_droite_label.color = self.cur_accelerateur_label.color = 0.95,0.23,0.0,1
			self.cur_respawn_label.state = self.cur_upcam_label.state = self.cur_retrograder_label.state = self.cur_passerVitesse_label.state = self.cur_nitro_label.state = self.cur_freinMain_label.state = self.cur_gauche_label.state = self.cur_droite_label.state = self.cur_accelerateur_label.state = 0

		elif self.cur_frein_label.state == 1:
			self.cur_frein_label.color = 0.95,0.23,0.0,1
			self.cur_frein_label.state = 0

	def Modifierdroite(self, widget):
		if self.cur_droite_label.state == 0:
			self.cur_droite_label.color = 0.95,0.23,1.0,1
			self.cur_droite_label.state = 1
			self.cur_respawn_label.color = self.cur_upcam_label.color = self.cur_retrograder_label.color = self.cur_passerVitesse_label.color = self.cur_nitro_label.color = self.cur_freinMain_label.color = self.cur_gauche_label.color = self.cur_frein_label.color = self.cur_accelerateur_label.color = 0.95,0.23,0.0,1
			self.cur_respawn_label.state = self.cur_upcam_label.state = self.cur_retrograder_label.state = self.cur_passerVitesse_label.state = self.cur_nitro_label.state = self.cur_freinMain_label.state = self.cur_frein_label.state = self.cur_frein_label.state = self.cur_accelerateur_label.state = 0

		elif self.cur_droite_label.state == 1:
			self.cur_droite_label.color = 0.95,0.23,0.0,1
			self.cur_droite_label.state = 0

	def Modifiergauche(self, widget):
		if self.cur_gauche_label.state == 0:
			self.cur_gauche_label.color = 0.95,0.23,1.0,1
			self.cur_gauche_label.state = 1
			self.cur_respawn_label.color = self.cur_upcam_label.color = self.cur_retrograder_label.color = self.cur_passerVitesse_label.color = self.cur_nitro_label.color = self.cur_freinMain_label.color = self.cur_droite_label.color = self.cur_frein_label.color = self.cur_accelerateur_label.color = 0.95,0.23,0.0,1
			self.cur_respawn_label.state = self.cur_upcam_label.state = self.cur_retrograder_label.state = self.cur_passerVitesse_label.state = self.cur_nitro_label.state = self.cur_freinMain_label.state = self.cur_droite_label.state = self.cur_frein_label.state = self.cur_accelerateur_label.state = 0

		elif self.cur_gauche_label.state == 1:
			self.cur_gauche_label.color = 0.95,0.23,0.0,1
			self.cur_gauche_label.state = 0

	def ModifierfreinMain(self, widget):
		if self.cur_freinMain_label.state == 0:
			self.cur_freinMain_label.color = 0.95,0.23,1.0,1
			self.cur_freinMain_label.state = 1
			self.cur_respawn_label.color = self.cur_upcam_label.color = self.cur_retrograder_label.color = self.cur_passerVitesse_label.color = self.cur_nitro_label.color = self.cur_gauche_label.color = self.cur_droite_label.color = self.cur_frein_label.color = self.cur_accelerateur_label.color = 0.95,0.23,0.0,1
			self.cur_respawn_label.state = self.cur_upcam_label.state = self.cur_retrograder_label.state = self.cur_passerVitesse_label.state = self.cur_nitro_label.state = self.cur_gauche_label.state = self.cur_droite_label.state = self.cur_frein_label.state = self.cur_accelerateur_label.state = 0

		elif self.cur_freinMain_label.state == 1:
			self.cur_freinMain_label.color = 0.95,0.23,0.0,1
			self.cur_freinMain_label.state = 0

	def Modifiernitro(self, widget):
		if self.cur_nitro_label.state == 0:
			self.cur_nitro_label.color = 0.95,0.23,1.0,1
			self.cur_nitro_label.state = 1
			self.cur_respawn_label.color = self.cur_upcam_label.color = self.cur_retrograder_label.color = self.cur_passerVitesse_label.color = self.cur_freinMain_label.color = self.cur_gauche_label.color = self.cur_droite_label.color = self.cur_frein_label.color = self.cur_accelerateur_label.color = 0.95,0.23,0.0,1
			self.cur_respawn_label.state = self.cur_upcam_label.state = self.cur_retrograder_label.state = self.cur_passerVitesse_label.state = self.cur_freinMain_label.state = self.cur_gauche_label.state = self.cur_droite_label.state = self.cur_frein_label.state = self.cur_accelerateur_label.state = 0

		elif self.cur_nitro_label.state == 1:
			self.cur_nitro_label.color = 0.95,0.23,0.0,1
			self.cur_nitro_label.state = 0

	def ModifierpasserVitesse(self, widget):
		if self.cur_passerVitesse_label.state == 0:
			self.cur_passerVitesse_label.color = 0.95,0.23,1.0,1
			self.cur_passerVitesse_label.state = 1
			self.cur_respawn_label.color = self.cur_upcam_label.color = self.cur_retrograder_label.color = self.cur_nitro_label.color = self.cur_freinMain_label.color = self.cur_gauche_label.color = self.cur_droite_label.color = self.cur_frein_label.color = self.cur_accelerateur_label.color = 0.95,0.23,0.0,1
			self.cur_respawn_label.state = self.cur_upcam_label.state = self.cur_retrograder_label.state = self.cur_nitro_label.state = self.cur_freinMain_label.state = self.cur_gauche_label.state = self.cur_droite_label.state = self.cur_frein_label.state = self.cur_accelerateur_label.state = 0

		elif self.cur_passerVitesse_label.state == 1:
			self.cur_passerVitesse_label.color = 0.95,0.23,0.0,1
			self.cur_passerVitesse_label.state = 0

	def Modifierretrograder(self, widget):
		if self.cur_retrograder_label.state == 0:
			self.cur_retrograder_label.color = 0.95,0.23,1.0,1
			self.cur_retrograder_label.state = 1
			self.cur_respawn_label.color = self.cur_upcam_label.color = self.cur_passerVitesse_label.color = self.cur_nitro_label.color = self.cur_freinMain_label.color = self.cur_gauche_label.color = self.cur_droite_label.color = self.cur_frein_label.color = self.cur_accelerateur_label.color = 0.95,0.23,0.0,1
			self.cur_respawn_label.state = self.cur_upcam_label.state = self.cur_passerVitesse_label.state = self.cur_nitro_label.state = self.cur_freinMain_label.state = self.cur_gauche_label.state = self.cur_droite_label.state = self.cur_frein_label.state = self.cur_accelerateur_label.state = 0

		elif self.cur_retrograder_label.state == 1:
			self.cur_retrograder_label.color = 0.95,0.23,0.0,1
			self.cur_retrograder_label.state = 0

	def Modifierupcam(self, widget):
		if self.cur_upcam_label.state == 0:
			self.cur_upcam_label.color = 0.95,0.23,1.0,1
			self.cur_upcam_label.state = 1
			self.cur_respawn_label.color = self.cur_retrograder_label.color = self.cur_passerVitesse_label.color = self.cur_nitro_label.color = self.cur_freinMain_label.color = self.cur_gauche_label.color = self.cur_droite_label.color = self.cur_frein_label.color = self.cur_accelerateur_label.color = 0.95,0.23,0.0,1
			self.cur_respawn_label.state = self.cur_retrograder_label.state = self.cur_passerVitesse_label.state = self.cur_nitro_label.state = self.cur_freinMain_label.state = self.cur_gauche_label.state = self.cur_droite_label.state = self.cur_frein_label.state = self.cur_accelerateur_label.state = 0

		elif self.cur_upcam_label.state == 1:
			self.cur_upcam_label.color = 0.95,0.23,0.0,1
			self.cur_upcam_label.state = 0

	def Modifierrespawn(self, widget):
		if self.cur_respawn_label.state == 0:
			self.cur_respawn_label.color = 0.95,0.23,1.0,1
			self.cur_respawn_label.state = 1
			self.cur_upcam_label.color = self.cur_retrograder_label.color = self.cur_passerVitesse_label.color = self.cur_nitro_label.color = self.cur_freinMain_label.color = self.cur_gauche_label.color = self.cur_droite_label.color = self.cur_frein_label.color = self.cur_accelerateur_label.color = 0.95,0.23,0.0,1
			self.cur_upcam_label.state = self.cur_retrograder_label.state = self.cur_passerVitesse_label.state = self.cur_nitro_label.state = self.cur_freinMain_label.state = self.cur_gauche_label.state = self.cur_droite_label.state = self.cur_frein_label.state = self.cur_accelerateur_label.state = 0

		elif self.cur_upcam_label.state == 1:
			self.cur_respawn_label.color = 0.95,0.23,0.0,1
			self.cur_respawn_label.state = 0

	def detruire(self) :
		"""Détruit les widgets"""
		self.frame.parent._remove_widget(self.frame)


	def main(self) :
		"""Refresh des events et de l'affichage"""
		BaseGui.main(self)

class MenuVoitureMultijoueursGui(BaseGui):
	"""
	Gui pour le choix du nom des joueurs
	"""


	def __init__(self, parent):

		# initialiation des variables pour les groupe de boutons en mode 3 et 4 joueurs
		groupeHautGauche = False
		groupeHautDroit = False
		groupeBasGauche = False
		groupeBasDroit = False
		# Initiate the system
		BaseGui.__init__(self, gl.skin)

		# Fond
		self.frame = bgui.Frame(parent, 'cadre', size=[1, 1], pos=[0, 0],
			sub_theme="Invisible", options =  bgui.BGUI_CENTERED | bgui.BGUI_DEFAULT)

		if gl.dispPlayers[0] == 1:
	#############bouton flecheGJ1############################
			self.flecheGJ1_button = bgui.ImageButton(self.frame, 'flecheGJ1', sub_theme='selFlecheG', size=[0.04, 0.26], pos=[0.32, 0.72])

			# Setup an on_click callback
			#self.flecheGJ1_button.on_click = self.leftcar

	#############bouton flecheJ1############################
			self.flecheJ1_button = bgui.ImageButton(self.frame, 'flecheJ1', sub_theme='selFleche', size=[0.04, 0.26], pos=[0.64, 0.72])

			# Setup an on_click callback
			#self.flecheJ1_button.on_click = self.rightcar

	#############bouton flecheGJ1Roue############################
			self.flecheGJ2Roue_button = bgui.ImageButton(self.frame, 'flecheGRoueJ1', sub_theme='selFlecheG', size=[0.04, 0.18], pos=[0.32, 0.52])

			# Setup an on_click callback
			#self.flecheGJ1Roue_button.on_click = self.leftwheels

	#############bouton flecheJ1Roue############################
			self.flecheJ1Roue_button = bgui.ImageButton(self.frame, 'flecheRoueJ1', sub_theme='selFleche', size=[0.04, 0.18], pos=[0.64, 0.52])

			# Setup an on_click callback
			#self.flecheJ1Roue_button.on_click = self.rightwheels

	#############bouton flecheGJ2############################
			self.flecheGJ2_button = bgui.ImageButton(self.frame, 'flecheGJ2', sub_theme='selFlecheG', size=[0.04, 0.26], pos=[0.32, 0.22])

			# Setup an on_click callback
			#self.flecheGJ2_button.on_click = self.leftcar

	#############bouton flecheJ2############################
			self.flecheJ2_button = bgui.ImageButton(self.frame, 'flecheJ2', sub_theme='selFleche', size=[0.04, 0.26], pos=[0.64, 0.22])

			# Setup an on_click callback
			#self.flecheJ2_button.on_click = self.rightcar

	#############bouton flecheGJ2Roue############################
			self.flecheGJ2Roue_button = bgui.ImageButton(self.frame, 'flecheGRoueJ2', sub_theme='selFlecheG', size=[0.04, 0.18], pos=[0.32, 0.02])

			# Setup an on_click callback
			#self.flecheGJ1Roue_button.on_click = self.leftwheels
	#############bouton flecheJ2Roue############################
			self.flecheJ2Roue_button = bgui.ImageButton(self.frame, 'flecheRoueJ2', sub_theme='selFleche', size=[0.04, 0.18], pos=[0.64, 0.02])

			# Setup an on_click callback
			#self.flecheJ2Roue_button.on_click = self.rightwheels

		if gl.dispPlayers[0] == 2:
	#############bouton flecheGJ1############################
			self.flecheGJ1_button = bgui.ImageButton(self.frame, 'flecheGJ1', sub_theme='selFlecheG', size=[0.04, 0.26], pos=[0.06, 0.54])

			# Setup an on_click callback
			#self.flecheGJ1_button.on_click = self.leftcar

	#############bouton flecheJ1############################
			self.flecheJ1_button = bgui.ImageButton(self.frame, 'flecheJ1', sub_theme='selFleche', size=[0.04, 0.26], pos=[0.4, 0.54])

			# Setup an on_click callback
			#self.flecheJ1_button.on_click = self.rightcar

	#############bouton flecheGJ1Roue############################
			self.flecheGJ2Roue_button = bgui.ImageButton(self.frame, 'flecheGRoueJ1', sub_theme='selFlecheG', size=[0.04, 0.18], pos=[0.06, 0.32])

			# Setup an on_click callback
			#self.flecheGJ1Roue_button.on_click = self.leftwheels

	#############bouton flecheJ1Roue############################
			self.flecheJ1Roue_button = bgui.ImageButton(self.frame, 'flecheRoueJ1', sub_theme='selFleche', size=[0.04, 0.18], pos=[0.4, 0.32])

			# Setup an on_click callback
			#self.flecheJ1Roue_button.on_click = self.rightwheels

	#############bouton flecheGJ2############################
			self.flecheGJ2_button = bgui.ImageButton(self.frame, 'flecheGJ2', sub_theme='selFlecheG', size=[0.04, 0.26], pos=[0.56, 0.54])

			# Setup an on_click callback
			#self.flecheGJ2_button.on_click = self.leftcar

	#############bouton flecheJ2############################
			self.flecheJ2_button = bgui.ImageButton(self.frame, 'flecheJ2', sub_theme='selFleche', size=[0.04, 0.26], pos=[0.9, 0.54])

			# Setup an on_click callback
			#self.flecheJ2_button.on_click = self.rightcar

	#############bouton flecheGJ2Roue############################
			self.flecheGJ2Roue_button = bgui.ImageButton(self.frame, 'flecheGRoueJ2', sub_theme='selFlecheG', size=[0.04, 0.18], pos=[0.56, 0.32])

			# Setup an on_click callback
			#self.flecheGJ1Roue_button.on_click = self.leftwheels
	#############bouton flecheJ2Roue############################
			self.flecheJ2Roue_button = bgui.ImageButton(self.frame, 'flecheRoueJ2', sub_theme='selFleche', size=[0.04, 0.18], pos=[0.9, 0.32])

			# Setup an on_click callback
			#self.flecheJ2Roue_button.on_click = self.rightwheels

		if gl.dispPlayers[0] == 3:
			groupeHautGauche = groupeHautDroit = groupeBasGauche = groupeBasDroit = True

		if gl.dispPlayers[0] == 4:
			groupeHautDroit = groupeBasGauche = groupeBasDroit = True

		if gl.dispPlayers[0] == 5:
			groupeHautGauche = groupeBasGauche = groupeBasDroit = True

		if gl.dispPlayers[0] == 6:
			groupeHautGauche = groupeHautDroit = groupeBasGauche = True

		if gl.dispPlayers[0] == 7:
			groupeHautGauche = groupeHautDroit = groupeBasDroit = True

		if 	groupeHautGauche == True:
	#############bouton flecheGJ1############################
			self.flecheGJ1_button = bgui.ImageButton(self.frame, 'flecheGJ1', sub_theme='selFlecheG', size=[0.04, 0.26], pos=[0.06, 0.72])

			# Setup an on_click callback
			#self.flecheGJ1_button.on_click = self.leftcar

	#############bouton flecheJ1############################
			self.flecheJ1_button = bgui.ImageButton(self.frame, 'flecheJ1', sub_theme='selFleche', size=[0.04, 0.26], pos=[0.4, 0.72])

			# Setup an on_click callback
			#self.flecheJ1_button.on_click = self.rightcar

	#############bouton flecheGJ1Roue############################
			self.flecheGJ1Roue_button = bgui.ImageButton(self.frame, 'flecheGRoueJ1', sub_theme='selFlecheG', size=[0.04, 0.18], pos=[0.06, 0.52])

			# Setup an on_click callback
			#self.flecheGJ1Roue_button.on_click = self.leftwheels

	#############bouton flecheJ1Roue############################
			self.flecheJ1Roue_button = bgui.ImageButton(self.frame, 'flecheRoueJ1', sub_theme='selFleche', size=[0.04, 0.18], pos=[0.4, 0.52])

			# Setup an on_click callback
			#self.flecheJ1Roue_button.on_click = self.rightwheels


		if 	groupeHautDroit == True:
	#############bouton flecheGJ2############################
			self.flecheGJ2_button = bgui.ImageButton(self.frame, 'flecheGJ2', sub_theme='selFlecheG', size=[0.04, 0.26], pos=[0.56, 0.72])

			# Setup an on_click callback
			#self.flecheGJ2_button.on_click = self.leftcar

	#############bouton flecheJ2############################
			self.flecheJ2_button = bgui.ImageButton(self.frame, 'flecheJ2', sub_theme='selFleche', size=[0.04, 0.26], pos=[0.9, 0.72])

			# Setup an on_click callback
			#self.flecheJ2_button.on_click = self.rightcar

	#############bouton flecheGJ2Roue############################
			self.flecheGJ2Roue_button = bgui.ImageButton(self.frame, 'flecheGRoueJ2', sub_theme='selFlecheG', size=[0.04, 0.18], pos=[0.56, 0.52])

			# Setup an on_click callback
			#self.flecheGJ2Roue_button.on_click = self.leftwheels

	#############bouton flecheJ2Roue############################
			self.flecheJ2Roue_button = bgui.ImageButton(self.frame, 'flecheRoueJ2', sub_theme='selFleche', size=[0.04, 0.18], pos=[0.9, 0.52])

			# Setup an on_click callback
			#self.flecheJ2Roue_button.on_click = self.rightwheels

		if 	groupeBasGauche == True:
	#############bouton flecheGJ3############################
			self.flecheGJ3_button = bgui.ImageButton(self.frame, 'flecheGJ3', sub_theme='selFlecheG', size=[0.04, 0.26], pos=[0.06, 0.22])

			# Setup an on_click callback
			#self.flecheGJ3_button.on_click = self.leftcar

	#############bouton flecheJ3############################
			self.flecheJ3_button = bgui.ImageButton(self.frame, 'flecheJ3', sub_theme='selFleche', size=[0.04, 0.26], pos=[0.4, 0.22])

			# Setup an on_click callback
			#self.flecheJ3_button.on_click = self.rightcar

	#############bouton flecheGJ3Roue############################
			self.flecheGJ3Roue_button = bgui.ImageButton(self.frame, 'flecheGRoueJ3', sub_theme='selFlecheG', size=[0.04, 0.18], pos=[0.06, 0.02])

			# Setup an on_click callback
			#self.flecheGJ3Roue_button.on_click = self.leftwheels

	#############bouton flecheJ3Roue############################
			self.flecheJ3Roue_button = bgui.ImageButton(self.frame, 'flecheRoueJ3', sub_theme='selFleche', size=[0.04, 0.18], pos=[0.4, 0.02])

			# Setup an on_click callback
			#self.flecheJ3Roue_button.on_click = self.rightwheels

		if 	groupeBasDroit == True:
	#############bouton flecheGJ4############################
			self.flecheGJ4_button = bgui.ImageButton(self.frame, 'flecheGJ4', sub_theme='selFlecheG', size=[0.04, 0.26], pos=[0.56, 0.22])

			# Setup an on_click callback
			#self.flecheGJ4_button.on_click = self.leftcar

	#############bouton flecheJ4############################
			self.flecheJ4_button = bgui.ImageButton(self.frame, 'flecheJ4', sub_theme='selFleche', size=[0.04, 0.26], pos=[0.9, 0.22])

			# Setup an on_click callback
			#self.flecheJ4_button.on_click = self.rightcar

	#############bouton flecheGJ4Roue############################
			self.flecheGJ4Roue_button = bgui.ImageButton(self.frame, 'flecheGRoueJ4', sub_theme='selFlecheG', size=[0.04, 0.18], pos=[0.56, 0.02])

			# Setup an on_click callback
			#self.flecheGJ4Roue_button.on_click = self.leftwheels

	#############bouton flecheJ4Roue############################
			self.flecheJ4Roue_button = bgui.ImageButton(self.frame, 'flecheRoueJ4', sub_theme='selFleche', size=[0.04, 0.18], pos=[0.9, 0.02])

			# Setup an on_click callback
			#self.flecheJ4Roue_button.on_click = self.rightwheels

	#############bouton valider############################
		self.valider_button = bgui.ImageButton(self.frame, 'valider', sub_theme='menu', size=[0.10, 0.05], pos=[0.45, 0.51])
		self.valider_label = bgui.Label(self.valider_button, 'validertext', text="VALIDER", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

	def detruire(self) :
		"""Détruit les widgets"""
		self.frame.parent._remove_widget(self.frame)


	def main(self) :
		"""Refresh des events et de l'affichage"""
		BaseGui.main(self)

class MenuOptionsSon(BaseGui):
	"""
	Gui pour
	"""
	def __init__(self, parent):
		# Initiate the system
		BaseGui.__init__(self, gl.skin)

		# Cadre général
		self.frame = bgui.Frame(parent, 'frame', size=[1, 1], pos=[0, 0],
			sub_theme="Invisible", options =  bgui.BGUI_CENTERED | bgui.BGUI_DEFAULT)
		

		self.radio_label = bgui.Label(self.frame, 'radio', text="radio par défaut:", pt_size=38, pos=[0.05, 0.90])
		
		#fleche radio gauche
		self.flecheRadioGauche_button = bgui.ImageButton(self.frame, 'flecheRadioGauche', sub_theme='selFlecheG', size=[0.04, 0.06], pos=[0.04, 0.80])
		
		# Setup an on_click callback
		self.flecheRadioGauche_button.on_click = self.flecheRadioGauche
		
		# affichage de la radio
		self.radio_frame = bgui.Frame(self.frame, 'fond', sub_theme='fondDigit', size=[0.20, 0.06], pos=[0.08, 0.80])
		self.radio_name_label = bgui.Label(self.radio_frame, 'radio_name_label', text=gl.sound[2], pt_size=35, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		#fleche radio droite

		self.flecheRadioDroite_button = bgui.ImageButton(self.frame, 'flecheRadioDroite', sub_theme='selFleche', size=[0.04, 0.06], pos=[0.28, 0.80])
		
		# Setup an on_click callback
		self.flecheRadioDroite_button.on_click = self.flecheRadioDroite		
		

		
#############bouton saveAudio############################
		self.saveAudio_button = bgui.ImageButton(self.frame, 'saveAudio', sub_theme='menu', size=[0.24, 0.08], pos=[0.45, 0.08])
		self.saveAudio_label = bgui.Label(self.saveAudio_button, 'saveAudioL', text="SAUVEGARDER", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

				# Setup an on_click callback
		self.saveAudio_button.on_click = self.saveRadio

#############bouton playAudio############################
		self.playAudio_button = bgui.ImageButton(self.frame, 'playAudio', sub_theme='menu', size=[0.14, 0.08], pos=[0.09, 0.38])
		self.playAudio_label = bgui.Label(self.playAudio_button, 'playAudioL', text="PLAY", pt_size=24, options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

				# Setup an on_click callback
		self.playAudio_button.on_click = self.playRadio

		# Autres attributs
		self.action = None

	def flecheRadioGauche(self, widget):
		gl.listeRadio.rotate(1)
		gl.sound = gl.listeRadio[0]
		self.radio_name_label.text = gl.sound

	def flecheRadioDroite(self, widget):
		gl.listeRadio.rotate(-1)
		gl.sound = gl.listeRadio[0]
		self.radio_name_label.text = gl.sound


	def playRadio(self, widjet):
		if self.playAudio_label.text == "PLAY":
			self.playAudio_label.text = "STOP"
		else:
			self.playAudio_label.text = "PLAY"

	def saveRadio(self, widjet):
		confParser.saveConf()

	def detruire(self) :
		"""Détruit les widgets"""
		self.frame.parent._remove_widget(self.frame)

	def main(self) :
		"""Refresh des events et de l'affichage"""
		BaseGui.main(self)
