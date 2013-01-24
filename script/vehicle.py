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
		boostPower = int()
		print('vehicle init')
		print('type du véhicule : '+vehicle_type)
		print('touches : ',end='')
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
				print("mass"+param[1])
				owner.mass = float(param[1])
		self.main.suspendDynamics()

	def __del__(self):
		if hasattr(self,"main") and not self.main is None:
			self.main.endObject()
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
				wheelsConf.append([ self.main.children.get(param[3]), param[1], param[2]])
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
		print("Select steering wheel")

	def addPiece( self, piece, mainObject ):
		child = objects.addObject( self.owner, piece )
		if child!=None:
			if mainObject!=None:
				print('main Object : ',mainObject)
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
		if self.simulated and self.physic:
			print("-----------------------------\nsimulate")
			cont = gl.getCurrentController()

			sce = gl.getCurrentScene()

			main = self.owner

			#bge.render.enableMotionBlur(0.99)

			#END SETUP

			wheels = self.wheels

			u = main["accelerate"]
			d = main["reverse"]
			l = main["left"]
			r = main["right"]
			b = main["brake"]
			boost = main["boost"]
			upGear = main["upGear"]
			downGear = main["downGear"]
			respawn = main["respawn"]

			speed = main['kph']
			if upGear and self.gearSelect < ( len(self.gearCalcs) - 1) and not downGear:
				self.gearSelect += 1
			if downGear and self.gearSelect > 0 and not upGear:
				self.gearSelect -= 1
			gas = 0
			print("gear", self.gearSelect)
			if u: gas += eval(self.gearCalcs[self.gearSelect]) * u
			if d: gas -= 800 + boost*300

			wheels[0].e_torque = gas
			wheels[1].e_torque = gas
			wheels[2].e_torque = gas
			wheels[3].e_torque = gas

			brake = 0
			if b: brake = 800
			for w in wheels:
				w.w_brake = brake

			for w in wheels:
				if w.w_grip < -0.4 and w.hit:
					pass
					#~ skid = sce.addObject("skid", "evo_main", 500)
					#~ skid.worldPosition = w.hpos+w.hmat.col[2]*0.01
					#~ o = vectrack(w.hmat.col[2], w.hvel)
					#~ o[1].length = w.hvel.length/24
					#~ skid.worldOrientation = o

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
				input_steer = r*STEER_BASE-l*STEER_BASE

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


			wheels[0].w_steer = -steer
			wheels[1].w_steer = -steer
			wheels[2].w_steer = steer
			wheels[3].w_steer = steer

			#Simulate the vehicle
			self.run()
			self.checkCheckpoint()

			#Turn the steering wheel
			#~ sw = main.children["evo_hull"].children["evo_steeringwheel"]
			#~ sw.localOrientation = [(wheels[0].w_steer_current + wheels[1].w_steer_current)*2,-pi/8,-pi/2]

			main['steer'] = steer
			print('voiture :',main)
			main['kph'] = (wheels[0].kph + wheels[1].kph + wheels[2].kph + wheels[3].kph)/4
			main['mph'] = (wheels[0].mph + wheels[1].mph + wheels[2].mph + wheels[3].mph)/4
			main['gear'] = self.gearSelect

			if respawn:
				self.respawn()

	def run(self):
		main = self.main

		dt = (1/self.framerate)

		lin_f = Vector([0,0,0])
		ang_f = Vector([0,0,0])

		for wheel in self.wheels:
			wheel.step(dt)
			lin_f += wheel.force
			ang_f += wheel.force_pos.cross(wheel.force)

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

	def checkCheckpoint(self):
		main = self.main
		print(str(self.nextIdCheckpoint) + " / " + str(len(gl.checkpoints)))
		print(self.distance( main, gl.checkpoints[self.nextIdCheckpoint] ))
		if self.nextIdCheckpoint < len(gl.checkpoints) and self.distance( main, gl.checkpoints[self.nextIdCheckpoint] )<5:
			self.nextIdCheckpoint += 1
			print("pass")
		if self.nextIdCheckpoint >= len(gl.checkpoints):
			self.nbTours += 1
		if self.nbTours == gl.nbTours:
			self.stop()
			print("arrived")

	def respawn(self):
		main = self.main
		zeroVector = Vector([0,0,0])
		main.applyForce(zeroVector)
		main.applyTorque(zeroVector)
		if self.nextIdCheckpoint >= 1:
			print(str(self.main) + " to " + str(gl.checkpoints[self.nextIdCheckpoint-1]))
			main.worldPosition = gl.checkpoints[self.nextIdCheckpoint-1].worldPosition
			main.worldOrientation = gl.checkpoints[self.nextIdCheckpoint-1].worldOrientation
		else:
			main.worldPosition = gl.checkpoints[len(gl.checkpoints)-1].worldPosition
			main.worldOrientation = gl.checkpoints[self.nextIdCheckpoint-1].worldOrientation

	def distance(self, obj0, obj1):
		pos0 = obj0.worldPosition
		pos1 = obj1.worldPosition

		cotex = +(pos0[0] - pos1[0])
		cotey = +(pos0[1] - pos1[1])
		cotez = +(pos0[2] - pos1[2])

		dist = sqrt(cotex**2 + cotey**2 + cotez**2)

		return dist

	def getRaceDuration(self):
		try:
			return str(timedelta(seconds=end-self.start))
		except:
			return -1
