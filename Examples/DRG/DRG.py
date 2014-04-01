import Network as ntw
import Node as nd
import Utils as utils
import time
import pygal
import threading
from math import pow,sqrt


class DRG(object):

    net = None
    nodes = []
    leaderArray = None

    class serviceNode(threading.Thread):

         pos = None
         rd = None
         leaderArray = None

         def __init__(self,pos,rd,leaderArray):
              self.pos = pos
              self.rd = rd
              self.leaderArray = leaderArray
              threading.Thread.__init__(self)

         def run(self):
              for i in range(0,self.rd):
                   self.pos.start(i,utils.electLeader(self.leaderArray))
                   time.sleep(1)

    def __init__(self, n):
        self.net = ntw.Network(n)
        list_n = self.net.getNodes()
        for i in range(0,len(list_n)):
            self.nodes.append(nd.Node(self.net,list_n[i]))
        self.leaderArray = utils.initLeaderArray()

    def computeStat(self, n):
        list_st = []
        auxSum = 0.0
        realVal = self.net.getAverage()
        for i in range(0,n):
            list_st.append(0.0)
        for i in range(0,len(self.nodes)):
            node = self.nodes[i]
            for j in range(0,n):
                #calculate the estimator = square((sum (realVal-estimated)^2)/n)
                auxSum += pow((realVal-node.getEstimate(j+1)),2)
                auxSum = auxSum/len(self.nodes)
                list_st[j] = sqrt(auxSum)
        return list_st

    def drawChart(self,n):
        line_chart = pygal.Line()
        line_chart.title = 'Average Estimate in each node'
        line_chart.x_labels = map(str, range(1, n+1))
        list_estimate = self.computeStat(n)
        line_chart.add('Estimate', list_estimate)
        line_chart.render_to_file('estimates.svg') 

    def printN(self):
      for i in range(0,len(self.nodes)):
        self.nodes[i].printLenV()

    def start(self,n):
         for i in range(0,len(self.nodes)):
              thread1 = self.serviceNode(self.nodes[i],n,self.leaderArray)
              thread1.start()

d = DRG(500) 
d.start(20)
time.sleep(60)
d.drawChart(20)
