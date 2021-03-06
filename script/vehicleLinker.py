import vehicle
from bge import logic as gl
import confParser as conf
from physicVehicle_wheel import r_wheel
from camera import camera
from logs import log
from weakref import proxy as weakInstance


class vehicleLinker(object):
	def __init__(self, physic=True, parent=False,
				posObj=gl.getCurrentController().owner,
				vehicle_type=None, wheels_type=None,
				camera_object=None, viewPort=None, shadowObj=None):
		self.carPartsColor = []
		self.windowsColor = []
		if not hasattr(gl, "objectsCars"):
			gl.objectsCars = []
		self.camera = camera()
		self.camera.setParams(camera=camera_object, viewPort=viewPort)
		self.car = None
		self.vehicle_type = None
		self.setVehicle(vehicle_type)
		self.shadowObj = shadowObj
		self.wheels_type = None
		self.wheels_free = True
		self.setWheels(wheels_type)
		self.physic = physic
		self.parent = False
		if parent is True:
			self.parent = True
			self.physic = False
		self.objPos = posObj

	def setParent(self, parent):
		if self.car is not None:
			self.car.setParent(parent)

	def setPhysic(self, activate):
		if not self.parent:
			self.physic = activate
			if self.car is not None:
				self.car.setPhysic(self.physic)

	def setVehicle(self, vehicle_type):
		if self.vehicle_type != vehicle_type:
			if self.car is not None:
				obName = self.car.main.name
				self.delVehicle()
				log("debug", "ob persist " + str(gl.getCurrentScene().objects.get(obName)))
			log("debug", "vehicleLinker setVehicle " + vehicle_type)
			self.vehicle_type = vehicle_type
			conf.loadVehicle(vehicle_type, self.onFinishVehicleLoaded)

	def getVehicle(self):
		return self.car.getMainObject()

	def setVehicleColor(self, r=None, g=None, b=None):
		if r!=None and g!=None or b!=None:
			if self.car:
				self.car.setCarColor(r, g, b)
			self.carPartsColor = [r, g, b]

	def setWindowsColor(self, r=None, g=None, b=None):
		if r!=None and g!=None or b!=None:
			if self.car:
				self.car.setWindowsColor(r, g, b)
			self.windowsColor = [r, g, b]

	def onFinishVehicleLoaded(self, st):
		log("debug", "finish loading vehicle : " + self.vehicle_type)
		conf.setFinishLoadedVehicle(self.vehicle_type)
		self.car = vehicle.vehicleSimulation(
				self.vehicle_type, self.objPos,
				self.physic, self.parent, self.shadowObj, weakInstance(self))
		self.__updateWheels()
		self.camera.setParams(car=self.car)
		if len(self.carPartsColor)==3:
			self.setVehicleColor(*self.carPartsColor)
		if len(self.windowsColor)==3:
			self.setWindowsColor(*self.windowsColor)

	def setWheels(self, wheels_type):
		if self.wheels_type != wheels_type:
			if self.wheels_type is not None:
				self.delWheels()
				self.wheels_type = None
			self.wheels_type = wheels_type
			conf.loadWheel(wheels_type, self.onFinishWheelsLoaded)


	def onFinishWheelsLoaded(self, st):
		log("debug", "finish loading wheels : " + self.wheels_type)
		conf.setFinishLoadedWheel(self.wheels_type)
		self.__updateWheels()

	def getVehicleConf(self):
		return gl.conf[1][self.vehicle_type]

	def getWheelsConf(self):
		return gl.conf[2][self.wheels_type]

	def isLoaded(self):
		return self.isVehicleLoaded() and self.isWheelsLoaded()

	def isVehicleLoaded(self):
		return conf.isLoadedVehicle(self.vehicle_type)

	def isWheelsLoaded(self):
		return conf.isLoadedWheel(self.wheels_type)

	def __updateWheels(self):
		if (self.car is not None and
				self.wheels_type is not None and
				self.wheels_type in gl.conf[2] and
				conf.isLoadedWheel(self.wheels_type)):
			for wheel_conf in self.car.getWheelsConf():
				wheel = r_wheel(
						self.car.getMainObject(), wheel_conf[0],
						self.wheels_type, wheel_conf[1], weakInstance(self),
						wheel_conf[2], wheel_conf[3])
				self.car.addWheel(wheel)
			self.wheels_free = False

	def __updateCamera(self):
		if (self.camera is not None and
				self.car is not None and self.isVehicleLoaded()):
			self.camera.updateCam()

	def delVehicle(self):
		log("debug", "del vehicle")
		self.car = None
		conf.freeVehicle(self.vehicle_type)

	def delWheels(self):
		print("del wheel")
		if self.car is not None:
			self.car.unloadWheel()
		conf.freeWheels(self.wheels_type)
		self.wheels_free = True

	def __del__(self):
		self.delVehicle()
		log("debug", "del vehicleLinker")

	def simulate(self):
		if self.car is not None and conf.isLoadedWheel(self.wheels_type):
			self.car.simulate()
			self.camera.simulate(self.car.owner['kph'])

	def respawn(self):
		if self.car is not None and conf.isLoadedWheel(self.wheels_type):
			self.car.respawn()

	def getRaceDuration(self):
		if self.car is not None:
			return self.car.getRaceDuration()
		return None

	def start(self):
		if self.car is not None:
			self.car.start()
			self.__updateCamera()

	def startSound(self):
		if self.car is not None and self.isVehicleLoaded():
			self.car.startSound()

	def stopSound(self):
		if self.car is not None and self.isVehicleLoaded():
			self.car.stopSound()

	def startCam(self):
		if self.car is not None and self.isVehicleLoaded():
			self.__updateCamera()
			self.car.startCam()

	def stop(self):
		if self.car is not None:
			self.car.stop()
