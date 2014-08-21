from bge import texture as VT
from bge import logic as gl
from bge import events as ev
import sys
import os
sys.path.append(gl.expandPath("//")+'script')
sys.path.append(gl.expandPath("//")+'bgui')
os.chdir(gl.expandPath("//"))

import logs
logs.initLogs()
cont = gl.getCurrentController()
scene = gl.getCurrentScene()

obj = cont.owner

def init():
	sys.path.append(gl.expandPath("//")+'script')
	sys.path.append(gl.expandPath("//")+'bgui')
	os.chdir(gl.expandPath("//"))

	import logs
	logs.initLogs()

	listFiles = os.listdir(os.path.expanduser(gl.expandPath("//")))


	if "menustat" in listFiles:
		scene = gl.getCurrentScene()
		with open('menustat', 'r') as f:
			if f.read() == 'anneauDeTest':
				gl.menuStat = True
		f.closed

		os.remove('menustat')
		scene.replace('menu')

def initVid():

	matID = VT.materialID(obj, 'MAvd')
	gl.video = VT.Texture(obj, matID)

	S1 = gl.expandPath("//menuItems/logo.avi")
	video_source = VT.VideoFFmpeg(S1)
	video_source.repeat = 1
	video_source.scale = True
	video_source.flip = True

	gl.video.source = video_source
	gl.video.source.play()


def update():

	if hasattr(gl, 'video'):
		gl.video.refresh(True)
		if obj['time'] < 450:
			obj['time'] += 1
		else:
			scene.replace('menu')
	if gl.keyboard.events[ev.SPACEKEY] == 2:
		scene.replace('menu')