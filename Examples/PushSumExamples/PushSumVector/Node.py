import Network as netwrk
import Message as msg
import vectorUtils as vector
from random import choice

class Node(object):

    Net = None
    pos = None
    alpha = None
    list_xj = None
    list_stat = None

    def __init__(self, Net, n):
        self.Net = Net
        self.pos = n
        self.alpha = Net.getAlpha()
        self.list_xj = []
        self.list_xj = Net.getXj()
        self.list_stat = []
        self.list_stat.append(0.0)

    def sendMessage(self,r):
        #start the algorithm
        vr = self.Net.getVr(self.pos,r-1) #calculate vti as sum(vr) in round t-1
        vr = vector.mul(vr,self.alpha)
        m =  msg.Message(r,v=vr) # create a new message to send it with vti * alpha-share
        self.Net.sendMessage(m) # send to all 

    def calculateS(self, r):
        sumVr = vector.sum(self.Net.getVr(self.pos,r),self.Net.getVr(self.pos,(r-1)))
        si = vector.sumElems(vector.mulVector(sumVr,self.list_xj))
        return si

    def calculateW(self,r):
        return len(self.Net.getVr(self.pos,r))

    def calculateEstimate(self,r):
        si = self.calculateS(r)
        wi = self.calculateW(r)
        print "Node %d in round %d"%(self.pos,r)
        self.list_stat.append(si/wi)

    def getEstimate(self, rd):
        print "round: %d"%rd
        print "size: %d"%len(self.list_stat)
        return self.list_stat[rd]

    def main(self,n):
            self.sendMessage(n)
            self.calculateEstimate(n)

