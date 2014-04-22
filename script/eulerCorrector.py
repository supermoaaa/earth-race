from math import pi

class eulerCorrector :
	x = None
	y = None
	z = None
	comp = 0

	def setEuler(self, euler, order="XYZ") :
		inX = euler[order.index("X")]
		inY = euler[order.index("Y")]
		inZ = euler[order.index("Z")]

		if self.x == None or 1 :
			self.x = inX
			self.y = inY
			self.z = inZ
		else :
			diffx = abs(self.x - inX)
			diffy = abs(self.y - inY)
			diffz = abs(self.z - inZ)
			if 3.14 < diffx + diffy +diffz :
				self.comp += 1
				self.x = inX % (2 * pi) - pi
				self.y = - (inY % (2 * pi)) + pi
				self.z = inZ % (2 * pi) - pi
			else :
				self.x = inX
				self.y = inY
				self.z = inZ

	def getEuler(self) :
		return self.x, self.y, self.z, self.comp
