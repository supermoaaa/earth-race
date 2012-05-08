#Advanced raycast vehicle simulation
#By Raider.
#
#THIS IS AN UNFINISHED PROTOTYPE.

#Set this property True for halo-like steering (Remember to change camera too)
USE_MOUSE_STEERING = False

import bge
	
#BEGIN SETUP
from physicVehicle_math import *

class vehicleSimulation:
	def __init__( ):
		gear=[[]]
		boostPower=int()
	
	def __init__( vehicle_type, wheel_type, keys ):
		self.__init__( )
		
		try:
			propertieFile = open("../objects/vehicles/"+vehicle_type+".cfg", "r")
			for line in fichier:
				if "gear = " in ligne:
					gear=eval(ligne[7:])
				if "boostPower = "
					boostPower=int(ligne[13:])
		except:
			print("fichier de configuration ../objects/vehicles/"+vehicle_type+".cfg non trouvé")
			print("paramètres par défaut utilisé")

	def simulate():
		cont = bge.logic.getCurrentController()
		
		#print(dir(bge.logic.getCurrentScene()))
		
		sce = bge.logic.getCurrentScene()
		
		main = cont.owner
		
		#bge.render.enableMotionBlur(0.99)
		
		if not "vs" in main:
			vs = main["vs"] = r_vehicle(main)
			
			vs.addWheel(main.children["fl_wheel"], wheel_type)
			vs.addWheel(main.children["fr_wheel"], wheel_type)
			vs.addWheel(main.children["bl_wheel"], wheel_type)
			vs.addWheel(main.children["br_wheel"], wheel_type)
		#END SETUP
		
		wheels = main["vs"].wheels
		
		u = cont.sensors["up"].positive
		d = cont.sensors["down"].positive
		l = cont.sensors["left"].positive
		r = cont.sensors["right"].positive
		b = cont.sensors["brake"].positive
		boost = cont.sensors["boost"].positive
		
		gas = 0
		if u: gas += 1000 + boost*500
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
				skid = sce.addObject("skid", "evo_main", 500)
				skid.worldPosition = w.hpos+w.hmat.col[2]*0.01
				o = vectrack(w.hmat.col[2], w.hvel)
				o[1].length = w.hvel.length/24
				skid.worldOrientation = o
		
		#Camera-steering
		cambase = main.children["camera_base"]
		cbmat = cambase.worldOrientation
		mmat = main.worldOrientation
		
		relmat = mmat*cbmat.inverted()
		steer = relmat.to_euler()[2]
		
		STEER_BASE = 0.8
		STEERING_DECAY = 0.1
		ANTIDRIFT = 0.5
		YAW_DAMP = 0#.1
		
		av = main.getAngularVelocity(1)
		lv = main.getLinearVelocity(1)
		
		input_steer = 0.0
		if USE_MOUSE_STEERING:
			input_steer = steer
			if lv[1] < 0.0: input_steer = -steer
		else:
			input_steer = r*STEER_BASE-l*STEER_BASE
		
		drift_steer = 0.0
		drift_vec = Vector([lv[0], lv[1]])
		
		if lv[1]>0.0: drift_steer = drift_vec.angle(Vector([0, 1])) * ((lv[0]>0.0)-0.5)*2.0
		if lv[1]<0.0: drift_steer = drift_vec.angle(Vector([0,-1])) * ((lv[0]>0.0)-0.5)*2.0
		
		drift_steer *= (abs(lv[1]) > 10)
		
		
		drift_vel = Vector([lv[0], lv[1]]).length
		
		input_steer = input_steer/(1+abs(lv[1]**0.9)*STEERING_DECAY)
		drift_steer = drift_steer*((1 - (1/(1+drift_vel)))*ANTIDRIFT)
		ydamp_steer = av[2]*YAW_DAMP
		
		steer = input_steer + drift_steer + ydamp_steer
		
		
		wheels[0].w_steer = -steer
		wheels[1].w_steer = -steer
		#wheels[2].w_steer = steer
		#wheels[3].w_steer = steer
		
		#Simulate the vehicle
		main["vs"].run()
		
		#Turn the steering wheel
		sw = main.children["evo_hull"].children["evo_steeringwheel"]
		sw.localOrientation = [(wheels[0].w_steer_current + wheels[1].w_steer_current)*2,-pi/8,-pi/2]
		
		
		main['kph'] = (wheels[0].kph + wheels[1].kph + wheels[2].kph + wheels[3].kph)/4
		main['mph'] = (wheels[0].mph + wheels[1].mph + wheels[2].mph + wheels[3].mph)/4
