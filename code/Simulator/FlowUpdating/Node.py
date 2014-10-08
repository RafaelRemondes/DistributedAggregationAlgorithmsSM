import time
from random import uniform

class Node(object):

    list_neighbours_avg = None
    list_neighbours_size =  None
    value = None
    size = None
    pos =  None
    net = None
    list_stat = None
    list_size = None
    list_sum =  None


    def __init__(self,pos,net):
        self.pos = pos
        self.net = net
        self.list_neighbours_avg = []
        self.list_neighbours_size =[]
        aux = self.net.getNeighbors(self.pos)
        self.value = self.net.getVal(self.pos)
        self.size = 0.0
        self.list_stat = []
        self.list_size = []
        self.list_sum = []
        self.list_stat.append(self.value)
        self.list_size.append(0.0)
        self.list_sum.append(0.0)
        for i in range(0,len(aux)):
            self.list_neighbours_avg.append((aux[i],0.0,0.0))
            self.list_neighbours_size.append((aux[i],0.0,0.0))

    def getFlows(self):
        aux = 0.0
        for i in range(0,len(self.list_neighbours_avg)): 
          aux += self.list_neighbours_avg[i][1]
        return aux 

    def setSize(self, size):
        self.size = size

    def getValue(self):
        return self.value

    def getLastAvg(self):
        return self.list_stat[len(self.list_stat)-1]

    def getAvgPerRound(self,n):
        return self.list_stat[n]

    def getSizePerRound(self,n):
        size = 0.0
        if self.list_size[n] > 0.0:
           size = pow(self.list_size[n],-1)
        return size

    def getSumPerRound(self,n):
        return self.list_sum[n]

    def send(self):
        for i in range(0,len(self.list_neighbours_avg)):
            dest = self.list_neighbours_avg[i][0]
            fij = self.list_neighbours_avg[i][1]
            eij = self.list_neighbours_avg[i][2]
            typo = "avg" 
            m = (dest,self.pos,fij,eij, typo)
            self.net.sendMessage(m)
            dest = self.list_neighbours_size[i][0]
            fij = self.list_neighbours_size[i][1]
            eij = self.list_neighbours_size[i][2]
            typo = "size" 
            m = (dest,self.pos,fij,eij, typo)
            self.net.sendMessage(m)


    def updateFijEij(self,list_m):
        for i in range(0,len(list_m)):
            for j in range(0,len(self.list_neighbours_avg)):
                # Update the flows, average
                if self.list_neighbours_avg[j][0] == list_m[i][1] and list_m[i][4] == "avg":
                    aux_fij = -list_m[i][2]
                    aux_triple = (list_m[i][1],aux_fij,list_m[i][3])
                    self.list_neighbours_avg[j] = aux_triple
                # Update the flows, size
                if self.list_neighbours_size[j][0] == list_m[i][1] and list_m[i][4] == "size":
                    aux_fij = -list_m[i][2]
                    aux_triple = (list_m[i][1],aux_fij,list_m[i][3])
                    self.list_neighbours_size[j] = aux_triple


    def computeEi(self, typo):
        sumF = 0.0
        sumE = 0.0
        if typo == "avg":
           for i in range(0,len(self.list_neighbours_avg)):
               sumF += self.list_neighbours_avg[i][1]
               sumE += self.list_neighbours_avg[i][2]
           aux_dif = self.value - sumF
           ei = (aux_dif+sumE)/(len(self.list_neighbours_avg)+1.0)
        if typo == "size":
           for i in range(0,len(self.list_neighbours_size)):
               sumF += self.list_neighbours_size[i][1]
               sumE += self.list_neighbours_size[i][2]
           aux_dif = self.size - sumF
           ei = (aux_dif+sumE)/(len(self.list_neighbours_size)+1.0)
        return ei
   
    def updateEi(self,ei_avg, ei_size):
        for i in range(0,len(self.list_neighbours_avg)):
            aux_fij = self.list_neighbours_avg[i][1] + (ei_avg-self.list_neighbours_avg[i][2]) 
            #if aux_fij == ei:
            self.list_neighbours_avg[i] = (self.list_neighbours_avg[i][0],aux_fij,ei_avg)
        for i in range(0,len(self.list_neighbours_avg)):
            aux_fij = self.list_neighbours_size[i][1] + (ei_size-self.list_neighbours_size[i][2]) 
            #if aux_fij == ei:
            self.list_neighbours_size[i] = (self.list_neighbours_size[i][0],aux_fij,ei_size)
            

    def compute(self):
        list_m = self.net.getMessages(self.pos)
        self.updateFijEij(list_m)
        ei_avg = self.computeEi("avg")
        ei_size = self.computeEi("size")
        self.updateEi(ei_avg,ei_size)

    def computeSize(self):
        aux = 0.0
        for i in range(0,len(self.list_neighbours_size)):
            aux+=self.list_neighbours_size[i][1]
        aux = self.size-aux
        self.list_size.append(aux)

    def computeStat(self):
        aux = 0.0
        for i in range(0,len(self.list_neighbours_avg)):
            aux+=self.list_neighbours_avg[i][1]
        aux = self.value-aux
        self.list_stat.append(aux)

    
    def computeSum(self):
        aux = 0.0
        if self.list_size[len(self.list_size)-1] > 0.0:
           aux = self.list_stat[len(self.list_stat)-1]/self.list_size[len(self.list_size)-1]
        else: 
            aux = self.list_stat[len(self.list_stat)-1]
        self.list_sum.append(aux)

    def clearInbox(self):
    	self.net.clearInbox(self.pos)

    def getAvgPerRound(self,n):
        return self.list_stat[n]

    def printFlows(self):
        s = ""
        s = "Node "+str(self.pos)
        s = s + "\n"
        for i in range(0,len(self.list_neighbours_avg)):
            s = s + str(self.list_neighbours_avg[i])
            s = s + "\n"
        s = s + "\n"
        self.net.log(s)

    def start(self):
        self.send()
        time.sleep(1)
        self.compute()
        self.computeStat()
        self.computeSize()
        self.computeSum()
        #self.printFlows()
