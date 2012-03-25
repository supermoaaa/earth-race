import bge
from mathutils import *
from r_math import *
from math import *

class r_wheel:
	def __init__(self, main_ob, wheel_ob):
		
		self.e_torque = 0.0				#Engine torque (connect directly to gas pedal!)
		self.e_backtorque = 5			#A drag factor on the engine that serves to limit the maximum speed of the wheel.
		self.e_gearing = 1				#Engine gearing ratio. This affects both torque and backtorque; higher gears have lower torque, but less backforce, allowing the wheel to reach a higher speed.. just like a real gearbox.
		self.w_brake = 0.0				#Braking torque (always attempts to stop the wheel)
		
		self.w_vel = 0.0				#Angular velocity of the wheel (radians per second)
		self.w_radius = 0.33			#Wheel radius (Note that this is like a second gearing factor!)
		self.w_ang = 0.0				#Wheel angle
		self.w_mass = 10.0				#Wheel angular mass (Does not affect actual weight of vehicle)
		self.w_staticf = 1.5			#Wheel coefficient of friction (ground is assumed to be 1.0)
		self.w_edgef = 0.5				#Wheel coefficient of friction when it is running on the rim- i.e. if the wheel is tilted, there is less rubber on the road. Friction is interpolated between w_friction at 0 degrees and w_edge_friction at 90 degrees.
		self.w_dynf = 1.0				#Dynamic coefficient of friction
		self.w_grip = 0					#Whether or not the wheel is skidding
		self.w_steer = 0.0				#Wheel steering angle (in radians). Positive angles rotate to the right.
		self.w_steer_current = 0.0		#The current steering angle.
		self.w_steer_rate = 2.0			#Rate at which the wheel turns towards the target angle. (Radians/second)
		self.w_steer_limit = 0.8		#Maximum steering angle
		
		self.w_axelf = 10				#The friction torque on the axle. Like a brake force that is always on.
		
		self.p_pos = Vector([0,0,0])	#Contact patch position (stored relative to ray hit point)
		self.p_vel = Vector([0,0,0])	#Again, relative to hit point
		self.p_shift = 0.3				#The maximum distance the patch can shift relative to the wheel.
		self.p_damp = 15000				#Patch spring viscous damping coefficient
		
		#See 'contact patches' and 'Cattaneo problem'. This simulation assumes an extremely small spring is desired.
		#An appropriate maximum patch spring force is calculated automatically from the vehicle's mass.
		#By the way, for anyone wondering, I don't understand half of the stuff I code. Honestly, the 'cattaneo problem'
		#is just something that seems vaguely similar to this.
		
		self.s_rest_length = 0.4			#The rest length of the suspension spring (from attach point to axle)
		self.s_length = self.s_rest_length	#The current length of the suspension spring
		self.s_force = 40000.0				#The maximum vertical spring force (at 100% compression)
		self.s_damp = 6000.0				#Suspension viscous damping coefficient (can become unstable at high values- tune carefully.)
		self.s_exp = 1.5					#Exponent which curves the force/distance graph. Does NOT change the maximum force.
		
		#Don't edit these variables.
		self.main = main_ob
		self.wheel = wheel_ob
		
		self.attach_pos = wheel_ob.localPosition.copy()
		self.attach_pos[2] += self.s_length
		self.attach_mat = wheel_ob.localOrientation.copy()
		
		self.r = [None,None,None]
		self.hit = False
		self.hpos = Vector([0,0,0])
		self.hmat = None
		self.hvel = Vector([0,0,0])
		self.force = Vector([0,0,0])
		self.force_pos = Vector([0,0,0])
		
		self.kph = 0.0
		self.mph = 0.0

	def __init__(self, main_ob, wheel_ob, wheel_type):
		self.__init__(self, main_ob, wheel_ob)

		try:
			propertieFile = open("../objects/wheels/"+wheel_type+".cfg", "r")
			for line in fichier:
				if "radius = " in ligne:
					self.w_radius = float(ligne[9:])
				elif "mass = " in ligne:
					self.w_mass = float(ligne[7:])
				elif "friction = " in ligne:
					self.w_staticf = float(ligne[11:])
				#~ elif chaine in ligne:
					#~ self.w_edgef = 0.5
				#~ elif chaine in ligne:
					#~ self.w_dynf = 1.0
				elif "grip = " in ligne:
					self.p_shift = float(ligne[7:])
				elif "steer_rate = " in ligne:
					self.w_steer_rate = float(ligne[13:])
				elif "steer_limit = " in ligne:
					self.w_steer_limit = float(ligne[14:])
				elif "friction_torque = " in ligne:
					self.w_axelf = float(ligne[18:])
				elif "rest_length = " in ligne:
					self.s_rest_length = float(ligne[14:])
					self.s_length = self.s_rest_length
				elif "max_force = " in ligne:
					self.s_force = float(ligne[12:])
				elif "damp = " in ligne:
					self.s_damp = float(ligne[7:])
				elif "exponent = " in ligne:
					self.s_exp = float(ligne[11:])
			propertieFile.close
		except:
			print("fichier de configuration ../objects/wheels/"+wheel_type+".cfg non trouvé")
			print("paramètres par défaut utilisé")
	
	def step(self, dt):
		
		mpos = self.main.worldPosition.copy()
		mmat = self.main.worldOrientation.copy()
		
		#Steering value
		self.w_steer_current = towards(self.w_steer_current, self.w_steer, self.w_steer_rate*dt)		#Approach target
		self.w_steer_current = min(max(self.w_steer_current, -self.w_steer_limit), self.w_steer_limit)	#Limit range
		
		#Generate worldspace wheel matrix, with steering applied
		wmat = mmat*(self.attach_mat*Matrix.Rotation(self.w_steer_current, 3, "Z"))
		
		#Ray coordinates..
		p0 = apos = mpos + mmat*self.attach_pos
		p1 = p0 - (mmat*self.attach_mat).col[2]*(self.s_rest_length+self.w_radius)
		
		#Cast the ray
		self.r = self.wheel.rayCast(p1, p0)
		if self.r[0]:
			
			#Generate surface-aligned contact matrix
			self.hmat = vectrack(self.r[2], wmat.col[1])
			self.flatness = self.hmat.col[2].dot(wmat.col[2])
			self.hit = True
		
		else:
			self.p_pos = Vector([0,0,0])
			self.hit = False
		
		#Reset the length variable (otherwise it 'sticks' when the wheel breaks contact and can incorrectly remain compressed)
		self.s_length = self.s_rest_length
		
		#Reset the force variables
		self.force = Vector([0,0,0])
		self.force_pos = Vector([0,0,0])
		
		
		#Run the sim!
		
		if self.r[0]:
			hob = self.r[0]
			hpos = self.hpos = self.r[1]
			
			main = self.main
			hmat = self.hmat
			
			#Hit position relative to the locations of main and hob (hit object)
			hpos_main = hpos - mpos
			hpos_hob = hpos - hob.worldPosition
			
			#Velocity of main at hit point
			hvel = self.hvel = (main.getVelocity(hpos_main) - hob.getVelocity(hpos_hob))
			
			p_pos = self.p_pos.copy()
			
			#Keep the patch still..
			p_pos -= hvel*dt
			
			#Move the patch according to the wheel rotation
			p_pos += self.w_vel * self.w_radius * hmat.col[1]*dt
			
			#Project the patch position onto the hit plane
			p_pos = vecplaneproject(p_pos, hmat.col[2])
			
			#p_pos = dualplanelimit(p_pos, hmat[0], self.p_shift)
			#p_pos = dualplanelimit(p_pos, hmat[1], self.p_shift)
			
			#Are we skidding?
			self.w_grip = 1 - p_pos.length / self.p_shift
			
			#Limit the distance the patch can shift from the rest position
			if p_pos.length != 0:
				p_pos.length = min(self.p_shift, p_pos.length)
			
			#Calculate patch velocity (relative to main), then copy the new position back to storage
			self.p_vel = (p_pos - self.p_pos)/dt
			self.p_pos = p_pos
			
			#Debug patch offset
			#bge.render.drawLine(hpos, hpos+self.p_pos, [1,1,1])
			
			#Debug grip
			#bge.render.drawLine(hpos, hpos+Vector([0,0,2]), [self.w_grip,0,0])
			
			#Suspension normal force
			self.s_length = max((apos-hpos).length-self.w_radius, 0)
			s_fac = 1.0 - self.s_length/self.s_rest_length
			s_spring_force = (s_fac**self.s_exp)*self.s_force
			s_spring_force -= hvel.dot(hmat.col[2])*self.s_damp
			Fnormal = max(s_spring_force, 0)
			
			#Calculate patch force
			Fpatch = p_pos * self.main.mass*8/self.p_shift #It is assumed that mass*5 is an appropriate maximum force
			#Fpatch = (p_pos.length/self.p_shift)**2 * p_pos/self.p_shift * self.main.mass*8/self.p_shift
			Fpatch += self.p_vel*self.p_damp
			
			#Force of road friction
			
			if self.w_grip < 0.0:
				Ftraction = Fnormal*lerp(self.w_edgef, self.w_staticf, self.flatness)
			else:
				Ftraction = Fnormal*lerp(self.w_edgef, self.w_dynf, self.flatness)
			
			#Limit patch force by available traction
			Fpatch.length = min(Fpatch.length, Ftraction)
			
			#Apply torque to wheel
			self.w_vel -= ((Fpatch.dot(hmat.col[1])*self.w_radius)/self.w_mass)*dt
			
			force = Fnormal*hmat.col[2]+Fpatch
			
			#Apply inverse force to hit object
			hob.applyImpulse(hpos_hob, -force*dt)
			
			#Force on vehicle has special treatment to iron out bugs. See r_vehicle.py.
			self.force = force
			self.force_pos = hpos_main
			
			
		#Engine torque
		self.e_gearing = max(0.0000001, self.e_gearing)
		Tengine = self.e_torque/self.e_gearing - self.w_vel*self.e_backtorque/self.e_gearing
		
		self.w_vel += (Tengine/self.w_mass)*dt
		
		#Brake torque
		Tbrake = self.w_brake + self.w_axelf
		
		self.w_vel = towards(self.w_vel, 0, (Tbrake/self.w_mass)*dt)
		
		#Wheel rotation
		self.w_ang -= self.w_vel*dt
		
		#Apply wheel position
		self.wheel.localPosition = self.attach_pos - self.attach_mat.col[2]*self.s_length
		
		#Apply wheel rotation
		self.w_ang = fmod(self.w_ang, 2*pi)
		ang = Matrix.Rotation(self.w_ang, 3, "X")
		self.wheel.worldOrientation = wmat*ang
		
		#Calculate ground speed
		self.kph = self.w_vel*self.w_radius*3.6
		self.mph = self.kph*0.621371192
