#test_ga.py
from genetic import *
import matplotlib.pyplot as plt
import random


class Eq1(object):
    """ parabole with max in 30.0 """
    def __init__(self):
        self.bestval = 10000.0
        self.minval = 10.0
        self.maxval = 50.0

    def get_result(self,x):
        return self.eq1(x)
        
    def eq1(self, x):
        return -10.0*(x-30.0)*(x-30.0)+10000.0
        
class Eq2(object):
    """ between -2 and 2 the max is on 0 with a value of 10 """
    def __init__(self):
        self.bestval = 10.0
        self.minval = -2.0
        self.maxval = 2.0

    def get_result(self,x):
        return self.eq2(x)
        
    def eq2(self, x):
        return x**4 - 10*x**2 + 9
        
class Eq3(object):
    """ vector function with eq1 = x, eq2 = y """
    def __init__(self):
        self.eq1 = Eq1()
        self.eq2 = Eq2()
        self.bestval = self.eq1.bestval + self.eq2.bestval
        self.minval = [self.eq1.minval,self.eq2.minval]
        self.maxval = [self.eq1.maxval,self.eq2.maxval]
        
    def get_result(self, vallst):
        
        return  self.eq1.get_result(vallst[0]) + self.eq2.get_result(vallst[1])
        

        
class TestGA(object):
    def __init__(self, neq, nmember, ngeneration):
        self._nmember = nmember
        self._ngeneration = ngeneration
        self._eq = neq
        
    def run(self):  
        #build member
        if self._eq == 1:
            eq = Eq1()
        elif self._eq == 2:
            eq = Eq2()
        elif self._eq == 3:
            eq = Eq3()
        else:
            print "Select an equation"
            exit
        valuelist = []
        fitnesslist = []
        for i in range(self._nmember):
            if self._eq == 1 or self._eq == 2:
                value = random.uniform(eq.minval,eq.maxval)
            elif self._eq == 3:
                value = [random.uniform(eq.minval[0],eq.maxval[0]),random.uniform(eq.minval[1],eq.maxval[1])]

            valuelist.append([value])
            fitnesslist.append(eq.get_result(value))  
        ga = Generation()
        for i in range(len(valuelist)):
            ga.build_member(valuelist[i],fitnesslist[i],[eq.minval],[eq.maxval]) 
        newgeneration = ga.next()
        xlist = []
        ylist = []
        for ngeneration in range(0,self._ngeneration):
            h = 0
            maxfit = 0
            fitnesslist = []
            valuelistlist = []
            for member in newgeneration:
                h += 1
                for gene in member.chromosome:
                    fitness = eq.get_result(gene.val)
                    fitnesslist.append(fitness)
                    valuelistlist.append([gene.val])
                if fitness > maxfit:
                    maxfit = fitness
                    
            ga = Generation(valuelistlist,fitnesslist,[eq.minval],[eq.maxval])
            newgeneration = ga.next()
            
            xlist.append(ngeneration)
            ylist.append(maxfit)
        plt.plot(xlist,ylist, 'ro')
        plt.axis([0, self._ngeneration, 0, eq.bestval])
        plt.show()
    
        
test1 = TestGA(1, 20, 100)

test1.run()






