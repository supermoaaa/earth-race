from bge import logic as gl
from bge import render as render
from mathutils import Euler
from math import cos
from math import sin
from math import sqrt
from math import atan
from logs import log
from eulerCorrector import eulerCorrector
import objects

class camera:

	def __init__(self, **args):
		self.car = None
		self.carObj = None
		self.compteurOwner = None
		self.camera = None
		self.viewPort = [0, 0,
				render.getWindowWidth(), render.getWindowHeight()]
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
		self.carRotEuler = eulerCorrector()
		self.smoothCarRotY = 0
		self.attachedToCam = []

	def setParams(self, car=None, camera=None, viewPort=None,
				lens=None, far=None):
		if car is not None:
			self.__setCar(car)
		if camera is not None:
			self.__setCam(camera)
		if viewPort is not None:
			self.viewPort = viewPort
		if lens is not None:
			self.lens = lens
		if far is not None:
			self.far = far
		self.updateCam()

	def __setCar(self, car):
		self.car = car
		self.carObj = car.getMainObject()
		self.compteurOwner = car.owner

	def __setCam(self, cam):
		self.camera = cam
		self.ray1 = cam.childrenRecursive['camRayView']
		self.ray2 = cam.childrenRecursive['camRayHorizon']
		self.ray3 = cam.childrenRecursive['camRayView2']
		if self.lens is None:
			self.lens = self.camera.lens

	def updateCam(self):
		if self.camera is not None:
			self.__cleanAttached()
			self.camera.removeParent()
			self.camera.setViewport(
				self.viewPort[0], self.viewPort[1], self.viewPort[2], self.viewPort[3])
			if self.lens is not None:
				self.camera.lens = self.lens
			if self.far is not None:
				self.camera.far = self.far
			if self.car is not None:
				self.car.setCamsParams(self.far, self.viewPort)
				self.car.setDefaultCam(self.camera)
			self.__setAttached()

	def __cleanAttached(self):
		for attachedObj in self.attachedToCam:
			objects.endObject(attachedObj[0])
		self.attachedToCam = []

	def __setAttached(self):
		for skyParam in gl.sky:
			if skyParam[0] == "attachedToCam":
				child = objects.addObject(self.camera, skyParam[1])
				if child is not None:
					self.attachedToCam.append([child, \
												float(skyParam[2]), \
												float(skyParam[3]), \
												float(skyParam[4])])

	def __positionAttached(self, speed):
		for attachedObj, decalZ, decalX, speedMultiplier in self.attachedToCam:
			ori = attachedObj.worldOrientation.to_euler()
			ori[2] = self.camera.worldOrientation.to_euler()[2]
			attachedObj.worldPosition = self.camera.localPosition[:]
			yLocalRelativePostion = decalX + (speed / 350) * speedMultiplier
			xRelativePosition, yRelativePosition = self.__to3D(0, yLocalRelativePostion, ori[2])
			attachedObj.worldPosition[0] += xRelativePosition
			attachedObj.worldPosition[1] += yRelativePosition
			attachedObj.worldPosition[2] += decalZ
			attachedObj.worldOrientation = ori.to_matrix()

	def reset(self):
		self.lastSpeed = 0.0
		self.downView = 0.0
		self.lastModifDownView = 0.0

	def simulate(self, speed):
		if self.car is not None and self.camera is not None:
			# variables initiales
			carPosX, carPosY, carPosZ = self.carObj.worldPosition
			carPosZ += 0.2  # correct the center of view
			ticRate = gl.getLogicTicRate() * 2
			absSpeed = abs(speed) + 0.5
			smoothSpeed = (absSpeed + self.lastSpeed * ticRate) / (ticRate + 1)
			self.lastSpeed = absSpeed
			self.carRotEuler.setEuler(self.carObj.localOrientation.to_euler("YXZ"), "YXZ")
			carRotZ = self.carRotEuler.getEuler()[2]
			self.smoothCarRotY = (self.carRotEuler.getEuler()[0] + self.smoothCarRotY * (ticRate/6)) / ((ticRate/6) + 1)
			camRot = self.camera.localOrientation.to_euler('XYZ')
			camRot[2] = self.__diffAngle(camRot[2], 1.57)

			# inversion de la caméra si on passe en marche arrière
			carRotZ, camRot[2], smoothSpeed = self.__autoReverseCam(speed>=0, carRotZ, camRot[2], smoothSpeed)

			# le dernier chiffre est la distance min
			xRelativePosition = smoothSpeed / 150 + 5
			yRelativePosition = 0
			zRelativePosition = 3.2 - (smoothSpeed / 150) * 1.5


			# anti object entre la caméra et la voiture
			xRelativePosition, zRelativePosition = self.__correctBlockedView(xRelativePosition, zRelativePosition)

			# limite
			xRelativePosition = max(xRelativePosition, 0.3)

			# anti vue trop courte
			log("debug", "zRelativePosition not compensate : "+str(zRelativePosition))
			zRelativePosition, xRelativePosition = self.__to3D(zRelativePosition, xRelativePosition, self.smoothCarRotY)
			log("debug", "zRelativePosition compensate : "+str(zRelativePosition))
			log("debug", "compensator : "+str(self.smoothCarRotY))

			#limite
			zRelativePosition = max(zRelativePosition, 0.3)

			# calcul de l'angle de la caméra
			camRot[0] = atan(xRelativePosition / (zRelativePosition / 1.5))

			# compensation pour le cas d'un bug sur l'axe z
			#~ if abs(diff_angle)>1.7:
				#~ carRotZ = (6.28-carRotZ)%6.28-3.14
				# calcul de la différence d'angle
				# ~ diff_angle = self.__diffAngle( carRotZ, camRot[2] )
			# lissage des mouvements de la caméra
			carRotZ = self.__smoothAngle(carRotZ, camRot[2])
			# blocage d'extrémités
			carRotZ = self.__limitAngle(carRotZ, camRot[2])
			# calcul de la position de la caméra
			camPosX, camPosY = self.__to3D(xRelativePosition, yRelativePosition, carRotZ)
			camPosX += carPosX
			camPosY += carPosY
			# application de la position et orientation sur la caméra
			self.camera.worldPosition = [camPosX,
										camPosY, carPosZ + zRelativePosition]
			self.camera.localOrientation = Euler(
				[camRot[0], camRot[1], (carRotZ + (3.14 / 2)) % 6.28], 'XYZ').to_matrix()
			self.__dynamicLens()
			self.__positionAttached(smoothSpeed)

	def __dynamicLens(self):
		self.camera.lens = self.lens - self.lens * \
			(self.compteurOwner['kph']) / 300

	def __diffAngle(self, angle1, angle2):
		return (angle1 - angle2 + 3.14) % 6.28 - 3.14

	def __camDistance(self, obj1, obj2):
		pos1 = obj1.position
		pos2 = obj2.position
		dist = self.__distance(pos1, pos2)
		obj, point, normal = obj1.rayCast(obj2, None, dist * 1.5)
		if obj is None:
			return None
		return self.__distance(pos1, point)

	def __distance(self, pos1, pos2):
		return sqrt((pos1[0] - pos2[0]) ** 2 +
				(pos1[1] - pos2[1]) ** 2 +
				(pos1[2] - pos2[2]) ** 2)

	# anti object entre la caméra et la voiture
	def __correctBlockedView(self, xRelativePosition, zRelativePosition):
		# y a t'il un obstacle et à quel distance
		distance = self.__camDistance(self.carObj, self.camera)
		if distance is not None:
			log("debug", "distance : " + str(distance))
			xRelativePosition = min(xRelativePosition, distance / 1.1)
			zRelativePosition = min(zRelativePosition, distance / 2)
		return xRelativePosition, zRelativePosition

	# lissage des mouvements de la caméra
	def __smoothAngle(self, carRotZ, camRotZ):
		diff_angle = self.__diffAngle(carRotZ, camRotZ)
		if -0.785 < diff_angle and diff_angle < 0.785:
			log("debug", 'smooth')
			carRotZ = camRotZ + diff_angle * 0.1
		return carRotZ

	# blocage d'extrémités
	def __limitAngle(self, carRotZ, camRotZ):
		# calcul de la différence d'angle
		diff_angle = self.__diffAngle(carRotZ, camRotZ)
		if diff_angle < -0.785:
			carRotZ = carRotZ + 0.785
		elif diff_angle > 0.785:
			carRotZ = carRotZ - 0.785
		carRotZ %= 6.28
		return carRotZ

	# inversion de la caméra si on passe en marche arrière
	def __autoReverseCam(self, forward, carRotZ, camRotZ, smoothSpeed):
		if not forward:  # si on est en marche arrière
			carRotZ = (carRotZ) % 6.28 - 3.14
			if smoothSpeed<0: smoothSpeed = smoothSpeed * 4
			if not self.rev:  # si on vient de passer en marche arrière
				self.rev = True
				camRotZ = carRotZ
				self.down = 0
		elif forward and self.rev: # si on vient de passer en marche avant
			self.rev = False
			camRotZ = carRotZ
			self.down = 0
		return carRotZ, camRotZ, smoothSpeed

	def __to3D(self, x, y, angle):
		return x*cos(angle) - y*sin(angle), x*sin(angle) + y*cos(angle)

	# retourne True si il faut descendre la cam sinon False
	def __camRay(self, ray1, ray2):
		obj, point, normal = self.carObj.rayCast(ray1, self.camera)
		pos1 = self.camera.position
		if obj is not None:
			dist1 = self.__distance(pos1, point)
			obj, point, normal = self.carObj.rayCast(ray2, self.camera)
			if obj is None:
				return False
			dist2 = self.__distance(pos1, point)
			if dist2 > (dist1 + 1):
				return 1 / dist1
		return False
