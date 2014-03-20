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
   
    def __init__(self, bikelst, minlst, maxlst):
         self.bikelst = bikelst
         self.minlst = minlst
         self.maxlst = maxlst
         chromosomelst = []
         fitnesslst = []
         for bike in bikelst:
            chromosomelst.append(bike.getChromosome())
            fitnesslst.append(bike.getFitness())
        self.chromosomelst = chromosomelst
        self.fitnesslst = fitnesslst
        
        
    def next(self):
        """ Return a list, that contains new generation of bikes. The 
        number of bikes generated is the same of the input bike number. 
        """
        ga = Generation(self, self.chromosomelst, self.fitnesslst, 
                self.minlst, self.maxlst)
        newgeneration = ga.next()
        newbikelst = []
        for member in newgeneration:
            # a bike is generated with a new chromosome and point(2,2) 
            #reference as default.
            bike = Bike(member.get_chrom(), Point(2, 2))
            newbikelst.append(bike)
        return newbikelst
