from geometry import *
from surface import Surface

class Mass(Point):
	def __init__(self, m = 10, v = Point(0, 0), x = 0, y = 0):
		super(Mass, self).__init__(x, y)
		self._m = float(m)
		self._v = v
		self._springs = {}
		self._gf = Point(0, -9.8 * self._m) 	# constant
		self._prevf = self._gf 	# for Velocity Verlet

	def touches(self, surface):
		if surface.isAbove(self):
			return True
		return False

	def setSprings(self, springs):
		self._springs = springs 	# dict {point: spring}

	def calcForce(self, dt):
		f = self._gf
		for s in self._springs:
			f += self._springs[s].getForce(self, s, dt)
		return f

	def getForce(self):
		return self._prevf

	def step(self, dt):
		dPos = self._v * dt + self._prevf * 0.5 * dt * dt / self._m
		self._x += dPos.x
		self._y += dPos.y
		f = self.calcForce(dt)
		self._v += (self._prevf + f) * 0.5 * dt / self._m		# Velocity Verlet
		self._prevf = f
		return self

		# self._v += self.calcForce(dt) / self._m
		# dPos = self._v * dt
		# self._x = dPos.x
		# self._y = dPos.y 	# Euler

class Wheel(Mass):
	def __init__(self, radius = 1, torque = 0, v = Point(0, 0), x = 0, y = 0):
		m = 2 * float(radius)
		super(Wheel, self).__init__(m, v, x, y)
		self._r = radius
		self._T = torque
		self._I = self._m * self._r * self._r 	# ring
		self._om = 0
		self._inAir = True

	@property
	def r(self):
		return self._r

	def step(self, dt, surface):
		pts = surface.getClosePoints(self)
		self._inAir = True
		# while len(pts) > 0:
		if dist(pts[0], self) < self._r:
			touchPoint = pts[0]
			self._inAir = False
				# pts.pop(0)
			# break
			# else:
				# pts.pop(0)
		if self._inAir == True:
			super(Wheel, self).step(dt)
		else:
			r = touchPoint - self	# pull the wheel out of surface
			d = r.getLength() - self._r
			r = r.normalized()
			# mov = r * d
			# self._x += mov.x
			# self._y += mov.y
			veldir = r.rotatedBy90()
			self._v = veldir * (self._om * self._r) 	# condition on touch
			# while len(pts) > 0:
			# 	if dist(self, pts[0]) < self._r:	# pull the wheel out of other surfaces
			# 		r = pts[0] - self
			# 		d = r.getLength() - self._r
			# 		r = r.normalized()
			# 		# cosA = veldir * r
			# 		# d /= cosA
			# 		# mov = veldir * d
			# 		# self._x += mov.x
			# 		# self._y += mov.y
			# 	pts.pop(0)

			mult = 1 / (self._m + self._I / (self._r * self._r))

			dPos = self._v * dt + self._prevf * 0.5 * dt * dt * mult
			self._x += dPos.x
			self._y += dPos.y

			f = self.calcForce(dt)		#as for Mass
			r = touchPoint - self
			r = r.normalized()
			absN = f * r
			if absN > 0:
				N = r * -absN
			else:
				N = Point(0, 0)
			f += N
			fr = veldir * (self._T / self._r)
			f += fr
			
			self._v += (self._prevf + f) * 0.5 * dt * mult
			self._prevf = f
			self._om = self._v.getLength() / self._r
			return self

class Spring(object):
	def __init__(self, m1, m2, D):
		self._l0 = dist(m1, m2)
		self._l = self._l0
		self._D = D
		self._b = 20

	def getForce(self, m1, m2, dt):
		l = dist(m1, m2)
		diffl = l - self._l0
		dl = l - self._l
		self._l = l
		absF = self._D * diffl + self._b * dl / dt		# D * x + b * (dx / dt)
		direct = m2 - m1
		return direct.normalized() * absF

class Bike(object):
	def __init__(self, c, bikepos, test = False):
		self._fitness = 0
		self._chromosome = c
		self._m1 = Mass(m = 40, x = 0, y = 0)	# all velocities implicitly = (0, 0)
		self._m2 = Mass(m = 20, x = c[0].x, y = c[0].y)
		self._w1 = Wheel(radius = c[2], torque = 700, x = c[1].x, y = c[1]. y)
		self._w2 = Wheel(radius = c[4], x = c[3].x, y = c[3].y)	# torque = 0
		self._m1m2 = Spring(self._m1, self._m2, c[5])
		self._m1w1 = Spring(self._m1, self._w1, c[6])
		self._m1w2 = Spring(self._m1, self._w2, c[7])
		self._m2w1 = Spring(self._m2, self._w1, c[8])
		self._m2w2 = Spring(self._m2, self._w2, c[9])
		self._w1w2 = Spring(self._w1, self._w2, c[10])

		self._springset = {"m1": {self._m2: self._m1m2, self._w1: self._m1w1, self._w2: self._m1w2},
						   "m2": {self._m1: self._m1m2, self._w1: self._m2w1, self._w2: self._m2w2},
						   "w1": {self._m1: self._m1w1, self._m2: self._m2w1, self._w2: self._w1w2},
						   "w2": {self._m1: self._m1w2, self._m2: self._m2w2, self._w1: self._w1w2}}

		self._m1.x += bikepos.x		# converting coordinates to global frame
		self._m1.y += bikepos.y
		self._m2.x += bikepos.x
		self._m2.y += bikepos.y
		self._w1.x += bikepos.x
		self._w1.y += bikepos.y
		self._w2.x += bikepos.x
		self._w2.y += bikepos.y

	def setFitness(self, fit):
		self._fitness = fit

	def getFitness(self):
		return self._fitness

	def getChromosome(self):
		return self._chromosome

	def getElements(self):
		return [self._m1, self._m2, self._w1, self._w2]

	def touches(self, surface):
		if self._m1.touches(surface) or self._m2.touches(surface):
			return True
		return False

	def step(self, dt, surface):
		self._w1.setSprings(self._springset["w1"])
		self._w1.step(dt, surface)
		self._w2.setSprings(self._springset["w2"])
		self._w2.step(dt, surface)
		self._m1.setSprings(self._springset["m1"])
		self._m1.step(dt)
		self._m2.setSprings(self._springset["m2"])
		self._m2.step(dt)
