#test_ga.py

from genetic import *
import matplotlib.pyplot as plt


def asign_fitness(fac):
    return -10.0*(float(fac)-30.0)*(float(fac)-30.0)+10000.0


genlist = []
chromosomeslist = []
for i in range(10,20,1):
    value = float(i)
    gen = [Gene(value,10.0,50.0)]
    chromosomeslist.append(Chromosome(gen,asign_fitness(value)))
    
newlist = chromosomeslist

h = 0
for i in newlist:
    h += 1
    print h
    print i.genes[0].value, i.fitness

xlist = []
ylist = []

for ngeneration in range(0,100):
    GA = GeneticAlgorithm(chromosomeslist)
    newlist = GA.run_ga()
    
    print "\n"
    h = 0

    maxfit = 0
    for i in newlist:
        h += 1
        print h
        
        print i.genes[0].value , asign_fitness(i.genes[0].value)
        if asign_fitness(i.genes[0].value) > maxfit:
            maxfit = asign_fitness(i.genes[0].value)
        
    xlist.append(ngeneration)
    ylist.append(maxfit)
        



plt.plot(xlist,ylist, 'ro')
plt.axis([0, 100, 0, 10000])
plt.show()

#~ for i in range(0,100):
    #~ print i, asign_fitness(i)
#~ 







