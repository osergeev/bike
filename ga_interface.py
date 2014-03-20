"""ga_interface.py
connect simulation with genetic library.
"""

from genetic import *
from bike import *
from geometry import *



class BikeGeneration(object):
    """Use to connect with genetic library. 
    
    Keyword arguments:
    bikelst -- list of bike objects
    minlst -- list with minima values with same format of bike chromosome
    maxlst -- list with maxima values with same form of bike chromosome
    """
   
    def __init__(self, bikelst):
        self.bikelst = bikelst
        self.minlst = [[-1, -1], [-1, -1], 0.2, [-1, -1], 0.2,
            5000, 5000, 5000, 5000, 5000, 5000] # fill!
        self.maxlst = [[1, 1], [1, 1], 0.7, [1, 1], 0.7,
            25000, 25000, 25000, 25000, 25000, 25000]
        chromosomelst = []
        fitnesslst = []
        for bike in bikelst:
            c = bike.getChromosome()
            c_internal = [[c[0].x, c[0].y], [c[1].x, c[1].y], c[2],
                [c[3].x, c[3].y], c[4], c[5], c[6], c[7], c[8], c[9], c[10]]
            chromosomelst.append(c_internal)
            fitnesslst.append(bike.getFitness())
        self.chromosomelst = chromosomelst
        self.fitnesslst = fitnesslst
        
        
    def next(self):
        """ Return a list, that contains new generation of bikes. The 
        number of bikes generated is the same of the input bike number. 
        """
        ga = Generation(self.chromosomelst, self.fitnesslst, 
                self.minlst, self.maxlst)
        newgeneration = ga.next()
        newbikelst = []
        for member in newgeneration:
            # a bike is generated with a new chromosome and point(2,2) 
            #reference as default.
            c_internal = member.get_chrom()
            c = [Point(c_internal[0][0], c_internal[0][1]),
                Point(c_internal[1][0], c_internal[1][1]), c_internal[2],
                Point(c_internal[3][0], c_internal[3][1]), c_internal[4],
                c_internal[5], c_internal[6], c_internal[7],
                c_internal[8], c_internal[9], c_internal[10]]
            bike = Bike(c, Point(2, 2))
            newbikelst.append(bike)
        return newbikelst
