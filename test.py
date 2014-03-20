from geometry import *
from bike import *
from surface import *
from simulator import *
import matplotlib.pyplot as mpl

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

#t = 0
#dt = 0.01

#origin = Point(0, 10)
#mass = Mass(1, Point(0, 3), 0, 5)

#spring = Spring(mass, origin, 100)

#outfile = open("damposc.txt", "w")

#while t < 10:
#	mass.setSprings({origin: spring})
#	mass.step(dt)
#	f = mass.getForce()
#	text = "{time}   {y}   {fy}\n"
#	text = text.format(time = t, y = mass.y, fy = f.y)
#	outfile.write(text)
#	t += dt

#elem = SurfaceElement(Point(0, 30.02), Point(52, 0))	# 30 degrees
#surface = Surface(70, 50)

#wheel = Wheel(1, 10, Point(0, 0), 2, 2)

#outfile = open("wheelpos_surf.txt", "w")

#t = 0
#while t < 15 and wheel.x < 100:	# change condition in surface.getClosePoints() to run this test
#	bikepos = wheel
#	bikepos = wheel.step(dt, surface)
#	text = "{time}   {x}   {y}\n"
#	text = text.format(time = t, x = wheel.x, y = wheel.y)
#	outfile.write(text)
#	t += dt
#print wheel.x
#print t

elem = SurfaceElement(Point(0, 0), Point(52, 0))	# 30 degrees
surface = Surface(50, 50)
surfacepoints = surface.getPoints()
#Draw the surface
mpl.ion()
figure = mpl.figure()
axes = figure.add_subplot('111',aspect='equal')
xs, ys = zip(*surfacepoints)
mpl.plot(xs,ys,linewidth=3)
#    
    
c = [Point(-1, 0), Point(0, -1), 0.5, Point(-1, -1), 0.5, 5000, 5000, 5000, 5000, 5000, 5000]

b = Bike(c, Point(2, 2))

#Initializing Bike Elements for Animation
axes.set_ylim(-10,10)
time_text = axes.text(0.02, 0.95, '', transform=axes.transAxes)
dist_text = axes.text(0.02, 0.90, '', transform=axes.transAxes)
elems = b.getElements()
spr1,=axes.plot([elems[2].x,elems[3].x,elems[0].x,elems[1].x,elems[3].x], [elems[2].y,elems[3].y,elems[0].y,elems[1].y,elems[3].y],'-')
spr2,=axes.plot([elems[1].x,elems[2].x,elems[0].x], [elems[1].y,elems[2].y,elems[0].y],'-')
wheel1 = mpl.Circle((0,0), radius=elems[2].r,color='black')
axes.add_patch(wheel1)
wheel1.center = (elems[2].x,elems[2].y)
wheel2 = mpl.Circle((0,0), radius=elems[3].r,color='black')
wheel2.center = (elems[3].x,elems[3].y)
axes.add_patch(wheel2)
point1 = mpl.Circle((0,0), radius=0.2,color='r')
point1.center = (elems[0].x,elems[0].y)
axes.add_patch(point1)
point2 = mpl.Circle((0,0), radius=0.2,color='r')
point2.center = (elems[1].x,elems[1].y)
axes.add_patch(point2)
   
t = 0.0
dt = 0.001

#outfile = open("bike_surf.txt", "w")

doRun = True
nsteps = 0
while doRun:
	b.step(dt, surface)
        
	# print b.getPositions()[0]
	# vis.draw(self)

	# bpos = b.getPositions()[0]
	# rundist = bpos.x - self._initpos.x
	# if rundist >= maxdist:
	# 	doRun = False
	# distances.append(rundist)
	# if len(distances) > 100:
	# 	diff = distances[-1] - distances.pop(0)
	# 	if diff < 0.01:
	# 		doRun = False

#	text = "{time}\t{m1x}\t{m1y}\t{m2x}\t{m2y}\t{w1x}\t{w1y}\t{w2x}\t{w2y}\n"

#	text = text.format(time = t, m1x = pos[0].x, m1y = pos[0].y,
#						  m2x = pos[1].x, m2y = pos[1].y, 
#						  w1x = pos[2].x, w1y = pos[2].y, 
#						  w2x = pos[3].x, w2y = pos[3].y)
#	outfile.write(text)
	t += dt
	nsteps += 1
	if nsteps % 10 == 0:
		elems = b.getElements()
		wheel1.center = (elems[2].x,elems[2].y)
		wheel2.center = (elems[3].x,elems[3].y)
		point1.center = (elems[0].x,elems[0].y)
		point2.center = (elems[1].x,elems[1].y)
		spr1.set_xdata([elems[2].x,elems[3].x,elems[0].x,elems[1].x,elems[3].x])
		spr2.set_xdata([elems[1].x,elems[2].x,elems[0].x])
		spr1.set_ydata([elems[2].y,elems[3].y,elems[0].y,elems[1].y,elems[3].y])
		spr2.set_ydata([elems[1].y,elems[2].y,elems[0].y])
		time_text.set_text('time = %.1f' % t)
		#dist_text.set_text('distance = %.3f' % i)
		axes.set_xlim(elems[0].x-2,elems[0].x+12)
		#mpl.title()
		mpl.draw()
	if b.touches(surface):
		doRun = False
	if t > 10:
		doRun = False

mpl.ioff()
mpl.show()

