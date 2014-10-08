import time
from random import uniform

class Node(object):

    list_neighbours = None
    value = None
    pos =  None
    net = None
    list_stat = None

    def __init__(self,pos,net):
        self.pos = pos
        self.net = net
        self.list_neighbours = []
        aux = self.net.getNeighbors(self.pos)
        self.value = self.net.getVal(self.pos)
        self.list_stat = []
        self.list_stat.append(self.value)
        for i in range(0,len(aux)):
            self.list_neighbours.append((aux[i],0.0,0.0))

    def getFlows(self):
        aux = 0.0
        for i in range(0,len(self.list_neighbours)): 
          aux += self.list_neighbours[i][1]
        return aux 

    def getValue(self):
        return self.value

    def getLastAvg(self):
        return self.list_stat[len(self.list_stat)-1]

    def send(self):
        for i in range(0,len(self.list_neighbours)):
            dest = self.list_neighbours[i][0]
            fij = self.list_neighbours[i][1]
            eij = self.list_neighbours[i][2]
            m = (dest,self.pos,fij,eij)
            self.net.sendMessage(m)

    def updateFijEij(self,list_m):
        for i in range(0,len(list_m)):
            for j in range(0,len(self.list_neighbours)):
                if self.list_neighbours[j][0] == list_m[i][1]:
                    aux_fij = -list_m[i][2]
                    aux_triple = (list_m[i][1],aux_fij,list_m[i][3])
                    self.list_neighbours[j] = aux_triple

    def computeEi(self):
        sumF = 0.0
        sumE = 0.0
        for i in range(0,len(self.list_neighbours)):
            sumF += self.list_neighbours[i][1]
            sumE += self.list_neighbours[i][2]
        aux_dif = self.value - sumF
        ei = (aux_dif+sumE)/(len(self.list_neighbours)+1.0)
        return ei
   
    def updateEi(self,ei):
        for i in range(0,len(self.list_neighbours)):
            aux_fij = self.list_neighbours[i][1] + (ei-self.list_neighbours[i][2]) 
            self.list_neighbours[i] = (self.list_neighbours[i][0],aux_fij,ei)
            

    def compute(self):
        list_m = self.net.getMessages(self.pos)
        self.updateFijEij(list_m)
        ei = self.computeEi()
        self.updateEi(ei)

    def computeStat(self):
        aux = 0.0
        for i in range(0,len(self.list_neighbours)):
            aux+=self.list_neighbours[i][1]
        aux = self.value-aux
        self.list_stat.append(aux)

    def clearInbox(self):
    	self.net.clearInbox(self.pos)

    def getAvgPerRound(self,n):
        return self.list_stat[n]

    def start(self):
        self.send()
        time.sleep(1)
        self.compute()
        self.computeStat()
