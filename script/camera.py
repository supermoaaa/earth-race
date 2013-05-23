from bge import logic as gl
from bge import render as render
from mathutils import Euler
from math import cos
from math import sin
from math import sqrt
from math import atan
import logs

class camera(object):
	def __init__( self, **args ):
		self.car = None
		self.carObj = None
		self.compteurOwner = None
		self.camera = None
		self.viewPort = [ 0, 0, render.getWindowWidth(), render.getWindowHeight() ]
		self.lens = None
		self.far = None
		self.setParams(*args)
		self.lastSpeed = 0.0
		self.rev = False
		self.downView = 0.0
		self.lastModifDownView = 0.0
		self.ray1 = None
		self.ray2 = None
		self.ray3 = None

	def setParams( self, **args):
		if 'car' in args: self.__setCar(args['car'])
		if 'camera' in args: self.__setCam(args['camera'])
		if 'viewPort' in args: self.viewPort = args['viewPort']
		if 'lens' in args: self.lens = args['lens']
		if 'far' in args: self.far = args['far']
		self.updateCam()

	def __setCar( self, car ):
		self.car = car
		self.carObj = car.getMainObject()
		self.compteurOwner = car.owner

	def __setCam( self, cam ):
		self.camera = cam
		self.ray1 = cam.childrenRecursive['camRayView']
		self.ray2 = cam.childrenRecursive['camRayHorizon']
		self.ray3 = cam.childrenRecursive['camRayView2']
		if self.lens == None:
			self.lens = self.camera.lens

	def updateCam(self):
		if self.camera!=None:
			self.camera.removeParent()
			self.camera.setViewport( self.viewPort[0], self.viewPort[1], self.viewPort[2], self.viewPort[3] )
			if self.lens!=None: self.camera.lens = self.lens
			if self.far!=None: self.camera.far = self.far
			if self.car!=None:
				self.car.setCamsParams(self.far,self.viewPort)
				self.car.setDefaultCam(self.camera)

	def reset(self):
		self.lastSpeed = 0.0
		self.downView = 0.0
		self.lastModifDownView = 0.0

	def simulate( self ):
		if self.car != None and self.camera != None:
			# variables initiales
			carPosX, carPosY, carPosZ = self.carObj.worldPosition
			ticRate = gl.getLogicTicRate()*2
			speed = abs(self.compteurOwner['kph'])+0.5
			smoothSpeed = (speed+self.lastSpeed*ticRate)/(ticRate-1)
			self.lastSpeed = speed
			carRot = self.carObj.localOrientation.to_euler('XYZ')[2]
			camRot = self.camera.localOrientation.to_euler('XYZ')
			camRot[2] = self.__diffAngle( camRot[2], 1.57 )
			xRelativePosition = smoothSpeed/150+5 # le dernier chiffre est la distance min
			yRelativePosition = 0
			zRelativePosition = 3.3-(smoothSpeed/150)*1.5

			# anti object entre la caméra et la voiture
			distance = self.__camDistance( self.carObj, self.camera ) # y a t'il un obstacle et à quel distance
			if distance != None:
				logs.log("debug","distance : "+str(distance))
				xRelativePosition = min( xRelativePosition, distance/1.1 )
				zRelativePosition = min( zRelativePosition, distance/2 )

			# anti vue trop courte
			modifDownView = self.__calculModifDownView()
			self.__smoothDownView(modifDownView)
			zRelativePosition -= self.downView
			xRelativePosition = max( xRelativePosition, 0.3 )
			zRelativePosition = max( zRelativePosition, 0.3 )
			camRot[0] = atan(xRelativePosition/(zRelativePosition/1.5))

			# début des calculs
			if self.car.gearSelect == 0: # si en marche arrière
				carRot = (carRot)%6.28-3.14
				if not self.rev: # si on vient de passer en marche arrière
					self.rev = True
					camRot[2] = carRot
					self.down = 0
			elif self.car.gearSelect!=0 and self.rev: # si on vient de passer en marche avant
				self.rev = False
				camRot[2] = carRot
				self.down = 0
			diff_angle = self.__diffAngle( carRot, camRot[2] ) # calcul de la différence d'angle
			# compensation pour le cas d'un bug sur l'axe z
			#~ if abs(diff_angle)>1.7:
				#~ carRot = (6.28-carRot)%6.28-3.14
				#~ diff_angle = self.__diffAngle( carRot, camRot[2] ) # calcul de la différence d'angle
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
			self.__dynamicLens()

	def __dynamicLens( self ):
		self.camera.lens = self.lens - self.lens * (self.compteurOwner['kph'])/300

	def __diffAngle( self, angle1, angle2 ):
		return ( angle1-angle2 + 3.14 ) % 6.28 - 3.14

	def __camDistance( self, obj1, obj2 ):
		pos1 = obj1.position
		pos2 = obj2.position
		dist = self.__distance( pos1, pos2 )
		obj, point, normal = obj1.rayCast( obj2, None, dist*1.5)
		if obj==None:
			return None
		return self.__distance( pos1, point )

	def __distance( self, pos1, pos2 ):
		return sqrt( (pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2 + (pos1[2]-pos2[2])**2 )

	def __camRay( self, ray1, ray2): # retourne True si il faut descendre la cam sinon False
		obj, point, normal = self.carObj.rayCast( ray1, self.camera )
		pos1 = self.camera.position
		if obj!=None:
			dist1 = self.__distance( pos1, point)
			obj, point, normal = self.carObj.rayCast( ray2, self.camera )
			if obj==None:
				return False
			dist2 = self.__distance( pos1, point)
			if dist2 > (dist1 + 1):
				return 1/dist1
		return False

	def __calculModifDownView(self):
			modifDownView = 0.0
			down = self.__camRay( self.ray1, self.ray2 )
			if down!=False:
				if self.downView<3:
					modifDownView = down
			elif self.downView>0:
				down = self.__camRay( self.ray3, self.ray1 )
				if down!=False:
					modifDownView = -down
			return modifDownView

	def __smoothDownView(self, modifDownView):
		#~ if self.lastModifDownView==0.0 :
			#~ self.downView += modifDownView
			#~ self.lastModifDownView = modifDownView
		#~ elif self.lastModifDownView<0 and modifDownView<0 :
		#~ elif self.lastModifDownView>0 and modifDownView>=0 :
			#~ self.downView += modifDownView
			#~ self.lastModifDownView = modifDownView
		#~ else :
			#~ self.lastModifDownView = 0.0
		modifDownView = ( modifDownView + self.lastModifDownView )/2
		self.downView += modifDownView
		self.lastModifDownView = modifDownView
