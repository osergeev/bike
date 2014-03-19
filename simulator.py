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
	def __init__(self, bike, surface):
		self._bike = bike
		self._surface = surface

	def getSurface(self):
		return self._surface

	def getTime(self):
		return self._t

	def getBikePos(self):
		return self._bikepos

	def run(self, bike, surface, dt = 0.01):
		self._bike = bike
		self._surface = surface
		self._t = 0.0
		self._bikepos = Point(2, 2)
		positions = [self._bikepos.x - 2]

		doRun = True
		while doRun:
			self._bikepos = self._bike.update(self._surface, self._bikepos, dt)
			self._t += dt
			vis.draw(self)

			rundist = self._bikepos.x - 2
			if rundist >= 100:
				doRun = False
			positions.append(rundist)
			if len(positions) > 100
				diff = positions[-1] - positions.pop(0)
				if diff < 0.1:
					doRun = False
			if self._bike.touches(self._surface, self._bikepos)
				doRun = False

		fit = positions[-1]
		if fit > self._surface.getDistance():
			fit += 200 / self._t

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


