import numpy as np
import random as R
import sys

from surface import Surface
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

	def run(self, bike, dt = 0.01):
		self._bike = bike
		self._t = 0.0
		self._initpos = bike.getPositions()[0]
		distances = [0]

		doRun = True
		maxdist = self._surface.getDistance()
		while doRun:
			self._bike.step(dt, self._surface)
			self._t += dt
			# vis.draw(self)

			self._bikepos = self._bike.getPositions()[0]
			rundist = self._bikepos.x - self._initpos.x
			if rundist >= maxdist:
				doRun = False
			distances.append(rundist)
			if len(distances) > 100:
				diff = distances[-1] - distances.pop(0)
				if diff < 0.01:
					doRun = False
			if self._bike.touches(self._surface):
				doRun = False

		fit = distances[-1]
		if fit > maxdist:
			fit += 100 / self._t

		return fit


if __name__ == "__main__":
	nbikes = 20
	timestep = 0.01
	distance = 100
	height = 30

	surf = Surface(distance, height)

	# bikes = []
	# for i in xrange(nbikes):
	# 	...
	# 	c = Chromosome(...)
	# 	b = Bike(c)
	# 	bikes.append(b)

	# c = [Point[-0.5, 0], Point(-1, 1), 0.5, Point(-1, -1.5), 0.5, 100, 100, 100, 100, 100, 100]

	generation = 1 		# show generation in the corner
	doRunAll = True		# a button to stop the simulation?
	while doRunAll:
		# for b in bikes:
		# 	fit = Simulator.run(b, surf)
		# 	b.setFitness(fit)

		# nextgen = GeneticAlgorithm(bikes)

		generation += 1

		if generation > 100:
			break

		# bikes = nextgen


