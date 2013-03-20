# -- coding: utf-8 --

import bgui
import bge

from bge import logic as gl
from bge import render as rd
from bge import events as ev


class StatSys(bgui.System):
	"""
	A subclass to handle our game specific gui
	"""

	### fonctions de retour a menu principal

	def retour(self, retour_button):
		for lib in gl.LibList():
			gl.LibFree(lib)
		scene = gl.getCurrentScene()
		scene.replace('menu')

	def relancer(self, relancer_button):
		for lib in gl.LibList():
			gl.LibFree(lib)
		scene = gl.getCurrentScene()
		scene.replace('game')

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

		self.main_stat.img = bgui.Image(self.main_stat, 'image', 'menuItems/menu.jpg', size=[1.0, 1.0],
			options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX|bgui.BGUI_CACHE)

#############bouton retour au menu############################
		self.retour_button = bgui.ImageButton(self.main_stat, 'retour', sub_theme='menu',
				size=[0.24, 0.08], pos=[0.75, 0.08])

		self.retour_label = bgui.Label(self.retour_button, 'retour', text="RETOUR AU MENU", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		# Setup an on_click callback
		self.retour_button.on_click = self.retour

#############bouton relancer############################
		self.relancer_button = bgui.ImageButton(self.main_stat, 'relancer', sub_theme='menu',
				size=[0.24, 0.08], pos=[0.75, 0.18])

		self.relancer_label = bgui.Label(self.relancer_button, 'relancer', text="RECOMMENCER", pt_size=24,
				options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERED)

		# Setup an on_click callback
		self.relancer_button.on_click = self.relancer
#--------------frame tableau----------------#
#
#
#
		self.tableau = bgui.Frame(self.main_stat, 'tableau', border=None, size=[0.64, 0.75], pos=[0.02, 0.04], sub_theme='stat',
				options=bgui.BGUI_DEFAULT)

		self.tableau.img = bgui.Image(self.tableau, 'imagetableau', 'menuItems/fondStat.png', size=[1.0, 1.0],
			options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX|bgui.BGUI_CACHE)

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

	if 'Stat' not in own:
		# Create our system and show the mouse
		own['Stat'] = StatSys()
		mouse.visible = True
	else:
		own['Stat'].main()