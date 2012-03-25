import bge
from r_wheel import *

class r_vehicle:
	def __init__(self, main, framerate = 120):
		self.main = main
		
		self.wheels = []
		
		self.framerate = framerate
		bge.logic.setLogicTicRate(framerate)
	
	def addWheel(self, wheel, wheel_type):
		self.wheels.append(r_wheel(self.main, wheel, wheel_type))
	
	def run(self):
		m = self.main
		
		dt = (1/self.framerate)
		
		lin_f = Vector([0,0,0])
		ang_f = Vector([0,0,0])
		
		for wheel in self.wheels:
			wheel.step(dt)
			lin_f += wheel.force
			ang_f += wheel.force_pos.cross(wheel.force)
		
		m.applyForce(lin_f)
		m.applyTorque(ang_f)
