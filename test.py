from geometry import *
from bike import *
from surface import *

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

p3 += p4
print p3.x

t = 0
dt = 0.01

origin = Point(0, 10)
mass = Mass(1, Point(0, 3), 0, 5)

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

elem = SurfaceElement(Point(0, 30.02), Point(52, 0))	# 30 degrees
surface = Surface(70, 50)

wheel = Wheel(1, 10, Point(0, 0), 2, 2)

outfile = open("wheelpos_surf.txt", "w")

t = 0
while t < 15 and wheel.x < 100:	# change condition in surface.getClosePoints() to run this test
	bikepos = wheel
	bikepos = wheel.step(dt, surface)
	text = "{time}   {x}   {y}\n"
	text = text.format(time = t, x = wheel.x, y = wheel.y)
	outfile.write(text)
	t += dt
print wheel.x
print t
