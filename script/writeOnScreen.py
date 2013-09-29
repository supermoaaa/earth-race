from bge import logic as gl
from bge import render as render
import bgl
import blf
from logs import log

class bflFactory:
	def __init__( self, obPos, cam ):
		self.manager = bflManager()
		self.text = Text( obPos, self.manager.getScreenInfo(), cam)
		self.manager.addText(self.text)

	def write( self, newText ):
		self.text.text = newText

class bflManager:
	def __init__( self ):
		if not hasattr(bflManager,'__instance'):
			bflManager.__instance = True

			scene = gl.getCurrentScene()

			#~ self.camera = scene.active_camera
			#~ self.camera = cam

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
			blf.position( self.fontid, text.x, text.y, 1 )
			blf.size(self.fontid, 50, 72)
			blf.draw( self.fontid, text.text )
			log("debug","x="+str(text.x)+" y="+str(text.y))

class Text:
	def __init__( self, obPos, screenInfo, cam ):
		cam = gl.getCurrentScene().active_camera
		log("debug", "screenInfo x="+str(screenInfo[0])+" y="+str(screenInfo[1])+" cam="+str(cam))
		log("debug", "pos x="+str(cam.getScreenPosition(obPos)[0])+" y="+str(cam.getScreenPosition(obPos)[1]))
		self.x = screenInfo[0] * (cam.getScreenPosition(obPos)[0]/1.57)
		self.y = screenInfo[1] * (1-cam.getScreenPosition(obPos)[1]/1.11)
		self.text = ''
