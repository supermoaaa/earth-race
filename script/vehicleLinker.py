import vehicle
from bge import logic as gl
import confParser as conf
from physicVehicle_wheel import r_wheel

class vehicleLinker(object):
	def __init__(self, **args):
		if not hasattr(gl,"objectsCars"):
			gl.objectsCars = []
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
			wheels_type=self.wheels_type
			if self.car != None:
				self.delVehicle()
			if vehicle_type not in gl.conf[1]:
				conf.loadVehicle(vehicle_type)
			self.vehicle_type = vehicle_type
			self.car = vehicle.vehicleSimulation( vehicle_type, self.objPos, self.physic, self.parent )
			if wheels_type!=None:
				if wheels_type not in gl.conf[2]:
					conf.loadWheel(wheels_type)
				self.__updateWheels()

	def setWheels( self, wheels_type ):
		if self.wheels_type != wheels_type:
			if self.wheels_type != None:
				self.delWheels()
				self.wheels_type=None
			if wheels_type not in gl.conf[2]:
				conf.loadWheel(wheels_type)
			self.wheels_type = wheels_type
			self.__updateWheels()

	def getVehicleConf( self ):
		return gl.conf[1][self.vehicle_type]

	def getWheelsConf( self ):
		return gl.conf[2][self.wheels_type]

	def __updateWheels( self ):
		if self.car != None and self.wheels_type != None:
			if not self.wheels_free:
				self.delWheels()
			for wheel_conf in self.car.getWheelsConf():
				wheel = r_wheel(self.car.getMainObject(), wheel_conf[0], self.wheels_type, wheel_conf[1], wheel_conf[2])
				self.car.addWheel(wheel)
			self.wheels_free = False

	def delVehicle( self ):
		self.delWheels()
		self.car=None
		conf.freeVehicle(self.vehicle_type)

	def delWheels( self ):
		if self.car!=None:
			self.car.unloadWheel()
		conf.freeWheels(self.wheels_type)
		self.wheels_free = True

	def __del__( self ):
		self.delVehicle()

	def simulate( self ):
		if self.car != None:
			self.car.simulate()

	def getRaceDuration( self ):
		if self.car != None:
			return self.car.getRaceDuration()
		return None

	def start( self ):
		if self.car != None:
			self.car.start()

	def stop( self ):
		if self.car != None:
			self.car.stop()
