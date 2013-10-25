import vehicle
from bge import logic as gl
import confParser as conf
from physicVehicle_wheel import r_wheel
from camera import camera
import logs

class vehicleLinker(object):
	def __init__(self, **args):
		if not hasattr(gl,"objectsCars"):
			gl.objectsCars = []
		self.camera = camera()
		self.vehicle_type = None
		self.car = None
		self.wheels_type = None
		self.wheels_free = True
		self.physic = True
		self.parent = False
		if 'physic' in args: self.setPhysic(args['physic'])
		if 'parent' in args and args['parent'] == True:
			self.parent = True
			self.physic = False
		if 'posObj' in args: self.objPos = args['posObj']
		else: self.objPos = gl.getCurrentController().owner
		if 'vehicle_type' in args: self.setVehicle( args['vehicle_type'] )
		if 'wheels_type' in args: self.setWheels( args['wheels_type'] )
		if 'camera_object' in args: self.camera.setParams( camera = args['camera_object'] )
		if 'viewPort' in args: self.camera.setParams( viewPort = args['viewPort'] )

	def setParent( self, parent ):
		if self.car != None:
			self.car.setParent(parent)

	def setPhysic( self, activate ):
		if not self.parent:
			self.physic = activate
			if self.car != None:
				self.car.setPhysic(self.physic)

	def setVehicle( self, vehicle_type ):
		if self.vehicle_type != vehicle_type:
			if self.car != None:
				self.delVehicle()
			conf.loadVehicle(vehicle_type, self.onFinishVehicleLoaded)
			self.vehicle_type = vehicle_type

	def onFinishVehicleLoaded(self, st):
		logs.log("debug","finish loading vehicle : "+self.vehicle_type)
		wheels_type=self.wheels_type
		conf.setFinishLoadedVehicle(self.vehicle_type)
		self.car = vehicle.vehicleSimulation( self.vehicle_type, self.objPos, self.physic, self.parent )
		self.__updateWheels()
		self.camera.setParams( car = self.car )

	def setWheels( self, wheels_type ):
		if self.wheels_type != wheels_type:
			if self.wheels_type != None:
				self.delWheels()
				self.wheels_type=None
			conf.loadWheel(wheels_type, self.onFinishWheelsLoaded)
			self.wheels_type = wheels_type

	def onFinishWheelsLoaded(self, st):
		logs.log("debug","finish loading wheels : "+self.wheels_type)
		conf.setFinishLoadedWheel(self.wheels_type)
		self.__updateWheels()

	def getVehicleConf( self ):
		return gl.conf[1][self.vehicle_type]

	def getWheelsConf( self ):
		return gl.conf[2][self.wheels_type]

	def isLoaded( self ):
		return self.isVehicleLoaded() and self.isWheelsLoaded()

	def isVehicleLoaded( self ):
		return conf.isLoadedVehicle(self.vehicle_type)

	def isWheelsLoaded( self ):
		return conf.isLoadedWheel(self.wheels_type)

	def __updateWheels( self ):
		if self.car != None and self.wheels_type != None and self.wheels_type in gl.conf[2] and conf.isLoadedWheel(self.wheels_type):
			for wheel_conf in self.car.getWheelsConf():
				wheel = r_wheel(self.car.getMainObject(), wheel_conf[0], self.wheels_type, wheel_conf[1], wheel_conf[2], wheel_conf[3])
				self.car.addWheel(wheel)
			self.wheels_free = False

	def __updateCamera( self ):
		if self.camera != None and self.car != None and self.isVehicleLoaded():
			self.camera.updateCam()

	def delVehicle( self ):
		conf.freeVehicle(self.vehicle_type)

	def delWheels( self ):
		if self.car != None:
			self.car.unloadWheel()
		conf.freeWheels(self.wheels_type)
		self.wheels_free = True

	def __del__( self ):
		self.delVehicle()
		logs.log("debug","del vehicleLinker")

	def simulate( self ):
		if self.car != None and conf.isLoadedWheel(self.wheels_type):
			self.car.simulate()
			self.camera.simulate()

	def getRaceDuration( self ):
		if self.car != None:
			return self.car.getRaceDuration()
		return None

	def start( self ):
		if self.car != None:
			self.car.start()
			self.__updateCamera()

	def startCam( self ):
		if self.car != None:
			self.__updateCamera()
			self.car.startCam()

	def stop( self ):
		if self.car != None:
			self.car.stop()
