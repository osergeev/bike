from geometry import *
from bike import Bike
import random as R

def geneticAlgorithm(bikes, numfinest):
	chromosomes = getChromosomes(bikes)
	finest = selectFinest(chromosomes, numfinest)
	return nextGen(finest, len(bikes))

def getChromosomes(bikes):
	chromosomes = {}
	for b in bikes:
		fit = b.getFitness()
		c = b.getChromosome()
		chromosomes[fit] = c
	return chromosomes

def selectFinest(chrom, numfinest):
	keys = chrom.keys()
	keys.sort()
	chosenkeys = keys[-numfinest:]
	return [chrom[x] for x in chosenkeys]

def nextGen(best, nbikes):
	nextGen = []
	n = 0
	nc = len(best)
	while n < nbikes:
		n1 = R.randrange(nc)
		n2 = R.randrange(nc)
		if n1 == n2:
			continue
		c1 = best[n1]
		c2 = best[n2]
		c = crossover(c1, c2)
		c = mutate(c)
		b = Bike(c, Point(2, 2))
		nextGen.append(b)
		n += 1
	return nextGen

def crossover(c1, c2):
	newc = []
	for i in xrange(11):
		# if isinstance(c1[i], Point):
		# 	newG = crossPoints(c1[i], c2[i])
		# else:
		# 	newG = crossFloats(c1[i], c2[i])
		newG = c1[i] + (c1[i] - c2[i]) * 0.5
		newG += (c2[i] - c1[i]) * (2 * R.random())
		newc.append(newG)
	applyConstraints(newc)
	return newc

# def crossPoints(p1, p2):
# 	b = p1 + (p1 - p2) * 0.5
# 	return b + (p2 - p1) * (2 * R.random())

# def crossFloats(v1, v2):
# 	v = v1 + (v1 - v2) * 0.5
# 	return v + (v2 - v1) * (2 * R.random())

def applyConstraints(c):
	newc = c[:]
	if c[2] < 0.25:
		newc[2] = 0.25
	if c[4] < 0.25:
		newc[4] = 0.25
	if c[5] < 3000:
		newc[5] = 3000
	if c[6] < 3000:
		newc[6] = 3000
	if c[7] < 3000:
		newc[7] = 3000
	if c[8] < 3000:
		newc[8] = 3000
	if c[9] < 3000:
		newc[9] = 3000
	if c[10] < 3000:
		newc[10] = 3000
	return newc

def mutate(c):
	newc = c[:]
	for i in xrange(11):
		if R.random() > 0.02:
			continue
		else:
			if i == 0 or i == 1 or i == 3:
				randx = 2 * R.random() - 1
				randy = 2 * R.random() - 1
				newc[i] = Point(randx, randy)
			if i == 2 or i == 4:
				randr = 0.2 + 0.5 * R.random()
				newc[i] = randr
			if i > 4:
				randD = 3000 + 25000 * R.random()
				newc[i] = randD
	return newc
