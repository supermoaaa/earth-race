from bge import texture as VT
from bge import logic as gl
from bge import events as ev
from sys import path
import os
import bgl
import blf
from bge import render

path.append(gl.expandPath("//")+'script')
path.append(gl.expandPath("//")+'bgui')
os.chdir(gl.expandPath("//"))

import confParser
import logs
logs.initLogs()
cont = gl.getCurrentController()
scene = gl.getCurrentScene()
confParser.loadConf()
obj = cont.owner

def init():
	path.append(gl.expandPath("//")+'script')
	path.append(gl.expandPath("//")+'bgui')
	path.append(gl.expandPath("//"))
	os.chdir(gl.expandPath("//"))
	os.path.expanduser(gl.expandPath("//"))

	import logs
	logs.initLogs()
	

	listFiles = os.listdir(os.path.expanduser(gl.expandPath("//")))
	

	scene = gl.getCurrentScene()
	if "menustat" in listFiles:
		
		with open('menustat', 'r') as f:
			if f.read() == 'anneauDeTest':
				gl.menuStat = True
		f.closed

		os.remove('menustat')
		scene.replace('menu')
	# initialisation video 

	matID = VT.materialID(obj, 'MAvd')
	gl.video = VT.Texture(obj, matID)

	S1 = gl.expandPath("//menuItems/logo.avi")
	video_source = VT.VideoFFmpeg(S1)
	video_source.repeat = 1
	video_source.scale = True
	video_source.flip = True

	gl.video.source = video_source
	gl.video.source.play()
	
	# initialisation texte
	gl.font_id = blf.load(gl.expandPath('//abberancy.otf'))
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

	blf.position(gl.font_id, (width * 0.2), (height * 0.9), 0)
	blf.size(gl.font_id, 25, 72)
	bgl.glColor4f(0.2, 0.5, 1, 1)
	blf.draw(gl.font_id, "appuyer sur espace pour passer l\'intro")

def update():

	if hasattr(gl, 'video'):
		gl.video.refresh(True)
		if obj['time'] < 450:
			obj['time'] += 1
		else:
			scene.replace('menu')
	if gl.keyboard.events[ev.SPACEKEY] == 2:
		scene.replace('menu')