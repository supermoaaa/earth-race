import aud
import threading
from logs import log
from bge import logic as gl
import os

class Sound(object):
	""" sound manager """

	def __init__ ( self, buffered=False, volume=False):
		""" Class initialiser """
		self.device = aud.device()
		self.buffered = buffered
		self.factory = None
		self.handle = None
		self.looped = False
		if volume is not False:
			self.volume = volume
		elif hasattr(gl, 'sound'):
			self.volume = gl.sound[0]
		else:
			self.volume = 1

	def load( self, soundPath):
		try:
			self.factory = aud.Factory(soundPath)
			if self.buffered:
				self.factory = aud.Factory.buffer(self.factory)
		except:
			log("error","impossible de trouver le fichier "+soundPath)

	def play(self):
		self.stop()
		if self.factory != None:
			self.handle = self.device.play(self.factory)
			self.handle.volume = self.volume
			self.handle.relative = True
			self.loop(self.looped)

	def stop(self):
		if self.handle != None:
			self.handle.stop()

	def setVolume( self, volume ):
		self.volume = volume
		if self.handle != None:
			self.handle.volume = volume

	def getVolume(self):
		return self.volume

	def location( self, location, velocity ):
		if self.handle != None:
			self.handle.location = location
			self.handle.velocity = velocity

	def getState( self ):
		if self.handle != None:
			return self.handle.status
		else:
			return None

	def setPitch( self, pitch ):
		if self.handle != None:
			if pitch<0:pitch=-pitch
			self.handle.pitch = pitch

	def loop( self, looped = True):
		self.looped = looped
		if self.handle != None:
			if looped:
				self.handle.loop_count = -1 #3 pour les tests, sinon -1
			else:
				self.handle.loop_count = 0

class Music:
	def __init__( self, playlist, volume=False ):
		self.player = Sound()
		self.playlist = playlist
		self.idPlayed = -1
		self.state = False
		if volume is not False:
			self.setVolume(volume)
		elif hasattr(gl, 'sound'):
			self.setVolume(gl.sound[1])

	def play( self ):
		if len(self.playlist) >= 1 and (self.player.getState()==0 or self.player.getState()==None) and self.state == False:
			self.state = True

	def step( self ):
		if (self.player.getState()==0 or self.player.getState()==None) and self.state:
			self.playNext()

	def playNext( self ):
		if len(self.playlist) >= 1 and self.state:
			self.state = False
			self.idPlayed+=1
			if len(self.playlist) <= self.idPlayed:
				self.idPlayed=0
			self.player.load(self.playlist[self.idPlayed])
			self.player.play()
			self.state = True

	def setVolume( self, volume ):
		self.player.setVolume(volume)

	def getVolume( self ):
		return self.player.getVolume()

	def stop( self ):
		self.player.stop()
		self.state = False

	def __del__( self ):
		self.stop()

def musicPlayer():
	if not hasattr(gl,'music'):
		if hasattr(gl,'sound'):
			path = gl.expandPath("//")+"music"+os.sep+gl.sound[2]
			playlist = [ path+os.sep+f for f in os.listdir(path) if os.path.isfile(path+os.sep+f) ]
			gl.music = Music(playlist)
			gl.music.play()
	else:
		gl.music.step()
