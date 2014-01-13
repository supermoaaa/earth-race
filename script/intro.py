from bge import texture as VT
from bge import logic as G
from bge import events as ev
cont = G.getCurrentController()
scene = G.getCurrentScene()

obj = cont.owner


def init():

	matID = VT.materialID(obj, 'MAvd')
	G.video = VT.Texture(obj, matID)

	S1 = G.expandPath("//menuItems/logo.avi")
	video_source = VT.VideoFFmpeg(S1)
	video_source.repeat = 1
	video_source.scale = True
	video_source.flip = True

	G.video.source = video_source
	G.video.source.play()


def update():

	if hasattr(G, 'video'):
		G.video.refresh(True)
		if obj['time'] < 450:
			obj['time'] += 1
		else:
			scene.replace('menu')
	if G.keyboard.events[ev.SPACEKEY] == 2:
		scene.replace('menu')