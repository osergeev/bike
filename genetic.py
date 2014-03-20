#  genetic.py
DEFLIMIT = 2.0

import random

class Generation(object):
        def __init__(self, valuelistlist=[], fitnesslist=[], minlist=None, maxlist=None):
            self.memberlist = []
            self.fitnesslist = fitnesslist
            self.minlist = minlist
            self.maxlist = maxlist
            for i in range(0,len(valuelistlist)):
                self.build_member(valuelistlist[i],fitnesslist[i],minlist,maxlist)
                
        def set_memberlist(self, memberlist):
            self.memberlist = memberlist
        
        def add_memberlist(self, memberlist):
            self.memberlist += memberlist
            
        
        def add_member(self, member):
            self.memberlist.append(member)
        
        
        def build_member(self, valuelist, fitness, minlist=None, maxlist=None):
            chromosome = []
            if minlist == None:
                minlist = self.minlist
            if maxlist == None:
                maxlist = self.maxlist
            for i in range(len(valuelist)):
                value = valuelist[i]
                try:
                    minvalue = minlist[i]
                except:
                    minvalue = None
                try:
                    maxvalue = maxlist[i]
                except:
                    maxvalue = None
                gene = Gene(value, minvalue, maxvalue)
                chromosome.append(gene)
            member = Member(chromosome,fitness)        
            self.memberlist.append(member)
        
        
        def next(self):
            ga = GeneticAlgorithm(self.memberlist)
            return ga.run_ga()


class GeneticAlgorithm(object):
   
    def __init__(self, memberlist):
        self.MAXRULETTEWHEELCYCLES = 1000000
        self.ALTERCONST = 2.
        self.memberlist = memberlist
        self.MUTPERCENT = 10.
        
    
    def check_limits(self,value,minvalue,maxvalue):
        if value < minvalue:
            return minvalue
        elif value > maxvalue:
            return  maxvalue
        else:
            return value
    
    
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
        sumfitness =  sum(member.fitness for member in self.memberlist)
        parentlist = []
        cycles = 0
        while len(parentlist)< (len(self.memberlist)/2):
            pick = random.uniform(0, sumfitness)
            current = 0
            for member in self.memberlist:
                current += member.fitness
                if (current > pick) and (member not in parentlist) and len(parentlist)< (len(self.memberlist)/2):
                    parentlist.append(member)
            if cycles > self.MAXRULETTEWHEELCYCLES:
                print "Warning! Cycles superate MAXRULETTEWHEELCYCLES, fix this situation"
                return parentlist
            cycles += 1
        return parentlist
        

    def build_randomchildren(self):
        childrenlist=[]
        membernumber = len(self.memberlist)
        #copy chromosome list
        cpmemberlist = self.memberlist[:]
        for nchild in range(len(self.memberlist)/2):
            #select and delete the parent 1
            parent1 = cpmemberlist.pop(random.randint(0,len(cpmemberlist)-1))
            #select and delete the parent 2
            parent2= cpmemberlist.pop(random.randint(0,len(cpmemberlist)-1))
            childrenlist.append(self.crossover_chromosome(parent1.chromosome,parent2.chromosome))
        return childrenlist
    
    

    # CROSSOVER FUNCTIONS
    #============================================
    
    def crossover_chromosome(self, chromosome1, chromosome2):
        #can implement check_crossovility
        childgenlist = []
        for igen in range(0,len(chromosome1)):
            crossgen = self.crossover_gene(chromosome1[igen],chromosome2[igen])
            # mutation of gen 
            crossgen = self.mutation_gene(crossgen)
            childgenlist.append(crossgen)
            
        return Member(childgenlist)

    
    def crossover_gene(self,gene1,gene2):
        if type(gene1.value)!=type(gene2.value):
            print "ERROR: genes with different types"
            exit()
        if isinstance(gene1.value,float):
            return self.crossover_floatgene(gene1,gene2)
        elif isinstance(gene1.value,list):
            return self.crossover_listgene(gene1,gene2)
        else:
            print "ERROR: Type of gene is not defined"
            exit()

    
    def crossover_listgene(self,listgene1,listgene2):
        rndselector = random.random()
        # gaussian center in 0 x ALTERCONST
        rndalter = random.gauss(0,0.3) * self.ALTERCONST
        listnewgene = []
        # random number select one of the two input list of genes
        if rndselector < 0.5:
            listgeneselect = listgene1
        else:
            listgeneselect = listgene2
        # iterate over all genes in the selected list of genes
        for item in listgeneselect:
            newvalue = self.check_limits(item.value + rndalter,item.minvalue,item.maxvalue)
            newlistgene.append(Gene(newvalue,item.minvalue,item.maxvalue))
        return newlistgene
            
        
    def crossover_floatgene(self,floatgene1,floatgene2):    
        rndselector = random.random()
        # gaussian center in 0 x ALTERCONST
        rndalter = random.gauss(0,0.3) * self.ALTERCONST
        if rndselector < 0.5:
            newvalue = self.check_limits(floatgene1.value + rndalter,floatgene1.minvalue,floatgene1.maxvalue)
            return Gene(newvalue,floatgene1.minvalue,floatgene1.maxvalue)
        else:
            value = floatgene2.value + rndalter
            minvalue = floatgene2.minvalue
            maxvalue = floatgene2.maxvalue
            newvalue = self.check_limits(value,minvalue,maxvalue)
            return Gene(newvalue,floatgene2.minvalue,floatgene2.maxvalue)
           
            
    # MUTATION FUNCTIONS
    #============================================
    #
    def mutation_gene(self,gene):
        # implemented for float gene only
        # do mutation on value
        rnd = random.random() * 100.0
        if rnd > self.MUTPERCENT:
            return gene
        else:
            if isinstance(gene.value,float):
                gene.value = (self.mutation_floatgene(gene))
                return gene
            elif isinstance(gene.value,list):
                gene.value = (self.mutation_list(gene))
                return gene
            
    
    def mutation_listgene(self,listgene):
        mutvaluelist = []
        for gene in listgene:
            newvalue = uniform(gene.minvalue, gene.maxvalue)
            mutvaluelist.append(newvalue)
        return mutvaluelist
            
    
    def mutation_floatgene(self,floatgene):
        minvalue = floatgene.minvalue
        maxvalue = floatgene.maxvalue
        mutvalue = random.uniform(minvalue,maxvalue)
        return mutvalue

        
class Member(object):
    def __init__(self, genelist, fitness=None):
        self.chromosome = genelist
        self.fitness = fitness
        
    def get_chrom(self):
        genevaluelist = []
        for gene in self.chromosome:
            genevaluelist.append(gene.value)
        return genevaluelist
        
        
class Gene(object):
    def __init__(self, value, minvalue=None, maxvalue=None):
        self.value = value
        
        if minvalue == None:
            if isinstance(value,float):
                self.minvalue(value-DEFLIMIT)
            elif isinstance(value,list):
                #buil a list of dimension of gene
                self.minvalue([value-DEFLIMIT]*len(value))
        else:
            self.minvalue = minvalue
            
        
        if maxvalue == None:
            if isinstance(value,float):
                self.maxvalue(value+DEFLIMIT)
            elif isinstance(value,list):
                #build a list of dimension of gene
                self.maxvalue([value+DEFLIMIT]*len(value))
        else:
            self.maxvalue = maxvalue
        
 

#~ def bike_to_chromosome(bike,minvaluedic,maxvaluedic):
    #~ gene00 = Gene(bike.p0.value,minvaluedic["p00"],maxvaluedic["p00"])
    #~ gene01 = Gene(bike.p0.value,minvaluedic["p01"],maxvaluedic["p01"])
    #~ gene02 = Gene(bike.p0.value,minvaluedic["p02"],maxvaluedic["p02"])
    #~ gene03 = Gene(bike.p0.value,minvaluedic["p03"],maxvaluedic["p03"]) 
    #~ gene04 = Gene(bike.p0.value,minvaluedic["p04"],maxvaluedic["p04"])
    #~ gene05 = Gene(bike.p0.value,minvaluedic["p05"],maxvaluedic["p05"]) 
    #~ gene06 = Gene(bike.p0.value,minvaluedic["p06"],maxvaluedic["p06"])
    #~ gene07 = Gene(bike.p0.value,minvaluedic["p07"],maxvaluedic["p07"])
    #~ gene08 = Gene(bike.p0.value,minvaluedic["p08"],maxvaluedic["p08"])
    #~ gene09 = Gene(bike.p0.value,minvaluedic["p09"],maxvaluedic["p09"]) 
    #~ pass
    #~ 
    #~ 
#~ def chromosome_to_bike(chromosome):
    #~ pass
