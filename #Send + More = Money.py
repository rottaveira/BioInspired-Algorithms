#Send + More = Money
import random

def getKey(dictionary, val):
    for key, value in dictionary.items():
        if val == value:
            return key

def subtract(x,y):
    return x - y

def numConcat(num1, num2):  
    num1 = str(num1) 
    num2 = str(num2) 
    num1 += num2 
    return int(num1) 

def GetSample():
    #return random.sample(range(0, 9), 8)
    return random.sample(range(0, 10), 10)
'''
use the vector size as the same of char qtd. It will facilitate the crossover step when apply the circular approach.
'''

def Evaluate(sendmory):
    
    send = numConcat(numConcat(numConcat(sendmory[0],sendmory[1]),sendmory[2]),sendmory[3])
    more = numConcat(numConcat(numConcat(sendmory[4],sendmory[5]),sendmory[6]),sendmory[1])
    money= numConcat(numConcat(numConcat(numConcat(sendmory[4],sendmory[5]),sendmory[2]),sendmory[1]),sendmory[7])
    result = abs(money - (send + more))
    if result == 0:
        print(sendmory)
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
                item = sampleList[roullete.index(n)]
                parents.append(item)
                break
         
    return parents

def Tournment(samples, tour, qtdparentsSamples):
     
    parents=[]
    while len(parents) < qtdparentsSamples:
        players = random.sample(list(samples.values()), tour)         
        parents.append(sampleList[getKey(samples,max(players))])
    
    return parents

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
    while(len(parents) > 0):
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
        
    return Mutation(childrens)

def Mutation(childrens):
    for element in childrens:
        random_list = [random.randint(0, len(element)-1), random.randint(0, len(element)-1)]
        element[random_list[0]],element[random_list[1]] =element[random_list[1]],element[random_list[0]]
    return childrens
    
def Main(): 

    for sample in range(size):  
        sampleList.append(GetSample())

    classification ={}    
    generation = 0
    while any(v == 0 for v in classification.values()) == False:
        
        print('Generation: '+str(generation))
        
        for n in sampleList:
            classification.update({sampleList.index(n):Evaluate(n)})

        print('Greatest: '+str(min(classification.values())))

        #Min to max classification
        reclassificated = {k: subtract(max(classification.values())+1,v) for k, v in classification.items()}
        sortClassification = dict(sorted(reclassificated.items(), key=lambda x:x[1]))
        
        #parents = Roulette(sortClassification, size)
        parents = Tournment(sortClassification,4,size)
        #Truncating(classification,False,60)
        sampleList.clear() 
        sampleList.extend(CiclicCrossover(parents))
        generation = generation+1

    print('searched on '+str(generation)+' generation')

size = 100
sampleList=[]
 
Main()
print("end")

