from geometry import *

class Mass(Point):
	def __init__(self, m = 10, v = Point(0, 0), x = 0, y = 0):
		super(Mass, self).__init__(x, y)
		self._m = float(m)
		self._v = v
		self._springs = {}
		self._gf = Point(0, -9.8 * self._m) 	# constant
		self._prevf = self._gf 	# for Velocity Verlet

	def update(self, dt):
		self.step(dt)

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
		self._prevf = f
		self._v += (self._prevf + f) * 0.5 * dt / self._m		# Velocity Verlet

		# self._v += self.calcForce(dt) / self._m
		# dPos = self._v * dt
		# self._x = dPos.x
		# self._y = dPos.y 	# Euler

class Wheel(Mass):
	def __init__(self, radius = 1, torque = 0, v = Point(0, 0), x = 0, y = 0):
		m = 2 * radius * float(radius)
		super(Wheel, self).__init__(m, v, x, y)
		self._r = radius
		self._T = torque
		self._om = 0
		self._inAir = True

	def update(self, dt):
		self.calcForce()
		self.step()

class Spring(object):
	def __init__(self, m1, m2, D):
		self._l0 = dist(m1, m2)
		self._l = self._l0
		self._D = D
		self._b = D * 0.07

	def getForce(self, m1, m2, dt):
		l = dist(m1, m2)
		diffl = l - self._l0
		dl = l - self._l
		self._l = l
		absF = self._D * diffl + self._b * dl / dt		# D * x + b * (dx / dt)
		direct = m2 - m1
		return direct.normalized() * absF

class Bike(object):
	def __init__(self, c):
		self._fitness = 0
		self._chromosome = c
		self._m1 = Mass(m = 40, v = Point(0, 0), x = 0, y = 0)
		self._m2 = Mass(m = 20, v = Point(0, 0), x = c[0].x, y = c[0].y)
		self._w1 = Wheel(radius = c[2], torque = 1)
