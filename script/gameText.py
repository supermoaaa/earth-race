# import game engine modules
from bge import render
from bge import logic
# import stand alone modules
import bgl
import blf


def init():

	logic.font_id = blf.load(logic.expandPath('//abberancy.otf'))

	# set the font drawing routine to run every frame
	scene = logic.getCurrentScene()
	scene.post_draw = [write]


def write():
	"""write on screen"""
	width = render.getWindowWidth()
	height = render.getWindowHeight()

	# OpenGL setup
	bgl.glMatrixMode(bgl.GL_PROJECTION)
	bgl.glLoadIdentity()
	bgl.gluOrtho2D(0, width, 0, height)
	bgl.glMatrixMode(bgl.GL_MODELVIEW)
	bgl.glLoadIdentity()


	blf.position(logic.font_id, (width * 0.2), (height * 0.9), 0)
	blf.size(logic.font_id, 25, 72)
	bgl.glColor4f(0.2, 0.5, 1, 1) 
	blf.draw(logic.font_id, "appuyer sur espace pour passer l\'intro")

