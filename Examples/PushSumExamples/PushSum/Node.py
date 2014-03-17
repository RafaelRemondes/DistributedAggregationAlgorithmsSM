import Network as netwrk
import Message as msg
import time
from random import choice

class Node(object):

    Net = None
    pos = None
    list_neighbors = None
    list_stat = None

    def __init__(self, Net, n):
        self.Net = Net
        self.pos = n
        self.list_neighbors = self.Net.getNeighbors(self.pos)
        self.list_stat = []

    def sendMessage(self,r):
        #start the algortihm
        si = 0.5*self.getSumS(r-1) #1/2 sti
        wi = 0.5*self.getSumW(r-1) # 1/2 wti
        m =  msg.Message(si,wi,r) #Create a message with the parameters and the correspondent round
       # self.nrBytes += sys.getsyzeof(m)
        fi = choice(self.list_neighbors) # select a random neighbor
        self.Net.sendMessage(self.pos,m) # send to itself
        self.Net.sendMessage(fi,m) # send to selected neighbor 

    def getSumS(self,r):
        return self.Net.computeSumS(self.pos,r) # calculate sti from the round t-1

    def getSumW(self,r):
    	return self.Net.computeSumW(self.pos,r) # calculate wti from the round t-1
    
    def getEstimate(self, rd):
        for i in range(0,len(self.list_stat)):
            if self.list_stat[i].getRound() == rd :
                return self.list_stat[i].getS()
        return 0.0


    def getEstimates(self):
        return self.list_stat

    def calculateEstimate(self,r):
         s = self.getSumS(r)+self.getSumS(r-1)
         w = self.getSumW(r)+self.getSumW(r-1)
         return s/w

    def addEstimate(self,n):
        stat = msg.Message(self.calculateEstimate(n),1.0,n)
        self.list_stat.append(stat)

    def main(self,n):
        self.sendMessage(n)        
        self.addEstimate(n)
        time.sleep(0.5)
