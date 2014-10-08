import vectorUtils
import time

class Node(object):

    list_neighbors = None
    list_Nx = None
    degree =  None
    pos = None
    net = None
    packetSize = None
    
    def __init__(self,pos,net,packetSize):    
       self.list_Nx = []
       self.pos = pos    
       self.net = net    
       self.list_neighbors = self.net.getNeighbors(self.pos)
       self.degree = len(self.list_neighbors)
       self.packetSize = packetSize


    def send(self):
       x = self.net.getX(self.pos)
       for i in range(0,len(self.list_neighbors)):
          channelC = self.net.getChannelCapacity(self.pos, list_neighbors[]i)
          if channelC > 0.0
             timetoSleep = (self.packetSize*8)/channelC
             print timetoSleep
             time.sleep(timetoSleep)
          self.net.send(x,self.list_neighbors[i])

    def getDegree(self):
      return self.degree

    def update(self):
        list_m = self.net.getM(self.pos)
        x = self.net.getX(self.pos)
        for i in range(0,len(list_m)):
           x = vectorUtils.pointWiseMinimum(x,list_m[i])
        self.net.setX(self.pos,x)

    def computeNx(self, k):
        x = self.net.getX(self.pos)
        sumX = 0.0
        for i in range(0,k):
            sumX += x[i]
        self.list_Nx.append((k-1.0)/sumX)

    def getNx(self,n):
      return self.list_Nx[n]



