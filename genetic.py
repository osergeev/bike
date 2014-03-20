"""genetic.py 
Library for Genetic Algorithm 
"""
DEFLIMIT = 2.0

import random

class Generation(object):
    ''' Generation is used as main interface to interact with the library.
            INPUT: Fit
    
    '''
    def __init__(self, vallstlst=[], fitnesslst=[], minlst=None, maxlst=None):
        self.memberlst = []
        self.fitnesslst = fitnesslst
        self.minlst = minlst
        self.maxlst = maxlst
        for i in range(0,len(vallstlst)):
            self.build_member(vallstlst[i],fitnesslst[i],minlst,maxlst)
                
        def set_memberlst(self, memberlst):
            ''' Set '''
            self.memberlst = memberlst
        
        def add_memberlst(self, memberlst):
            self.memberlst += memberlst
            
        
        def add_member(self, member):
            self.memberlst.append(member)
        
        
        def build_member(self, vallst, fitness, minlst=None, maxlst=None):
            chromosome = []
            if minlst == None:
                minlst = self.minlst
            if maxlst == None:
                maxlst = self.maxlst
            for i in range(len(vallst)):
                val = vallst[i]
                try:
                    minval = minlst[i]
                except:
                    minval = None
                try:
                    maxval = maxlst[i]
                except:
                    maxval = None
                gene = Gene(val, minval, maxval)
                chromosome.append(gene)
            member = Member(chromosome,fitness)        
            self.memberlst.append(member)
        
        
        def next(self):
            ga = GeneticAlgorithm(self.memberlst)
            return ga.run_ga()


class GeneticAlgorithm(object):
   
    def __init__(self, memberlst):
        self.MAXRULETTEWHEELCYCLES = 1000000
        self.ALTERCONST = 2.
        self.memberlst = memberlst
        self.MUTPERCENT = 10.
        
    
    def check_limits(self,val,minval,maxval):
        if val < minval:
            return minval
        elif val > maxval:
            return  maxval
        else:
            return val
    
    
    def run_ga(self):
        parents = self.selection_parent()
        
        children = self.build_randomchildren()
        return parents + children
        


    # SELECTION FUNCTIONS
    #============================================
    
    def selection_parent(self):
        #only is implemented roulette wheel selector
        return self.selection_roulettewheel()
    
     
    def selection_roulettewheel(self):
        sumfitness =  sum(member.fitness for member in self.memberlst)
        parentlst = []
        cycles = 0
        while len(parentlst)< (len(self.memberlst)/2):
            pick = random.uniform(0, sumfitness)
            current = 0
            for member in self.memberlst:
                current += member.fitness
                if (current > pick) and (member not in parentlst) and len(parentlst)< (len(self.memberlst)/2):
                    parentlst.append(member)
            if cycles > self.MAXRULETTEWHEELCYCLES:
                print "Warning! Cycles superate MAXRULETTEWHEELCYCLES, fix this situation"
                return parentlst
            cycles += 1
        return parentlst
        

    def build_randomchildren(self):
        childrenlst=[]
        membernumber = len(self.memberlst)
        #copy chromosome lst
        cpmemberlst = self.memberlst[:]
        for nchild in range(len(self.memberlst)/2):
            #select and delete the parent 1
            parent1 = cpmemberlst.pop(random.randint(0,len(cpmemberlst)-1))
            #select and delete the parent 2
            parent2= cpmemberlst.pop(random.randint(0,len(cpmemberlst)-1))
            childrenlst.append(self.crossover_chromosome(parent1.chromosome,parent2.chromosome))
        return childrenlst
    
    

    # CROSSOVER FUNCTIONS
    #============================================
    
    def crossover_chromosome(self, chromosome1, chromosome2):
        #can implement check_crossovility
        childgenlst = []
        for igen in range(0,len(chromosome1)):
            crossgen = self.crossover_gene(chromosome1[igen],chromosome2[igen])
            # mutation of gen 
            crossgen = self.mutation_gene(crossgen)
            childgenlst.append(crossgen)
            
        return Member(childgenlst)

    
    def crossover_gene(self,gene1,gene2):
        if type(gene1.val)!=type(gene2.val):
            print "ERROR: genes with different types"
            exit()
        if isinstance(gene1.val,float):
            return self.crossover_floatgene(gene1,gene2)
        elif isinstance(gene1.val,list):
            return self.crossover_lstgene(gene1,gene2)
        else:
            print "ERROR: Type of gene is not defined"
            exit()

    
    def crossover_lstgene(self,lstgene1,lstgene2):
        rndselector = random.random()
        # gaussian center in 0 x ALTERCONST
        rndalter = random.gauss(0,0.3) * self.ALTERCONST
        lstnewgene = []
        # random number select one of the two input lst of genes
        if rndselector < 0.5:
            lstgeneselect = lstgene1
        else:
            lstgeneselect = lstgene2
        # iterate over all genes in the selected lst of genes
        for item in lstgeneselect:
            newval = self.check_limits(item.val + rndalter,item.minval,item.maxval)
            newlstgene.append(Gene(newval,item.minval,item.maxval))
        return newlstgene
            
        
    def crossover_floatgene(self,floatgene1,floatgene2):    
        rndselector = random.random()
        # gaussian center in 0 x ALTERCONST
        rndalter = random.gauss(0,0.3) * self.ALTERCONST
        if rndselector < 0.5:
            newval = self.check_limits(floatgene1.val + rndalter,floatgene1.minval,floatgene1.maxval)
            return Gene(newval,floatgene1.minval,floatgene1.maxval)
        else:
            val = floatgene2.val + rndalter
            minval = floatgene2.minval
            maxval = floatgene2.maxval
            newval = self.check_limits(val,minval,maxval)
            return Gene(newval,floatgene2.minval,floatgene2.maxval)
           
            
    # MUTATION FUNCTIONS
    #============================================
    #
    def mutation_gene(self,gene):
        # implemented for float gene only
        # do mutation on val
        rnd = random.random() * 100.0
        if rnd > self.MUTPERCENT:
            return gene
        else:
            if isinstance(gene.val,float):
                gene.val = (self.mutation_floatgene(gene))
                return gene
            elif isinstance(gene.val,list):
                gene.val = (self.mutation_lst(gene))
                return gene
            
    
    def mutation_lstgene(self,lstgene):
        mutvallst = []
        for gene in lstgene:
            newval = uniform(gene.minval, gene.maxval)
            mutvallst.append(newval)
        return mutvallst
            
    
    def mutation_floatgene(self,floatgene):
        minval = floatgene.minval
        maxval = floatgene.maxval
        mutval = random.uniform(minval,maxval)
        return mutval

        
class Member(object):
    def __init__(self, genelst, fitness=None):
        self.chromosome = genelst
        self.fitness = fitness
        
    def get_chrom(self):
        genevallst = []
        for gene in self.chromosome:
            genevallst.append(gene.val)
        return genevallst
        
        
class Gene(object):
    def __init__(self, val, minval=None, maxval=None):
        self.val = val
        
        if minval == None:
            if isinstance(val,float):
                self.minval(val-DEFLIMIT)
            elif isinstance(val,list):
                #buil a lst of dimension of gene
                self.minval([val-DEFLIMIT]*len(val))
        else:
            self.minval = minval
            
        
        if maxval == None:
            if isinstance(val,float):
                self.maxval(val+DEFLIMIT)
            elif isinstance(val,list):
                #build a lst of dimension of gene
                self.maxval([val+DEFLIMIT]*len(val))
        else:
            self.maxval = maxval
        
 

#~ def bike_to_chromosome(bike,minvaldic,maxvaldic):
    #~ gene00 = Gene(bike.p0.val,minvaldic["p00"],maxvaldic["p00"])
    #~ gene01 = Gene(bike.p0.val,minvaldic["p01"],maxvaldic["p01"])
    #~ gene02 = Gene(bike.p0.val,minvaldic["p02"],maxvaldic["p02"])
    #~ gene03 = Gene(bike.p0.val,minvaldic["p03"],maxvaldic["p03"]) 
    #~ gene04 = Gene(bike.p0.val,minvaldic["p04"],maxvaldic["p04"])
    #~ gene05 = Gene(bike.p0.val,minvaldic["p05"],maxvaldic["p05"]) 
    #~ gene06 = Gene(bike.p0.val,minvaldic["p06"],maxvaldic["p06"])
    #~ gene07 = Gene(bike.p0.val,minvaldic["p07"],maxvaldic["p07"])
    #~ gene08 = Gene(bike.p0.val,minvaldic["p08"],maxvaldic["p08"])
    #~ gene09 = Gene(bike.p0.val,minvaldic["p09"],maxvaldic["p09"]) 
    #~ pass
    #~ 
    #~ 
#~ def chromosome_to_bike(chromosome):
    #~ pass
