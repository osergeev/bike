#  genetic.py
  

import random



class GeneticAlgorithm(object):
   
    def __init__(self, chromosomelist):
        self.MAXRULETTEWHEELCYCLES = 1000000
        self.ALTERCONST = 2.
        self.chromosomes = chromosomelist
        
    
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
        return self.selection_roulettewheel(self.chromosomes)
    
    
    def selection_roulettewheel(self,chromosomes):
        sumfitness =  sum(chromosome.fitness for chromosome in chromosomes)
        parentlist = []
        cycles = 0
        while len(parentlist)< (len(chromosomes)/2):
            pick = random.uniform(0, sumfitness)
            current = 0
            for chromosome in self.chromosomes:
                current += chromosome.fitness
                if (current > pick) and (chromosome not in parentlist) and len(parentlist)< (len(chromosomes)/2):
                    parentlist.append(chromosome)
            if cycles > self.MAXRULETTEWHEELCYCLES:
                print "Warning! Cycles superate MAXRULETTEWHEELCYCLES, fix this situation"
                return parentlist
            cycles += 1
        return parentlist
        

    def build_randomchildren(self):
        childrenlist=[]
        chromosomesnumber = len(self.chromosomes)
        #copy chromosome list
        copychromosomeslist = self.chromosomes[:]
        for nchild in range(chromosomesnumber/2):
            #select and delete the chromosome 1
            chrom1 = copychromosomeslist.pop(random.randint(0,len(copychromosomeslist)-1))
            #select and delete the chromosome 2
            chrom2= copychromosomeslist.pop(random.randint(0,len(copychromosomeslist)-1))
            childrenlist.append(self.crossover_chromosome(chrom1,chrom2))
        return childrenlist
    
    

    # CROSSOVER FUNCTIONS
    #============================================
    
   
    
    def crossover_chromosome(self, chromosome1, chromosome2):
        #can implement check_crossovility
        childgenlist = []
        for igen in range(0,len(chromosome1.genes)):
            childgenlist.append(self.crossover_gene(chromosome1.genes[igen],chromosome2.genes[igen]))
        return Chromosome(childgenlist)

    
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
    
    #~ def mutation_chromosome(self,chromosome):
        #~ for gene in chromosome.genes:
            #~ rnd = random.random()
            #~ if rnd < self.mutationpercent:
                #~ gene.value = mutation_gene(gene)
    #~ 
    #~ 
    #~ def mutation_gene(self,gene):
        #~ # implemented for float gene only
        #~ # do mutation on value
        #~ gene.value = mutation_floatgene(gene)
    #~ 
    #~ 
    #~ def mutation_listgene(self,listgene):
        #~ pass
    #~ 
    #~ 
    #~ def mutation_floatgene(self,floatgene):
        #~ minvalue = self.floatgene.minvalue
        #~ maxvalue = self.floatgene.maxvalue
        #~ mutatedvalue = random.uniform(minvalue,maxvalue)
        #~ return mutatedvalue
        


  

class Chromosome(object):
    def __init__(self, genelist, fitness=None):
        self.genes = []
        self.fitness = fitness
        for gene in genelist:
            self.genes.append(gene)
        
    def add_gene(self,gene):
        self.genes.append(gene)
        
        
class Gene(object):
    def __init__(self, value, minvalue, maxvalue):
        self.value = value
        self.minvalue = minvalue
        self.maxvalue = maxvalue
    


def bike_to_chromosome(bike,minvaluedic,maxvaluedic):
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
    pass
    
    
def chromosome_to_bike(chromosome):
    pass
