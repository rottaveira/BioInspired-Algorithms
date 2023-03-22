#Send + More = Money
import random

def getKey(dictionary, val):
    for key, value in dictionary.items():
        if val == value:
            return key

def f(x,y):
    return x - y

def numConcat(num1, num2):  
    num1 = str(num1) 
    num2 = str(num2) 
    num1 += num2 
    return int(num1) 

def GetSample():
    return random.sample(range(0, 9), 8)

def Evaluate(sendmory):
    
    send = numConcat(numConcat(numConcat(sendmory[0],sendmory[1]),sendmory[2]),sendmory[3])
    more = numConcat(numConcat(numConcat(sendmory[4],sendmory[5]),sendmory[6]),sendmory[1])
    money= numConcat(numConcat(numConcat(numConcat(sendmory[4],sendmory[5]),sendmory[2]),sendmory[1]),sendmory[7])
    result = abs(money - (send + more))
    if result == 0:
        print(sendmory)
    return result

def Roulette(samples, qtdChildrenSamples):
    roulette_sum = sum(samples.values())
    roullete =[]
    start = 0
    
    for n in samples:
        new_start = abs(samples[n]) + start
        roullete.append([start,new_start])
        start = new_start
    
    children = [] 
    while len(children) < qtdChildrenSamples: #parar qndo hover 60 pares (não remover pais da roleta)
        parent = random.randint(0,roulette_sum)        
        for n in roullete: 
            if  parent >= n[0] and parent <= n[1]:
                item = sampleList[roullete.index(n)]
                children.append(item)
                continue
         
    print("generate children values")

def Tournment(samples, size, qtdChildrenSamples):
     
    children=[]
    while len(children) < qtdChildrenSamples:
        playersIds = random.sample(range(1, 100), size)
        players = []
        for n in playersIds:
            players.append(samples[n])
        
        children.append(sampleList[getKey(samples,max(players))])
    
    print("generate children values")

def Main():
    
    for sample in range(size):
        sampleList.append(GetSample())

    classification ={}
    for n in sampleList:
        classification.update({sampleList.index(n):Evaluate(n)})

    reordered = {k: f(max(classification.values()),v) for k, v in classification.items()}

    sortClassification = dict(sorted(reordered.items(), key=lambda x:x[1]))
    
    #Roulette(sortClassification, 120)
    Tournment(sortClassification,4,120)

size = 100
sampleList=[]
 
Main()
print("end")

