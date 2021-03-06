import random
import matplotlib.pyplot as plt
import numpy as np


##the constants used
generationSize=10
probabilityOfMutation=20
probabilityOfMating=60
mutationValues=[-1,1]
##n is size of the data array, numberOfGenerations is a counter to count the generations made so far
n=0
minimumAcceptedErrorValue= 49 ##Error is fitness
numberOfGenerations: int=0
##e[N] is a list for the errors going to be processed and d[N] is for days
e=[]
d=[]
totalFitness=0
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
    """if at any point, we find that our equation fits at least 10 points optimally,
        we plot that line as a separate world and then continue trying to generate the 
        optimal line for the rest of the points"""
    def calculateFitness(self):
        temp= 0.0
        global n
        global totalFitness
        for i in range(0,n):
            tempDif= self.genes[0]+ self.genes[1]*d[i]
            tempDif-=e[i]
            if(i>8 and temp<=minimumAcceptedErrorValue and temp + (tempDif*tempDif) > minimumAcceptedErrorValue):
                ##print(str(e[0])+' '+str(e[i-1])+' '+ str(self.genes[0])+' '+str(self.genes[1]))
                a = np.linspace(d[0], d[i-1], 100)
                b = self.genes[0] + self.genes[1]*a
                plt.plot(a,b, label="expected")
                while i>=0:
                    e.pop(0)
                    d.pop(0)
                    n-=1
                    i-=1
                totalFitness+=temp
                return self.calculateFitness()
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
        population.append(Individual(random.randint(i, 40 + i), random.randint(i, 40 + i)))


def selectAdvancedIndividuals():
    global population
    ##sort to have least fit regression line first
    population.sort()
    population.reverse()
    ##make a new population to store children
    newPopulation= list()
    temp = Individual(random.randint(0,50),random.randint(0,50))
    probability = 0
    ##mating with giving the most fit a higher probability in mating
    i= len(population)-1
    while(i>=0):
        j= i-1
        while(j>=0):
            probability= (random.randint(0,99))+i*2
            if(probability>=probabilityOfMating):
                temp= population[i].mate(population[j])
                newPopulation.append(temp)

            j-=1

        i-=1
    for i in newPopulation:
        i.fitness= i.calculateFitness()
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
    plt.scatter(d, e, label="actualValues", color="black", marker=".", s=10)
    plt.xlabel('days')
    plt.ylabel('errors')
    plt.title('visualization of data')
    makeInitialPopulation()
    global numberOfGenerations
    selectAdvancedIndividuals()

    for i in range(1000):
        numberOfGenerations +=1
        selectAdvancedIndividuals()
        ##if we represented all our data, break
        if(len(e)==0):
            break
    ##if there's still one more line we didn't represent, represent it
    if(len(e)>0):
        a = np.linspace(d[0], d[len(e)-1], 100)
        b = population[0].genes[0] + population[0].genes[1] * a
        plt.plot(a, b, label="expected")
        global totalFitness
        for i in range(0,len(d)):
            temp= (population[0].genes[0]+population[0].genes[1]*d[i])
            temp-= e[i]
            totalFitness+= (temp*temp)


    print("total fitness is: "+str(totalFitness))
    plt.show()

    return

start()
