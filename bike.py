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

	def step(self, dt, surface):
		pts = surface.getClosePoints(self)
		touchPoint = None
		while len(pts) > 0:
			if dist(pts[0], self) < self._r:
				touchPoint = pts[0]
				break
			else:
				pts.pop(0)
		if touchPoint == None:
			self._inAir = True
			super(Wheel, self).step(dt)
		else:
			self._inAir = False
			r = touchPoint - self	# pull the wheel out of surface
			d = r.getLength()
			r = r.normalized()
			mov = r * (d - self._r)
			self._x += mov.x
			self._y += mov.y
			veldir = r.rotatedBy90()
			self._v = veldir * (self._om * self._r) 	# condition on touch
			# pts.pop(0)
			# while len(pts) > 0:
			# 	if d(self, pts[0]) < self._r:
			# 		r = pts[0] - self
			# 		d = r.getLength()
			# 		r = r.normalized()
			# 		mov = r * (d - self._r)
			# 		cosA = mov * veldir
			# 		mov = veldir / cosA

			f = super(Wheel, self).calcForce(dt)
			absN = f * r
			if absN > 0:
				N = r * -absN
			else:
				N = Point(0, 0)
			f += N
			mgsinA = veldir * (self._gf * veldir) 	# vector multiplied by scalar
			mult = self._m / (self._m + self._I / (self._r * self._r))
			fr = (f + veldir * (self._T / self._r)) * mult - mgsinA
			f += fr

			dPos = self._v * dt + self._prevf * 0.5 * dt * dt / self._m
			self._x += dPos.x
			self._y += dPos.y
			f = self.calcForce(dt)
			self._v += (self._prevf + f) * 0.5 * dt / self._m
			self._prevf = f
			self._om = self._v.getLength() / self._r
			return self

class Spring(object):
	def __init__(self, m1, m2, D):
		self._l0 = dist(m1, m2)
		self._l = self._l0
		self._D = D
		self._b = 7

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
