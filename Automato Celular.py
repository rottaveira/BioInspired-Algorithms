from random import *
from operator import itemgetter
import matplotlib.pyplot as plt

ELEMENT_SIZE = 100
QTDNEIGHBORS = 1
randBinList = lambda n: [randint(0,1) for b in range(1,n+1)]

#regra de transição
MAP = {'000' : 1, '001' : 0, '010' : 1, '011' : 0, '100' : 0, '101' : 1, '110' : 0, '111' : 1}
 
#reticulado
def Neighbors(position):
    
    right =[]
    left =[]
    for i in range(1,QTDNEIGHBORS+1):
        
        #condições de contorno periódicas (ciclica)
        #obs: pode ser implementado não periodica 
        # (crio algum meio para o ultimo elemento, sem retornar para o primeiro. 
        #  Pode ser null ou algum valor fixo por exemplo)
        if position == ELEMENT_SIZE-1:
           right.append(sample[i-1])
           left.append(sample[position-i])
        elif position == 0:
            right.append(sample[position-1])
            left.append(sample[(ELEMENT_SIZE-1) - i])
        else:
            right.append(sample[position+i])
            left.append(sample[position-i])
 
    got = ''.join(map(str, left)) + str(sample[position]) + ''.join(map(str, right))
    return got
           
def Procriate():
    
    initPosition = randint(0,ELEMENT_SIZE-1) 
    actualPosition = initPosition

    newsample = [0] * ELEMENT_SIZE
    for i in range(ELEMENT_SIZE):
        
        newsample[actualPosition] = MAP[Neighbors(actualPosition)]

        if actualPosition == ELEMENT_SIZE-1:
            actualPosition = 0
        else:
            actualPosition += 1
    
        if actualPosition == initPosition:
            break

    print(''.join(map(str, newsample)))
    return newsample
   

#Espaço celular
sample = randBinList(ELEMENT_SIZE)
final =[]
for i in range(100):
    sample = Procriate()
    final.append(sample)

# plotagem da grade final
plt.imshow(final, cmap="binary")
plt.show()