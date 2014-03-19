from geometry import *
from bike import *

class A(object):
	def __init__(self, x):
		self._x = x

	@property
	def x(self):
		return self._x
	@x.setter
	def x(self, value):
		self._x = value
	
	def __add__(self, other):
		return A(self.x + other.x)

class B(A):
	def __init__(self, x):
		super(B, self).__init__(x)

p1 = A(1)
p2 = A(2)
print p1.x

p = p1 + p2
print p.x

p3 = B(4)
p4 = B(3)

p = p3 + p4
print p.x

t = 0
dt = 0.01

origin = Point(0, 10)
mass = Mass(1, Point(0, 0), 0, 5)

spring = Spring(mass, origin, 100)

outfile = open("damposc.txt", "w")

while t < 10:
	mass.setSprings({origin: spring})
	mass.step(dt)
	f = mass.getForce()
	text = "{time}   {y}   {fy}\n"
	text = text.format(time = t, y = mass.y, fy = f.y)
	outfile.write(text)
	t += dt
