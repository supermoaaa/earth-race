# -- coding: utf-8 --

import bgui
import webbrowser
import confParser as conf
#import scores

from bge import logic as gl
from bge import render as rd
from bge import events as ev


class StatSys(bgui.System):
	"""
	A subclass to handle our game specific gui
	"""

	def quitter(self, quitter_button):
		gl.endGame()

	def retour(self, retour_button):
		for lib in gl.LibList():
			gl.LibFree(lib)
		with open('menustat', 'w') as f:
			f.write(gl.mapName)
		f.closed
		gl.restartGame()

	def relancer(self, relancer_button):
		for lib in gl.LibList():
			gl.LibFree(lib)
		scene = gl.getCurrentScene()
		scene.replace('game')

	def credits(self, credits_button):
		webbrowser.open('http://earth-race.fr.nf/index.html', new=2, autoraise=True)

	def __init__(self):
		# Initialize the system
		bgui.System.__init__(self, 'themes/default')


		self.frame = bgui.Frame(self, 'frame', aspect=(4/3),
					options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
		self.frame.visible = False
#--------------frame principale----------------#
#
#
#
		self.main_stat = bgui.Frame(self, 'main_stat', border=1, size=[1.0, 1.0],
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)
		self.main_stat.visible = True

		self.main_stat.img = bgui.Image(self.main_stat, 'menuItems/menu.jpg', size=[1.0, 1.0],
			options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX|bgui.BGUI_CACHE)

#############bouton quitter############################
		self.quitter_button = bgui.ImageButton(self.main_stat, 'quitter', sub_theme='menu',
				size=[0.24, 0.08], pos=[0.75, 0.08])

		self.quitter_label = bgui.Label(self.quitter_button, 'quitter', text="QUITTER", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		# Setup an on_click callback
		self.quitter_button.on_click = self.quitter
#############bouton retour au menu############################
		self.retour_button = bgui.ImageButton(self.main_stat, 'retour', sub_theme='menu',
				size=[0.24, 0.08], pos=[0.75, 0.18])

		self.retour_label = bgui.Label(self.retour_button, 'retour', text="RETOUR AU MENU", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		# Setup an on_click callback
		self.retour_button.on_click = self.retour

#############bouton relancer############################
		self.relancer_button = bgui.ImageButton(self.main_stat, 'relancer', sub_theme='menu',
				size=[0.24, 0.08], pos=[0.75, 0.28])

		self.relancer_label = bgui.Label(self.relancer_button, 'relancer', text="RECOMMENCER", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		# Setup an on_click callback
		self.relancer_button.on_click = self.relancer

#############bouton credits############################
		self.credits_button = bgui.ImageButton(self.main_stat, 'credits', sub_theme='menu',
				size=[0.24, 0.08], pos=[0.75, 0.38])

		self.credits_label = bgui.Label(self.credits_button, 'credits', text="CREDITS", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		# Setup an on_click callback
		self.credits_button.on_click = self.credits

#--------------frame tableau----------------#
#
#
#
		self.tableau = bgui.Frame(self.main_stat, 'tableau', border=None, size=[0.64, 0.75], pos=[0.02, 0.04], sub_theme='stat',
				options=bgui.BGUI_DEFAULT)

		self.tableau.img = bgui.Image(self.tableau, 'menuItems/fondStat.png', size=[1.0, 1.0],
			options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX|bgui.BGUI_CACHE)


		# entete
		self.JoueurCol=bgui.Label(self.tableau, 'JoueurCol', text="JOUEUR", pt_size=24, pos=[0.12, 0.85])
		self.TempsCol=bgui.Label(self.tableau, 'TempsCol', text="TEMPS", pt_size=24, pos=[0.36, 0.85])
		self.ToursCol=bgui.Label(self.tableau, 'ToursCol', text="TOURS", pt_size=24, pos=[0.76, 0.85])
		
		# infos
		joueurListe = ''
		joueurTemps = ''
		joueurTours = ''
		for element in gl.scores.getLastScores():
			joueurListe += element[0] + '\n'
			joueurTemps += element[1] + '\n'
			joueurTours += str(element[2]) + '\n'
		
		self.JoueurListe = bgui.Label(self.tableau, 'JoueurListe', text = joueurListe, pt_size=24, pos=[0.12, 0.80])
		self.JoueurTemps = bgui.Label(self.tableau, 'JoueurTemps', text = joueurTemps, pt_size=24, pos=[0.36, 0.80])
		self.JoueurTours = bgui.Label(self.tableau, 'JoueurTours', text = joueurTours, pt_size=24, pos=[0.76, 0.80])



		# Create a keymap for keyboard input
		self.keymap = {getattr(ev, val): getattr(bgui, val) for val in dir(ev) if (val.endswith('KEY') or val.startswith('PAD')) and hasattr(bgui, val) }
		


		# Now setup the scene callback so we can draw
		gl.getCurrentScene().post_draw.append(self.render)

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
		gl.getCurrentScene().pre_draw = [self.render]

def main(cont):
	own = cont.owner

	if 'Stat' not in own:
		# Create our system and show the mouse
		own['Stat'] = StatSys()
		gl.mouse.visible = True
	else:
		own['Stat'].main()
