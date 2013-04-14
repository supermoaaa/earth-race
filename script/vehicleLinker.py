import vehicle
from bge import logic as gl
from mathutils import Euler
from math import cos
from math import sin
from math import sqrt
import confParser as conf
from physicVehicle_wheel import r_wheel
import logs

class vehicleLinker(object):
	def __init__(self, **args):
		if not hasattr(gl,"objectsCars"):
			gl.objectsCars = []
		self.camera = None
		self.vehicle_type = None
		self.car = None
		self.wheels_type = None
		self.wheels_free = True
		self.physic = True
		self.parent = False
		self.rev = False
		self.lastSpeed = 0.0
		if 'physic' in args: self.setPhysic(args['physic'])
		if 'parent' in args and args['parent'] == True:
			self.parent = True
			self.physic = False
		if 'posObj' in args: self.objPos = args['posObj']
		else: self.objPos = gl.getCurrentController().owner
		if 'vehicle_type' in args: self.setVehicle( args['vehicle_type'] )
		if 'wheels_type' in args: self.setWheels( args['wheels_type'] )
		if 'camera_object' in args: self.setCamera( args['camera_object'] )

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
		self.__updateCamera()

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

	def setCamera( self, cameraObj ):
		self.camera = cameraObj
		self.__updateCamera()

	def getVehicleConf( self ):
		return gl.conf[1][self.vehicle_type]

	def getWheelsConf( self ):
		return gl.conf[2][self.wheels_type]

	def isLoaded( self ):
		return conf.isLoadedVehicle(self.vehicle_type) and conf.isLoadedWheel(self.wheels_type)

	def __updateWheels( self ):
		if self.car != None and self.wheels_type != None and self.wheels_type in gl.conf[2] and conf.isLoadedWheel(self.wheels_type):
			for wheel_conf in self.car.getWheelsConf():
				wheel = r_wheel(self.car.getMainObject(), wheel_conf[0], self.wheels_type, wheel_conf[1], wheel_conf[2], wheel_conf[3])
				self.car.addWheel(wheel)
			self.wheels_free = False

	def __updateCamera( self ):
		if self.camera != None and self.car != None:
			self.camera.removeParent()

	def delVehicle( self ):
		conf.freeVehicle(self.vehicle_type)

	def delWheels( self ):
		if self.car!=None:
			self.car.unloadWheel()
		conf.freeWheels(self.wheels_type)
		self.wheels_free = True

	def __del__( self ):
		self.delVehicle()
		logs.log("debug","del vehicleLinker")

	def simulate( self ):
		if self.car != None and conf.isLoadedWheel(self.wheels_type):
			self.car.simulate()
			if self.camera != None:
				self.__simulateCamera( self.__distance( self.car.getMainObject(), self.camera ) )

	def __diffAngle( self, angle1, angle2 ):
		return ( angle1-angle2 + 3.14 ) % 6.28 - 3.14

	def __distance( self, obj1, obj2 ):
		pos1 = obj1.position
		pos2 = obj2.position
		dist = sqrt( (pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2 + (pos1[2]-pos2[2])**2 )
		obj, point, normal = obj1.rayCast( obj2, None, dist*1.5)
		if obj==None:
			return None
		pos1 = obj1.position
		return sqrt( (pos1[0]-point[0])**2 + (pos1[1]-point[1])**2 + (pos1[2]-point[2])**2 )

	def __simulateCamera( self, distance ):
		if self.camera != None:
			# variables initiales
			car = self.car.getMainObject()
			carPosX, carPosY, carPosZ = car.worldPosition
			ticRate = gl.getLogicTicRate()*2
			speed = abs(self.car.owner['kph'])+0.5
			smoothSpeed = (speed+self.lastSpeed*ticRate)/(ticRate-1)
			self.lastSpeed = speed
			xRelativePosition = smoothSpeed/150+5 # le dernier chiffre est la distance min
			yRelativePosition = 0
			zRelativePosition = 3.3-smoothSpeed/150
			if distance != None:
				logs.log("debug","distance : "+str(distance))
				xRelativePosition = min( xRelativePosition, distance/1.1 )
				zRelativePosition = min( zRelativePosition, distance/2 )
			carRot = car.localOrientation.to_euler('XYZ')[2]
			camRot = self.camera.localOrientation.to_euler('XYZ')
			camRot[2] = self.__diffAngle( camRot[2], 1.57 )
			camRot[0] = 1.4 - 0.2*(150-smoothSpeed)/150

			# début des calculs
			if self.car.gearSelect == 0: # si en marche arrière
				carRot = (carRot)%6.28-3.14
				if not self.rev: # si on vient de passer en marche arrière
					self.rev = True
					camRot[2] = carRot
			elif self.car.gearSelect!=0 and self.rev: # si on vient de passer en marche avant
				self.rev = False
				camRot[2] = carRot
			diff_angle = self.__diffAngle( carRot, camRot[2] ) # calcul de la différence d'angle
			# compensation pour le cas d'un bug sur l'axe z
			if abs(diff_angle)>1.7:
				carRot = (6.28-carRot)%6.28-3.14
				diff_angle = self.__diffAngle( carRot, camRot[2] ) # calcul de la différence d'angle
			# lissage des mouvements de la caméra
			if -0.785<diff_angle and diff_angle<0.785:
				logs.log("debug",'smooth')
				carRot = camRot[2] + diff_angle*0.1
			# blocage d'extrémités
			diff_angle =self.__diffAngle( carRot, camRot[2] ) # calcul de la différence d'angle
			if diff_angle<-0.785:
				carRot = carRot + 0.785
			elif diff_angle>0.785:
				carRot = carRot - 0.785
			carRot %= 6.28
			# calcul de la position de la caméra
			camPosX = carPosX+xRelativePosition*cos(carRot)-yRelativePosition*sin(carRot)
			camPosY = carPosY+xRelativePosition*sin(carRot)+yRelativePosition*cos(carRot)
			# application de la position et orientation sur la caméra
			self.camera.worldPosition = [camPosX,camPosY,carPosZ+zRelativePosition]
			self.camera.localOrientation = Euler([camRot[0],camRot[1],(carRot+(3.14/2))%6.28],'XYZ').to_matrix()

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
