import aud
import os
from bge import logic as gl

def loadMusic():
	try:
		listElements = os.listdir(gl.music['Dir'])
	except:
		gl.music['Dir'] = gl.expandPath("//")+'music'
		listElements = os.listdir(gl.music['Dir'])
	gl.music['List'] = []
	for element in listElements:
		if not os.path.isdir(element):
			gl.music['List'].append(element)
	gl.music['Counter'] = 0
	
def play():
	if !gl.music.is_key('handle.status') or gl.music['handle.status'] != True:
		gl.music['Counter'] += 1
		if gl.music['Counter'] >= len(gl.music['List']):
			gl.music['Counter'] == 0
		factory = aud.Factory(gl.expandPath("//")+'music'+os.sep+gl.music['List'][gl.music['Counter']])
		gl.music['handle'].stop()
		device = aud.device()
		gl.music['handle'] = device.play(factory)
		gl.music['handle'].volume = gl.music['volume']

def setVolume(volume):
	gl.music['volume'] = volume
	gl.music['handle'].volume = volume

def stop():
	gl.music['handle'].stop()

def searchDirectory():
	musicDirs = [gl.expandPath("//")+'music']
	musicDirs = os.listdir(gl.expandPath("//")+'music')
	for element in musicDirs:
		if os.path.isdir(element):
			musicDirs.append(element)
	return(musicDirs)
