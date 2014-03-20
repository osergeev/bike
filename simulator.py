import numpy as np
import random as R
import sys
import matplotlib.pyplot as mpl

from geometry import *
from surface import Surface
from bike import Bike
# import visualizer as vis

# try:
# 	from bike import Bike
#	from chromosome import Chromosome
# 	from ga import GeneticAlgorithm
#	from visual import Draw
# except:
# 	print "Not enough modules for simulation"
# 	sys.exit(1)

class Simulator(object):
	def __init__(self, surface):
		self._surface = surface

	def getSurface(self):
		return self._surface

	def getTime(self):
		return self._t

	def getBikePos(self):
		return self._bikepos

	def run(self, gen, nbike, bike, dt):
		self._bike = bike
		self._t = 0.0
		self._initpos = bike.getElements()[0].x
		distances = [0]

		# Visualization
		surfacepoints = self._surface.getPoints()
		mpl.ion()
		figure = mpl.figure()
		axes = figure.add_subplot('111',aspect='equal')
		xs, ys = zip(*surfacepoints)
		mpl.plot(xs,ys,linewidth=3)

		axes.set_ylim(-10,10)
		ngen_text = axes.text(0.02, 0.95, '', transform=axes.transAxes)
		bike_text = axes.text(0.02, 0.90, '', transform=axes.transAxes)
		time_text = axes.text(0.02, 0.85, '', transform=axes.transAxes)
		dist_text = axes.text(0.02, 0.80, '', transform=axes.transAxes)
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
		point2 = mpl.Circle((0,0), radius=0.1,color='r')
		point2.center = (elems[1].x,elems[1].y)
		axes.add_patch(point2)

		doRun = True
		maxdist = self._surface.getDistance()
		nsteps = 0
		while doRun:
			self._bike.step(dt, self._surface)
			self._t += dt
			nsteps += 1

			if nsteps % 20 == 0:
				elems = self._bike.getElements()
				wheel1.center = (elems[2].x,elems[2].y)
				wheel2.center = (elems[3].x,elems[3].y)
				point1.center = (elems[0].x,elems[0].y)
				point2.center = (elems[1].x,elems[1].y)
				spr1.set_xdata([elems[2].x,elems[3].x,elems[0].x,elems[1].x,elems[3].x])
				spr2.set_xdata([elems[1].x,elems[2].x,elems[0].x])
				spr1.set_ydata([elems[2].y,elems[3].y,elems[0].y,elems[1].y,elems[3].y])
				spr2.set_ydata([elems[1].y,elems[2].y,elems[0].y])
				ngen_text.set_text('Ngen = %d' % gen)
				bike_text.set_text('Nbike = %d' % nbike)
				time_text.set_text('time = %.1f' % self._t)
				dist_text.set_text('distance = %.3f' % (elems[0].x - self._initpos))
				axes.set_xlim(elems[0].x-2,elems[0].x+12)
				#mpl.title()
				mpl.draw()

			rundist = self._bike.getElements()[0].x - self._initpos
			if rundist >= maxdist:
				doRun = False
			distances.append(rundist)
			if len(distances) > 10000:
				diff = distances[-1] - distances.pop(0)
				if diff < 0.01:
					doRun = False
			if self._bike.touches(self._surface):
				doRun = False

		mpl.ioff()
		mpl.close(figure)

		fit = distances[-1]
		if fit > maxdist:
			fit += 100 / self._t

		return fit


if __name__ == "__main__":
	nbikes = 20
	timestep = 0.001
	distance = 100
	height = 30

	surf = Surface(distance, height)
	sim = Simulator(surf)

	bikes = []
	for i in xrange(nbikes):
	 	m2x = 2 * R.random() - 1
	 	m2y = 2 * R.random() - 1
	 	w1x = 2 * R.random() - 1
	 	w1y = 2 * R.random() - 1
	 	w1r = 0.2 + R.random() * 0.5
	 	w2x = 2 * R.random() - 1
	 	w2y = 2 * R.random() - 1
	 	w2r = 0.2 + R.random() * 0.5
	 	Dm1m2 = 5000 + 20000 * R.random()
	 	Dm1w1 = 5000 + 20000 * R.random()
	 	Dm1w2 = 5000 + 20000 * R.random()
	 	Dm2w1 = 5000 + 20000 * R.random()
	 	Dm2w2 = 5000 + 20000 * R.random()
	 	Dw1w2 = 5000 + 20000 * R.random()

		c = [Point(m2x, m2y), Point(w1x, w1y), w1r, Point(w2x, w2y), w2r,
			Dm1m2, Dm1w1, Dm1w2, Dm2w1, Dm2w2, Dw1w2]
		b = Bike(c, Point(2, 2))
		bikes.append(b)

	# c = [Point[-0.5, 0], Point(-1, 1), 0.5, Point(-1, -1.5), 0.5, 100, 100, 100, 100, 100, 100]

	generation = 1 		# show generation in the corner
	doRunAll = True		# a button to stop the simulation?
	while doRunAll:
		nbike = 1
		for b in bikes:
			fit = sim.run(generation, nbike, b, timestep)
			b.setFitness(fit)
			nbike += 1

		# nextgen = GeneticAlgorithm(bikes)
		nextgen = bikes

		generation += 1

		if generation > 1:
			break

		bikes = nextgen

	mpl.show()
