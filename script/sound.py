import aud
from logs import log
from bge import logic as gl
import os


class Sound(object):
	""" sound manager """

	def __init__(self, buffered=False, looped=False, volume=False):
		""" Class initialiser """
		self.device = aud.device()
		self.buffered = buffered
		self.factory = None
		self.handle = None
		self.loop(looped)
		self.isPlaying = False
		if volume is not False:
			self.volume = volume
		elif hasattr(gl, 'sound'):
			self.volume = gl.sound[0]
		else:
			self.volume = 1
		self.play()
		self.stop()

	def load(self, soundPath):
		try:
			self.factory = aud.Factory(soundPath)
			if self.buffered:
				self.factory = aud.Factory.buffer(self.factory)
		except:
			log("error", "impossible de trouver le fichier " + soundPath)

	def play(self, forceStop=True):
		if forceStop:
			self.stop()
		if self.factory is not None and not self.isPlaying:
			self.handle = self.device.play(self.factory)
			self.handle.volume = self.volume
			self.handle.relative = True
			self.loop(self.looped)
			self.isPlaying = True

	def stop(self):
		if self.handle is not None:
			log("debug", "sound stop sound")
			self.handle.stop()
			self.isPlaying = False

	def setVolume(self, volume):
		self.volume = volume
		if self.handle is not None:
			self.handle.volume = volume

	def getVolume(self):
		return self.volume

	def location(self, location, velocity):
		if self.handle is not None:
			self.handle.location = location
			self.handle.velocity = velocity

	def getState(self):
		if self.handle is not None:
			return self.handle.status
		else:
			return None

	def setPitch(self, pitch):
		if self.handle is not None:
			if pitch < 0:
				pitch = -pitch
			self.handle.pitch = pitch

	def loop(self, looped=True):
		self.looped = looped
		if self.handle is not None:
			if looped:
				self.handle.loop_count = -1  # 3 pour les tests, sinon -1
			else:
				self.handle.loop_count = 0

	def __del__(self):
		self.stop()


class Music:
	def __init__(self, playlist, volume=False):
		self.player = Sound()
		self.playlist = playlist
		self.idPlayed = -1
		self.state = False
		self.updateVolume = True
		if volume is not False:
			self.setVolume(volume, False)
		elif hasattr(gl, 'sound'):
			self.setVolume(gl.sound[1])
		else:
			self.setVolume(1, False)

	def play(self):
		if (len(self.playlist) >= 1 and
				(self.player.getState() == 0 or self.player.getState() is None) and
				not self.state):
			self.state = True

	def step(self):
		if self.updateVolume and hasattr(gl, 'sound'):
			self.setVolume(gl.sound[1])
		if ((self.player.getState() == 0 or self.player.getState() is None) and
				self.state):
			self.playNext()

	def playNext(self):
		if len(self.playlist) >= 1 and self.state:
			self.state = False
			self.idPlayed += 1
			if len(self.playlist) <= self.idPlayed:
				self.idPlayed = 0
			self.player.load(self.playlist[self.idPlayed])
			self.player.play()
			self.state = True

	def getState(self):
		return self.state

	def setVolume(self, volume, updateVolume=True):
		self.updateVolume = updateVolume
		self.player.setVolume(volume)

	def getVolume(self):
		return self.player.getVolume()

	def stop(self):
		self.player.stop()
		self.state = False

	def __del__(self):
		self.stop()


def musicPlayer():
	if not hasattr(gl, 'music'):
		if hasattr(gl, 'sound'):
			path = gl.expandPath("//") + "music" + os.sep + gl.sound[2]
			playlist = [path + os.sep + f
					for f in os.listdir(path)
					if os.path.isfile(path + os.sep + f)]
			gl.music = Music(playlist)
			gl.music.play()
	elif not gl.music.getState():
		gl.music.play()
	else:
		gl.music.step()


class TestSoundVolume:
	def init(self):
		self.motorSound = Sound(buffered=True, looped=True)
		self.motorSound.load(gl.expandPath("//") + 'testMotorSound.ogg')
		self.motorSound.setPitch(0.2)

	def start(self):
		musicPlayer()
		self.motorSound.play()

	def step(self):
		musicPlayer()
		self.motorSound.setVolume(gl.sound[0])

	def stop(self):
		self.motorSound.stop()
		gl.music.stop()

	def __del__(self):
		self.stop()