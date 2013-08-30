from bge import logic as gl
from bge import render as render
import bgl
import blf

class bflFactory():
	@staticmethod
	def write( text, obPos ):
		manager = bflManager()
		newText = Text( text, obPos, manager.getScreenInfo())
		manager.addText(newText)
		return newText

class bflManager():
	def __init__( self ):
		if not hasattr(bflManager,'__instance'):
			bflManager.__instance = True

			scene = gl.getCurrentScene()

			self.camera = scene.active_camera

			self.height = render.getWindowHeight()
			self.width = render.getWindowWidth()

			self.texts = []
			self.fontid = 0

			scene.post_draw = [self.writeAll]

	def addText( self, text ):
		self.texts.append(text)

	def getScreenInfo(self):
		return [ self.camera, self.width, self.height ]

	def bglInit(self):
		bgl.glMatrixMode(bgl.GL_PROJECTION)
		bgl.glLoadIdentity()
		bgl.gluOrtho2D(0, self.width, 0, self.height)
		bgl.glMatrixMode(bgl.GL_MODELVIEW)
		bgl.glLoadIdentity()

	def writeAll(self):
		self.bglInit()
		for text in self.texts:
			blf.position( self.fontid, text.x, text.y, 1 )
			blf.draw( self.fontid, text.text )

class Text():
	def __init__( self, text, obPos, screenInfo ):
		self.x = screenInfo[1] * screenInfo[0].getScreenPosition(obPos)[0]
		self.y = screenInfo[2] * (1.0-screenInfo[0].getScreenPosition(obPos)[1])
		self.setText(text)

	def setText( self, text ):
		self.text = text
