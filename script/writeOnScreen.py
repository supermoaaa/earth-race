from bge import logic as gl
from bge import render as render
import bgl
import blf
from logs import log

class bflFactory:
	def __init__( self, x, y, size, cam ):
		self.manager = bflManager()
		self.text = Text( x, y, size, cam )
		self.manager.addText(self.text)

	def write( self, newText ):
		self.text.text = newText

class bflManager:
	def __init__( self ):
		if not hasattr(bflManager,'__instance'):
			bflManager.__instance = True

			scene = gl.getCurrentScene()

			self.height = render.getWindowHeight()
			self.width = render.getWindowWidth()

			self.texts = []
			self.fontid = 0

			scene.post_draw = [self.writeAll]

	def addText( self, text ):
		self.texts.append(text)

	def getScreenInfo(self):
		return [ self.width, self.height ]

	def bglInit(self):
		bgl.glMatrixMode(bgl.GL_PROJECTION)
		bgl.glLoadIdentity()
		bgl.gluOrtho2D(0, self.width, 0, self.height)
		bgl.glMatrixMode(bgl.GL_MODELVIEW)
		bgl.glLoadIdentity()

	def writeAll(self):
		self.bglInit()
		for text in self.texts:
			blf.size(self.fontid, text.size, text.size)
			blf.position( self.fontid, text.globalX, text.globalY, 1 )
			blf.draw( self.fontid, text.text )

class Text:
	def __init__( self, x, y, size, cam):
		self.localX = x
		self.localY = y
		self.size = size
		self.cam = cam
		viewPort = self.cam.viewPort
		self.globalX = viewPort[0]+x*(viewPort[2]-viewPort[0])-(size/6)
		self.globalY = viewPort[1]+y*(viewPort[3]-viewPort[1])-(size/6)
		self.text = ''
