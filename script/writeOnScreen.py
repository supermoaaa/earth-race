from bge import logic as gl
from bge import render as render
import bgl
import blf
from logs import log


class bflFactory:
	def __init__(self, x, y, size, cam):
		self.fontid = blf.load(
				gl.expandPath('//themes/default/LiquidCrystal-Bold.otf'))
		self.manager = bflManager()
		self.text = Text(x, y, size, self.fontid, cam)
		self.manager.addText(self.text)

	def updateCam(self, cam):
		self.text.updateCam(cam)

	def write(self, newText):
		self.text.setText(newText)
		return self.text


class bflManager:
	_instance = None

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(bflManager, cls).__new__(cls, *args, **kwargs)
		return cls._instance

	def __init__(self):
		if not hasattr(self, 'texts'):
			scene = gl.getCurrentScene()

			self.height = render.getWindowHeight()
			self.width = render.getWindowWidth()
			log("debug", "screen height: {} width : {}".format(self.height, self.width))

			self.texts = []

			scene.post_draw = [self.writeAll]

			bflManager._inited = True

	def addText(self, text):
		self.texts.append(text)
		log('debug', 'bflManager : add Text')

	def getScreenInfo(self):
		return [self.width, self.height]

	def bglInit(self):
		bgl.glMatrixMode(bgl.GL_PROJECTION)
		bgl.glLoadIdentity()
		bgl.gluOrtho2D(0, self.width, 0, self.height)
		bgl.glMatrixMode(bgl.GL_MODELVIEW)
		bgl.glLoadIdentity()

	def writeAll(self):
		self.bglInit()
		log('debug', 'bflManager : nb Text' + str(len(self.texts)))
		for text in self.texts:
			blf.size(text.fontid, text.globalSizeX, text.globalSizeY)
			blf.position(text.fontid, text.globalCenteredX, text.globalCenteredY, 1)
			blf.draw(text.fontid, text.text)
		self.resetInstance()

	def resetInstance(self):
		log('debug', 'bflManager : reset instance')
		bflManager._instance = None


class Text:
	def __init__(self, x, y, size, fontid, cam):
		self.localX = x
		self.localY = y
		self.localSize = size
		self.text = ''
		self.fontid = fontid
		self.updateCam(cam)

	def updateCam(self, cam):
		if cam is not None:
			viewPort = cam.viewPort
		else:
			viewPort = [0, 0, render.getWindowHeight(), render.getWindowWidth()]
		screenX = viewPort[2] - viewPort[0]
		screenY = viewPort[3] - viewPort[1]
		self.globalSizeX = int(self.localSize * screenX)
		self.globalSizeY = int(self.localSize * screenY)
		self.globalX = viewPort[0] + self.localX * screenX
		self.globalY = viewPort[1] + self.localY * screenY
		self.globalCenteredX = self.globalX
		self.globalCenteredY = self.globalY

	def setText(self, text):
		self.text = text
		relativeX, relativeY = blf.dimensions(self.fontid, self.text)
		self.globalCenteredX = self.globalX - relativeX / 2
		self.globalCenteredY = self.globalY - relativeY / 2
