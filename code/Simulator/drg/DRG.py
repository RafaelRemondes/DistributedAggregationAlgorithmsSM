import Network as ntw
import Node as nd
import Utils as utils
import time
import pygal
import threading
from random import choice
from math import pow,sqrt


class DRG(object):

    net = None
    nodes = []
    leaderArray = None

    class serviceNode(threading.Thread):

         pos = None
         leaderArray = None

         def __init__(self,pos,leaderArray):
              self.pos = pos
              self.leaderArray = leaderArray
              threading.Thread.__init__(self)

         def run(self):
              self.pos.start(utils.electLeader(self.leaderArray))

    def __init__(self, sample):
        self.net = ntw.Network(sample)
        list_n = self.net.getNodes()
        for i in range(0,len(list_n)):
            self.nodes.append(nd.Node(self.net,list_n[i]))
        node = choice(self.nodes)
        node.setCount()
        self.leaderArray = utils.initLeaderArray()

    def computeStat(self, n):
        list_st = []
        auxSum = 0.0
        realVal = self.net.getRealSum()
        for i in range(0,n+1):
           auxSum = 0.0
           for j in range(0,len(self.nodes)):
               node = self.nodes[j]
               print node.getCount(i)
               auxSum += pow(realVal-node.getSumPerRound(i),2)
           auxSum = auxSum/len(self.nodes)
           auxSum = sqrt(auxSum)
           auxSum = auxSum/realVal
           list_st.append(auxSum)
        return list_st

    def drawChart(self,n):
        line_chart = pygal.Line()
        line_chart.title = 'Average Estimate in each node'
        line_chart.x_labels = map(str, range(0, n+1))
        list_estimate = self.computeStat(n)
        line_chart.add('Estimate', list_estimate)
        line_chart.render_to_file('estimates.svg') 

    def start(self,n):
      list_t = []
      for i in range(0,n):
         print "New Round"
         for i in range(0,len(self.nodes)):
              thread1 = self.serviceNode(self.nodes[i],self.leaderArray)
              list_t.append(thread1)
              thread1.start()
         for i in range(0,len(list_t)):
              if list_t[i].isAlive():
                 list_t[i].join()

d = DRG("sample1.xml") 
d.start(100)
d.drawChart(100)
