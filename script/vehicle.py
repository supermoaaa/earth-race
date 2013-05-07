#Advanced raycast vehicle simulation
#By Raider.
#
#THIS IS AN UNFINISHED PROTOTYPE.

#Set this property True for halo-like steering (Remember to change camera too)
USE_MOUSE_STEERING = False

from bge import logic as gl
from time import time
from datetime import timedelta
import os
from mathutils import Vector
import objects
import logs

#BEGIN SETUP
from physicVehicle_math import *
#from steeringWheel import *

class vehicleSimulation(object):
	def __init__( self, vehicle_type, owner, physic=True, parent=False, framerate = 60 ):
		scene = gl.getCurrentScene()
		self.owner = owner
		owner['gear']=0
		owner['kph']=0
		self.vehicle_type = vehicle_type
		self.wheels = []
		self.steering_wheel = None
		self.framerate = framerate
		bge.logic.setLogicTicRate(framerate)

		self.gearCalcs = []
		self.gearSelect = 1
		self.nextIdCheckpoint = 1
		self.nbTours = 0
		try:
			gl.nbTours = gl.nbTours
		except:
			gl.nbTours = 1
		self.simulated = False
		self.physic = physic
		self.boostPower = int()
		self.cams = []
		self.currentCam = 0
		logs.log('debug','vehicle init')
		logs.log("debug",'type du véhicule : '+vehicle_type)
		for param in gl.conf[1][vehicle_type]:
			if param[0] == "car":
				mainObject = self.addPiece( param[1], None )
				self.main = mainObject
				self.setParent(parent)
				gl.objectsCars.append(mainObject)
			#~ elif param[0] == "child":
				#~ self.addPiece( line[8:-1], mainObject )
			elif param[0] == "steering_wheel":
				pos_ob = self.owner.children.get(param[1])
				#self.addSteeringWheel( pos_ob ) # pos_ob, steering_wheel
			elif param[0] == "gear":
				self.gearCalcs.append(''.join(param[1:]))
			elif param[0] == "boostPower":
				self.boostPower=int(param[1])
			elif param[0] == "mass":
				logs.log("debug","mass "+param[1])
				self.main.mass = float(param[1])
			elif param[0] == "cam":
				cam = self.main.children.get(param[1])
				if cam != None:
					logs.log("debug","add sub cam "+param[1])
					self.cams.append(cam)
				else:
					logs.log("error","impossible de trouver l'objet : "+param[1]+" comme fils de : "+str(self.main))
		self.main.suspendDynamics()

	def __del__(self):
		self.unloadWheel()

	def setParent( self, parent ):
		if parent:
			self.main.setParent(self.owner)
		else:
			self.main.removeParent()

	def setPhysic( self, activate ):
		if activate:
			self.main.restoreDynamics()
		else:
			self.main.suspendDynamics()
		self.physic = activate

	def getWheelsConf(self):
		scene = gl.getCurrentScene()
		wheelsConf=[]
		for param in gl.conf[1][self.vehicle_type]:
			if param[0] == "wheel":
				wheelsConf.append([ self.main.children.get(param[4]), param[1], param[2], param[3] ])
		return wheelsConf

	def getMainObject(self):
		return self.main

	def addWheel(self, wheel):
		self.wheels.append(wheel)

	def unloadWheel(self):
		#~ for w in self.wheels:
			#~ w.delete()
		self.wheels = []

	def addSteeringWheel(self, pos_ob):
		self.steering_wheel = steering_wheel(pos_ob)
		logs.log("debug","Select steering wheel")

	def addPiece( self, piece, mainObject ):
		child = objects.addObject( self.owner, piece )
		if child!=None:
			if mainObject!=None:
				logs.log("debug",'main Object : '+str(mainObject))
				#position
				objects.copyRelatifPosition(self.owner, child, mainObject)
				#orientation
				objects.copyRelatifOrientation(self.owner, child, mainObject)
				#scaling
				objects.copyRelatifScale(self.owner, child, mainObject)
				child.setParent(mainObject)

			try:
				self.pieces.append(child)
			except:
				self.pieces=[child]
		return child

	def simulate( self ):
		if self.simulated and self.physic and len(self.wheels)>0:
			logs.log("debug","-----------------------------")
			logs.log("debug","simulate")
			cont = gl.getCurrentController()

			sce = gl.getCurrentScene()

			main = self.owner

			#bge.render.enableMotionBlur(0.99)

			#END SETUP

			wheels = self.wheels

			accelerate = main["accelerate"]
			reverse = main["reverse"]
			left = main["left"]
			right = main["right"]
			brake = main["brake"]
			boost = main["boost"]
			upGear = main["upGear"]
			downGear = main["downGear"]
			respawn = main["respawn"]
			changeCam = main["changeCam"]

			self.__keyChangeCam( changeCam )

			speed = main['kph']
			if upGear and self.gearSelect < ( len(self.gearCalcs) - 1) and not downGear:
				self.gearSelect += 1
			if downGear and self.gearSelect > 0 and not upGear:
				self.gearSelect -= 1
			gas = 0
			logs.log("debug","gear"+str(self.gearSelect))
			if accelerate>0.0: gas += eval(self.gearCalcs[self.gearSelect]) * accelerate	# accelerate
			if reverse>0.0: gas -= 800 + boost*300 * reverse							# reverse

			#Camera-steering
			#~ cambase = main.children["camera"]
			#~ cbmat = cambase.worldOrientation
			#~ mmat = main.worldOrientation

			#~ relmat = mmat*cbmat.inverted()
			#~ steer = relmat.to_euler()[2]

			STEER_BASE = 0.8
			STEERING_DECAY = 0.1
			ANTIDRIFT = 0.5
			YAW_DAMP = 0#.1

			av = main.getAngularVelocity(1)
			lv = main.getLinearVelocity(1)

			input_steer = 0.0
			if USE_MOUSE_STEERING:
				pass
				#~ input_steer = steer
				#~ if lv[1] < 0.0: input_steer = -steer
			else:
				input_steer = right*STEER_BASE-left*STEER_BASE

			drift_steer = 0.0
			drift_vec = Vector([lv[0], lv[1]])

			if lv[1]>0.0: drift_steer = drift_vec.angle(Vector([0, 1])) * ((lv[0]>0.0)-0.5)*2.0
			if lv[1]<0.0: drift_steer = drift_vec.angle(Vector([0,-1])) * ((lv[0]>0.0)-0.5)*2.0

			#~ if self.steering_wheel!=None:
				#~ self.steering_wheel.setSteer(input_steer)

			drift_steer *= (abs(lv[1]) > 10)


			drift_vel = Vector([lv[0], lv[1]]).length

			input_steer = input_steer/(1+abs(lv[1]**0.9)*STEERING_DECAY)
			drift_steer = drift_steer*((1 - (1/(1+drift_vel)))*ANTIDRIFT)
			ydamp_steer = av[2]*YAW_DAMP

			steer = input_steer + drift_steer + ydamp_steer

			for w in wheels:
				w.e_torque = gas
				w.w_handbrake = brake
				w.setSteer(steer)
				if w.w_grip < -0.4 and w.hit:
					pass
					#~ skid = sce.addObject("skid", "evo_main", 500)
					#~ skid.worldPosition = w.hpos+w.hmat.col[2]*0.01
					#~ o = vectrack(w.hmat.col[2], w.hvel)
					#~ o[1].length = w.hvel.length/24
					#~ skid.worldOrientation = o

			#Simulate the vehicle
			self.__run()
			self.__checkCheckpoint()

			#Turn the steering wheel
			#~ sw = main.children["evo_hull"].children["evo_steeringwheel"]
			#~ sw.localOrientation = [(wheels[0].w_steer_current + wheels[1].w_steer_current)*2,-pi/8,-pi/2]

			main['steer'] = steer
			logs.log("debug",'voiture :'+str(main))
			main['kph'] = 0
			main['mph'] = 0
			for wheel in self.wheels:
				main['kph'] += wheel.kph
				main['mph'] += wheel.mph
			main['kph'] /= len(self.wheels)
			main['mph'] /= len(self.wheels)
			main['gear'] = self.gearSelect

			if respawn:
				self.__respawn()

	def __run(self):
		if len(self.wheels)>0:
			main = self.main

			dt = (1/self.framerate)

			lin_f = Vector([0,0,0])
			ang_f = Vector([0,0,0])

			#~ physics engine's' compensation
			groundContact=len(self.wheels)
			for wheel in self.wheels:
				wheel.step(dt)
				lin_f += wheel.force
				ang_f += wheel.force_pos.cross(wheel.force)
				if wheel.hit:
					groundContact-=1
			lin_f[2]+=-10*self.main.mass*groundContact/len(self.wheels)

			main.applyForce(lin_f)
			main.applyTorque(ang_f)

	def start(self):
		self.simulated = True
		self.setPhysic(True)
		self.start = time()

	def stop(self):
		self.end = time()
		self.simulated = False
		self.setPhysic(False)
		self.owner['arrived'] = True

	def __checkCheckpoint(self):
		main = self.main
		logs.log("debug",str(self.nextIdCheckpoint) + " / " + str(len(gl.checkpoints)))
		if self.nextIdCheckpoint < len(gl.checkpoints) and main.getDistanceTo( gl.checkpoints[self.nextIdCheckpoint] )<5:
			self.nextIdCheckpoint += 1
			logs.log("debug","pass checkpoint")
		if self.nextIdCheckpoint >= len(gl.checkpoints):
			self.nbTours += 1
			self.nextIdCheckpoint = 0
		if self.nbTours == gl.nbTours:
			self.stop()
			logs.log("debug","arrived")

		#~ positionning of the objectif for IA
		if self.nextIdCheckpoint+1 < len(gl.checkpoints):
			self.owner['AI'].worldPosition = gl.checkpoints[self.nextIdCheckpoint+1].worldPosition
		elif self.nbTours<=gl.nbTours:
			self.owner['AI'].worldPosition = gl.checkpoints[0].worldPosition
		else:
			self.owner['AI'].worldPosition = gl.checkpoints[gl.checkpoints-1]

	def __respawn(self):
		main = self.main
		zeroVector = Vector([0,0,0])
		main.applyForce(zeroVector)
		main.applyTorque(zeroVector)
		if self.nextIdCheckpoint >= 1:
			logs.log("debug",str(self.main) + " to " + str(gl.checkpoints[self.nextIdCheckpoint-1]))
			main.worldPosition = gl.checkpoints[self.nextIdCheckpoint-1].worldPosition
			main.worldOrientation = gl.checkpoints[self.nextIdCheckpoint-1].worldOrientation
		else:
			main.worldPosition = gl.checkpoints[len(gl.checkpoints)-1].worldPosition
			main.worldOrientation = gl.checkpoints[self.nextIdCheckpoint-1].worldOrientation

	def getAI(self):
		return self.owner['AI']

	def getRaceDuration(self):
		try:
			return str(timedelta(seconds=end-self.start))
		except:
			return -1

	def setCamsParams(self, lens, viewPort):
		self.viewPort = viewPort
		for cam in self.cams:
			cam.lens = lens
			cam.setViewport( viewPort[0], viewPort[1], viewPort[2], viewPort[3] )

	def setDefaultCam(self, cam):
		self.defaultCam = cam
		cam.useViewport = True
		gl.getCurrentScene().active_camera = cam
		self.currentCam = len(self.cams)

	def __keyChangeCam(self, changeCam):
		if len(self.cams)>0 and changeCam>0:
				if self.currentCam==len(self.cams)-1:
					self.changeCam( self.cams[self.currentCam], self.defaultCam )
					self.currentCam += 1
				elif self.currentCam>=len(self.cams):
					self.changeCam( self.defaultCam, self.cams[0] )
					self.currentCam = 0
				else:
					self.changeCam( self.cams[self.currentCam], self.cams[self.currentCam+1] )
					self.currentCam += 1

	def changeCam(self, oldCam, newCam):
		newCam.useViewport = True
		gl.getCurrentScene().active_camera = newCam
		oldCam.useViewport = False
