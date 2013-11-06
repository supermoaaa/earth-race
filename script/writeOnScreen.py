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
		self.text.setText(newText)

class bflManager:
	def __init__( self ):
		if not hasattr(bflManager,'__instance'):
			bflManager.__instance = True

			scene = gl.getCurrentScene()

			self.height = render.getWindowHeight()
			self.width = render.getWindowWidth()
			log("debug","screen height: {} width : {}".format(self.height, self.width))

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
			blf.size(self.fontid, text.globalSizeX, text.globalSizeY)
			blf.position( self.fontid, text.globalCenteredX, text.globalCenteredY, 1 )
			blf.draw( self.fontid, text.text )

class Text:
	def __init__( self, x, y, size, cam):
		self.localX = x
		self.localY = y
		self.localSize = size
		self.cam = cam
		viewPort = self.cam.viewPort
		screenX = (viewPort[2]-viewPort[0])
		screenY = (viewPort[3]-viewPort[1])
		self.globalSizeX = int(size*screenX)
		self.globalSizeY = int(size*screenY)
		self.globalX = viewPort[0]+x*screenX
		self.globalY = viewPort[1]+y*screenY
		self.globalCenteredX = self.globalX
		self.globalCenteredY = self.globalY
		self.text = ''

	def setText( self, text ):
		self.text = text
		relativeX, relativeY = blf.dimensions(0, self.text)
		self.globalCenteredX = self.globalX - relativeX/2
		self.globalCenteredY = self.globalY - relativeY/2
