import Network as netwrk
import Message as msg
from random import choice

class Node(object):

    Net = None
    pos = None
    list_neighbors = {}

    def __init__(self, Net, n):
        self.Net = Net
        self.pos = n
        self.list_neighbors = self.Net.getNeighbors(self.pos)

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
    
    def average(self,r):
        #compute the avarage
    	if self.Net.computeSumW(self.pos,r) > 0:
           return self.Net.computeSumS(self.pos,r)/self.Net.computeSumW(self.pos,r)
        else:
           return 1
    
    def estimate(self,r):
         s = self.getSumS(r)+self.getSumS(r-1)
         w = self.getSumW(r)+self.getSumW(r-1)
         return s/w

    def main(self,n):
        self.sendMessage(n)
        st = self.estimate(n)
        dif = self.Net.getRealVal()-st 
        print 'Estimate: %.2f in round %d'%(st,n)
        print 'Difference from real average: %.2f'%dif     
