import Network as netwrk
import time
from random import choice

class Node(object):

    Net = None
    pos = None
    list_neighbors = None
    s = None
    w = None
    list_stat = None
    list_sums = None

    def __init__(self, Net, n):
        self.Net = Net
        self.pos = n
        self.s = self.Net.getVal(self.pos)
        self.w = 0.0
        self.list_neighbors = self.Net.getNeighbors(self.pos)
        self.list_stat = []
        self.list_sums = []
        self.list_sums.append(self.s)

    def setW(self, val):
      self.w = val

    def getSumS(self):
        return self.computeSumS() # calculate sti from the round t-1

    def getSumW(self):
      return self.computeSumW() # calculate wti from the round t-1
    
    def getEstimate(self, rd):
      return self.list_stat[rd]

    def getEstimates(self):
        return self.list_stat

    def getSum(self):
        return self.list_sums

    def getSumPerRound(self,rd):
      return self.list_sums[rd]

    def computeSumS(self):
      list_m = self.Net.getMessages(self.pos)
      s = "Node "
      sum = 0.0
      s = s + str(self.pos)
      for i in range(0,len(list_m)):
            s = s + "\n"
            s = s + str(list_m[i])
            sum += list_m[i][0]
      self.Net.printS(s)
      return sum

    def computeSumW(self):
      list_m = self.Net.getMessages(self.pos)
      n = len(list_m)
      sum = 0.0
      for i in range(0,len(list_m)):
            sum += list_m[i][1]
      return sum


    def sendMessage(self,r):
        #start the algorithm
        si = 0.5*self.s #1/2 sti
        wi = 0.5*self.w # 1/2 wti
        m =  (si,wi) #Create a message with the parameters and the correspondent round
       # self.nrBytes += sys.getsyzeof(m)
        fi = choice(self.list_neighbors) # select a random neighbor
        self.Net.sendMessage(fi,m) # send to selected neighbor 
        self.Net.sendMessage(self.pos,m) # send to itself
    
    
   # def calculateEstimate(self,r):
    #     s = self.getSumS(r)+self.getSumS(r-1)
     #    w = self.getSumW(r)+self.getSumW(r-1)
      #   if w > 0.0:
       #    return s/w
        # else:
         #  return s

    def addEstimate(self,n):
        self.list_stat.append(self.calculateEstimate(n))

    def addSum(self, r):
        self.s = self.getSumS()#+self.s
        self.w = self.getSumW()#+self.w
        if self.w > 0.0:
           self.list_sums.append(self.s/self.w)
        else:
           self.list_sums.append(self.s)



    def main(self,n):
        self.sendMessage(n)
        time.sleep(0.1)        
        #self.addEstimate(n)
        self.addSum(n)
        self.Net.clearInbox(self.pos)

     
