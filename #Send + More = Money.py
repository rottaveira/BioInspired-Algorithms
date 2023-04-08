#Send + More = Money
import math
import random

ELEMENT_SIZE = 10
POPULATION_SIZE = 100
POPULATION=[]
TX_CROSSOVER = math.ceil(POPULATION_SIZE *.6)
TX_PARENTS = math.ceil(POPULATION_SIZE*.4)
MAX_GENERATIONS = 50
MAX_EXECUTIONS = 1000

def getKey(dictionary, val):
    for key, value in dictionary.items():
        if val == value:
            return key

def subtract(x,y):
    return x - y

def GetSample():
    #return random.sample(range(0, 9), 8)
    return random.sample(range(0, 10), ELEMENT_SIZE)
'''
use the vector size as the same of char qtd. It will facilitate the crossover step when apply the circular approach.
''' 

def JoinNumbers(numeros):
    return int(''.join(map(str, numeros)))

def Evaluate(sendmory): 
    # check if is a valid entry
    if len(set(sendmory + [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])) != 10:
        return None
    
    send = JoinNumbers([sendmory[0], sendmory[1], sendmory[2], sendmory[3]])
    more = JoinNumbers([sendmory[4], sendmory[5], sendmory[6], sendmory[1]])
    money = JoinNumbers([sendmory[4], sendmory[5], sendmory[2], sendmory[1], sendmory[7]])
    result = abs(money - (send + more)) 
    return result


def Roulette(samples, qtdparentsSamples):
    roulette_sum = sum(samples.values())
    roullete =[]
    start = 0
    
    for n in samples:
        new_start = abs(samples[n]) + start
        roullete.append([start,new_start])
        start = new_start
    
    parents = [] 
    while len(parents) < qtdparentsSamples: #parar qndo hover x pares (não remover pais da roleta)
        parent = random.randint(0,roulette_sum)        
        for n in roullete: 
            if  parent >= n[0] and parent <= n[1]:
                item = POPULATION[roullete.index(n)]
                parents.append(item)
                break
         
    return parents

def Tournment(samples, tour, qtdparentsSamples):
     
    parents=[]
    while len(parents) < qtdparentsSamples:
        players = random.sample(list(samples.values()), tour)         
        parents.append(POPULATION[getKey(samples,max(players))])
    
    return parents

#need improvement
def Truncating(samples, canRepeat, txElitism):
    
    candidates = samples[0:txElitism]
    parents = []
    while len(parents) < txElitism:
        player = random.sample(range(0, len(candidates), 1))
        if canRepeat:
            parents.Append(candidates[player])
        else:
            parents.Append(candidates.pop(player))
    
    return parents

def NormalizeChildren(children, parent):
    if children == 'empty':
        return parent
    else:
        return children
    
def CiclicCrossover(parents, uniqueParents=True):
    childrens = []
    while(len(childrens) < TX_CROSSOVER):
      
        players = random.sample(parents, 2) 
        dad = players[0]
        mom = players[1]

        if uniqueParents:
            parents.remove(players[0])
            parents.remove(players[1])
         
        sampleSize = len(dad)
        children1 = ['empty'] * sampleSize
        children2 = ['empty'] * sampleSize
        sortedValues = []
        parentStart = random.randint(0,sampleSize-1)        
        for i in range(0,sampleSize):
           
            if len(sortedValues) == 0:
                    sortedValues.append(dad[parentStart])
 
            index = dad.index(sortedValues[i])
            dadElement = dad[index]
            momElement = mom[index]
            
            sortedValues.append(momElement)                            
            children1[index] = momElement
            children2[index] = dadElement

            if momElement == sortedValues[0]:
                childrens.append(list(map(NormalizeChildren, children1, dad)))
                childrens.append(list(map(NormalizeChildren, children2, mom)))
                break
    
    Mutation(childrens)
    return childrens

def Mutation(childrens, percent=5): 

    elements = random.sample(range(0, len(childrens)), percent)

    for element in elements:
        random_list = [random.randint(0, ELEMENT_SIZE-1), random.randint(0, ELEMENT_SIZE-1)]
        childrens[element][random_list[0]],childrens[element][random_list[1]] = childrens[element][random_list[1]],childrens[element][random_list[0]]
    
    return childrens

class data:
    def __init__(self):
        self.generation = set()
        self.solutions = set()
        self.bests = {}
    
    @property
    def qtdSolutions(self):
        return len(self.solutions)

if __name__ == '__main__':
    
    resultData=[]
    for attempt in range(MAX_EXECUTIONS):
        POPULATION.clear()
        result = data()  
        m = 0
        for sample in range(POPULATION_SIZE):  
            POPULATION.append(GetSample())

        classification ={}    
        generation = 0
        
        for n in range(MAX_GENERATIONS):
            m=0
            for n in POPULATION:
                if n[4] == 0:
                    m += 1
                evaluate = Evaluate(n)
                if evaluate == 0:
                    print(n)
                    solution =''.join(map(str,n))
                    
                    if solution not in result.solutions:
                        result.generation.add(generation)
                        result.solutions.add(solution) 
                    
                classification.update({POPULATION.index(n):evaluate})

            goodValues = list(sorted(filter(lambda x: x < 1000,list(classification.values()))))
            haveSolution = list(filter(lambda x: x == 0,list(classification.values())))
            result.bests[generation] = goodValues
            print('Generation: '+str(generation))
            print('Greatest: '+str(min(classification.values())))
            print(str(len(goodValues)) +' under 1000')
            print(goodValues)
            print('M == 0: '+str(m))
            print('Have '+str(len(haveSolution))+' solution(s)\n')

            #min
            sortMinClassification = dict(sorted(classification.items(), key=lambda x:x[1]))
            bestSamples = [POPULATION[sample] for sample in  list({k: sortMinClassification[k] for k in list(sortMinClassification)[:TX_PARENTS]}.keys())]
            #Min to max classification
            reclassificated = {k: subtract(max(classification.values())+1,v) for k, v in classification.items()}
            sortMaxClassification = dict(sorted(reclassificated.items(), key=lambda x:x[1]))
            
            #parents = Roulette(sortMaxClassification, POPULATION_SIZE)
            parents = Tournment(sortMinClassification,3,POPULATION_SIZE)
            #Truncating(classification,False,60)

            POPULATION.clear()
            POPULATION.extend(bestSamples)
            POPULATION.extend(CiclicCrossover(parents))
            generation += 1
    
        resultData.append(result)

    positiveExecutions = len([x for x in resultData if x.qtdSolutions > 0])
    positiveExecutionsWithMoreofOneResults = len([x for x in resultData if x.qtdSolutions > 1])
    premature = len([x for x in resultData if x.qtdSolutions > 0 and min(x.generation) < 25])
    print('end')

''' 
COCA+COLA=OASIS

1000 execuções / 50 gerações:
Rolleta - 
acertos: 38,7% 
multiplos acertos: 16,8%
prematuros: 96%

Torneio - Tour 2
acertos: 6,2% 
multiplos acertos: 3%
prematuros: 1,9%



'''