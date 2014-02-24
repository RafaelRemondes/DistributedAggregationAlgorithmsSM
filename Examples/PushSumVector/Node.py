import Network as netwrk
import Message as msg
import vectorUtils as vector
from random import choice

class Node(object):

    Net = None
    pos = None
    nodesToBroadcast = {}

    def __init__(self, Net, n):
        self.Net = Net
        self.pos = n
        self.list_neighbors = self.Net.getNodes()

    def sendMessage(self,r):
        #start the algorithm
        vr = self.Net.getVr(r) #calculate vti as sum(vr) in round t-1
        m =  msg.Message(vr,r) # create a new message to send it with vti * alpha-share
        self.Net.sendMessage(m) # send to selected neighbor
    
    def average(self,r):
        #compute the avarage
    	return vector.sumElems(self.Net.computeS(ps))/vector.sumElems(self.Net.computeW())

    def main(self,n):

            self.sendMessage(n)
            print 'AVERAGE %d in round %d'%(self.average(n),n)
