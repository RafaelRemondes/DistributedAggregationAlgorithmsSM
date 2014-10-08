import Network as ntw
import Node as nd
import threading
import time
from random import choice
from math import sqrt, pow


class FlowUpdating(object):
    
    net = None
    nodes = None

    class serviceNode(threading.Thread):

       pos = None

       def __init__(self,pos,rd):
          self.pos = pos
          threading.Thread.__init__(self)

       def run(self):
           self.pos.start()

    def __init__(self,n):
        self.net = ntw.Network(n)
        self.nodes = []
        aux = self.net.getNodes()
        for i in range(0,len(aux)):
            self.nodes.append(nd.Node(aux[i],self.net))

    def computeStat(self,n):
      list_stat = []
      realAvg =  self.net.getAvg()
      aux = 0.0
      for i in range(0,n):
        for j in range(0,len(self.nodes)):
          aux += pow(realAvg-self.nodes[j].getAvgPerRound(i),2)
        aux = sqrt(aux/len(self.nodes))
        aux = (aux/realAvg)*100.0
        print aux
        list_stat.append(aux)
    

    def start(self, n):
     for j in range(0,n):
        sum_avg = 0.0
        sum_vi = 0.0
        sum_flows = 0.0
        for i in range(0, len(self.nodes)):
           self.nodes[i].clearInbox()
           sum_avg += self.nodes[i].getLastAvg()
           sum_vi  += self.nodes[i].getValue()
           sum_flows += (self.nodes[i].getValue()-self.nodes[i].getFlows())
        print "AVG: %.2f FLOWS:%.2f SUM:%.2f"%(sum_avg,sum_flows,sum_vi)
        if sum_avg == sum_flows == sum_vi:
           print "true"
        else:
           print "false"
        list_t = []
        for i in range(0, len(self.nodes)):
           thread1 = self.serviceNode(self.nodes[i],n)
           thread1.start()
           list_t.append(thread1)
        for i in range(0, len(list_t)):
           if list_t[i].isAlive():
              list_t[i].join()


f = FlowUpdating(40)
f.start(20)
time.sleep(25)
f.computeStat(20)

