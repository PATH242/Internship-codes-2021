import random
import matplotlib.pyplot as plt
import numpy as np

##the constants used
generationSize=10
probabilityOfMutation=20
probabilityOfMating=60
mutationValues=[-1,1] ##helper values that are multiplied in random numbers
##n is size of the data array, numberOfGenerations is a counter to count the generations made so far
n=0
minimumAcceptedErrorValue= 100 ##error value is fitness
numberOfGenerations: int=0
##e is a list for the errors going to be processed and d is for days
e=[]
d=[]
population= list()

class Individual:
    ##fitness is the error value, the lower the fitness the better
    ##genes are the constants of the line equation: genes[0] + genes[1] * x
    def __init__(self, x,y):
        self.genes= [x,y]
        self.fitness= self.calculateFitness()
    ##after mating, mutation could occure, and then fitness is calculated
    def  mate(self, temp):
        x= random.randint(0,50)
        y= random.randint(0,50)
        child= Individual(x,y)
        child.genes[0]= (self.genes[0]+temp.genes[0])/2.0
        child.genes[1]=(self.genes[1]+temp.genes[1])/2.0
        child.mutate()
        child.fitness= child.calculateFitness()
        return child

    ##mutation occurs with the probability of mutation specified above
    def mutate(self):
        probability= random.randint(0,99)
        if(probability<probabilityOfMutation):
            self.genes[0]+= mutationValues[random.randint(0,1)]*random.randint(0,10)

        probability= random.randint(0,99)
        if(probability<probabilityOfMutation):
            self.genes[1]+= mutationValues[random.randint(0,1)]*random.randint(0,10)

    ##fitness is the difference between the expected e[i] and the actual e[i] squared
    def calculateFitness(self):
        temp= 0.0
        for i in range(0,n):
            tempDif= self.genes[0]+ self.genes[1]*d[i]
            tempDif-=e[i]
            temp+= (tempDif)*(tempDif)
        return temp
    ##to output the individual when needed
    def __str__(self):
        return (str(self.genes[0])+" "+str(self.genes[1])+" with fitness of: "+str(self.fitness)+"\n")

    ##for comparison used in sorting, we define lower than and greater than operators
    def __lt__(self, right):
        return self.fitness < right.fitness
    def __gt__(self, right):
        return self.fitness > right.fitness

##we create a random initial population to start with
def makeInitialPopulation():
    global population
    for i in range(generationSize):
        population.append(Individual( random.randint(i,40+i), random.randint(i,40+i)))


def selectAdvancedIndividuals():
    global population
    ##sort to have least fit regression line first
    population.sort()
    population.reverse()
    ##make a new population to store children
    newPopulation= list()
    temp = Individual(random.randint(0,50),random.randint(0,50))
    probability = 0
    ##mating with giving most similar higher probability in mating
    i= len(population)-1
    while(i>=0):
        j= i-1
        while(j>=0):
            probability= (random.randint(0,99))+i*2 ##give higher probability in mating to most fit individuals
            if(probability>=probabilityOfMating):
                temp= population[i].mate(population[j])
                newPopulation.append(temp)

            j-=1

        i-=1

    ##sort to have most fit first
    newPopulation.sort()

    ##eliminate from the new population so that it suits the generation size
    while(len(newPopulation)>generationSize):
        newPopulation.pop()

    population= newPopulation

##read data from file and store it in lists
def readData():
    global n
    n=195
    data = open('dataIN.txt', 'r')
    lines = data.readlines()
    data.close()
    base: int = ord('0')
    top: int = 0
    for i in range(195):
        j= 0
        temp=0
        temp2=0
        while j<len(lines[i]):
            if(lines[i][j]=='\t'):
                break
            temp*=10
            top= ord(lines[i][j])
            temp+= (top-base)
            j+=1
        j+=1
        while j<len(lines[i]):
            temp2*=10
            top = ord(lines[i][j])
            temp2 += (top - base)
            j+=1
        e.append(temp)
        d.append(temp)


def start():
    readData()
    makeInitialPopulation()
    global numberOfGenerations


    for i in range(1000):
        numberOfGenerations +=1
        selectAdvancedIndividuals()
        ##if we reach an optimal Individual, break
        if(population[0].fitness<=minimumAcceptedErrorValue):
            break
    print("the total fitness is: " +str(population[0].fitness))
    ##plot actual values
    plt.scatter(d,e, label="actualValues", color="green", marker=".", s=10)

    ## Creating vectors X and Y
    x = np.linspace(0, 600, 100)
    y= population[0].genes[0] + population[0].genes[1] * x
    ##plot the regression line
    plt.plot(x,y,label= "expected")
    plt.xlabel('days')
    plt.ylabel('errors')
    plt.title('visualization of data')

    plt.show()
    return

start()
