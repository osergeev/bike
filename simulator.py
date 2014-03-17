import numpy as np
import random as R
import sys

# try:
# 	from bike import Bike
#	from chromosome import Chromosome
# 	from ga import GeneticAlgorithm
#	from visual import Draw
# except:
# 	print "Not enough modules for simulation"
# 	sys.exit(1)

class SurfaceElement(object):
	def __init__(self, p,  tg):
		pass

class Surface(object):
	def __init__(self, dist, h):
		elements = []

	def 

if __name__ == "__main__":
	nbikes = 20
	timestep = 0.01
	distance = 100
	height = 30

	surf = Surface(distance, height)

	bikes = []
	for i in xrange(nbikes):
		...
		c = Chromosome(...)
		b = Bike(c)
		bikes.append(b)

	generation = 1 		# show generation in the corner
	doRun = True		# a button to stop the simulation?
	while doRun:
		for b in bikes:
			fit = Simulator.run(b, surf)
			b.setFitness(fit)

		nextgen = GeneticAlgorithm(bikes)

		generation += 1

		if generation > 100:
			break

		bikes = nextgen


