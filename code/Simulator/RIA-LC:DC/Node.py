from random import uniform
import time
import math

class Node(object):

    Net = None
    v_m = None
    val = None
    pos = None
    list_neighbors = None
    list_sum =  None
    degree = None

    def __init__(self,Net,pos):
        self.Net = Net
        self.pos = pos
        self.list_sum = []
        m =  self.Net.getM()
        self.v_m = []
        self.list_neighbors = self.Net.getNeighbors(self.pos)
        self.val = self.Net.getVal(self.pos)
        for i in range(0,int(m)):
            self.v_m.append(0)
        self.list_sum.append(self.val)
        self.degree = len(self.list_neighbors)
        self.computeSketch()
    
    def computeSketch(self):
        for i in range(0,self.val):
            index = uniform(0.0,self.Net.getM()-1.0)
            self.v_m[int(index)] = 1
    
    def getDegree(self):
      return self.degree
    
    def getSum(self,n):
        return self.list_sum[n]

    def send(self):
     for i in range(0,len(self.list_neighbors)):
          m = (self.list_neighbors[i],self.v_m)
          self.Net.sendMessage(m,m[0])

    def orOperand(self, a,b):
        for i in range(0,len(a)):
            a[i] = a[i] or b[1][i]
        return a

    def computeSum(self):
        m = int(self.Net.getM())
        sumatorium = 0
        list_m = self.Net.getMessages(self.pos)
        for i in range(0,len(list_m)):
            self.v_m = self.orOperand(self.v_m,list_m[i])
        for i in range(0,len(self.v_m)):
            if self.v_m[i] == 0:
                sumatorium += 1
        vn = float(sumatorium)/float(m)
        sumatorium = -m*math.log(vn)
        self.list_sum.append(sumatorium)

    def printSum(self):
        print self.list_sum[len(self.list_sum)-1]


    def main(self):
        self.send()
        time.sleep(0.5)
        self.computeSum()
        self.Net.clearInbox(self.pos)
