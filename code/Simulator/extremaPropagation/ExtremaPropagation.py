import Network as ntw
import Node as nd
from random import randint,choice
import time
import pygal
import threading
from math import sqrt,pow


class ExtremaPropagation(object):

    net = None
    nodes = None
    list_stats = None
    line_chart = None

    class serviceNode(threading.Thread):

       pos = None
       k = None

       def __init__(self,pos,k):
          self.pos = pos
          self.k = k
          threading.Thread.__init__(self)

       def run(self):
          self.pos.update()
          self.pos.send()
          self.pos.computeNx(self.k)


    def __init__(self,sample,k):
        self.list_stats =[]
        self.net = ntw.Network(sample,k)
        self.nodes = []
        for i in range(0,len(self.net.getNodes())):
           self.nodes.append(nd.Node(self.net.getNodes()[i],self.net,130.0))
           self.nodes[i].send()

    def reboot(self,k, trans_type, trans_n):
       self.net = ntw.Network("sample1.xml",k)
       self.net.applyTransformation(trans_type,trans_n)
       self.nodes = []
       for i in range(0,len(self.net.getNodes())):
           self.nodes.append(nd.Node(self.net.getNodes()[i],self.net,130.0))
           self.nodes[i].send()

    def start(self,mode, n,k,nodesToRemove):
       if mode == 1: #Random node Remove
         if nodesToRemove > 0:
           for i in range(0,nodesToRemove):
             node = choice(self.nodes)
             self.nodes.remove(node)
       if mode == 2: #Node degree Remove
          self.nodes.sort(key=lambda x: x.getDegree(), reverse=True)
          for i in range(0,nodesToRemove):
            self.nodes.remove(self.nodes[i])
       for j in range(0, n):
           list_t = []
           for i in range(0, len(self.nodes)):
               thread1 = self.serviceNode(self.nodes[i],k)
               list_t.append(thread1)
               thread1.start()
           for i in range(0,len(list_t)):
               if list_t[i].isAlive():
                  list_t[i].join()

    def computeN(self,n):
        list_Nx = []
        aggregates = self.net.getAggregates()
        auxSum = 0.0
        node = choice(self.nodes)
        for i in range(0,n):
          auxSum = sqrt(pow(aggregates-node.getNx(i),2))
         # for j in range(0,len(self.nodes)):
          #  node = self.nodes[i]
           # nx = node.getNx(i)
            #auxSum +=pow((aggregates-nx),2)
         # auxSum = sqrt(auxSum/len(self.nodes))
          auxSum = (auxSum/aggregates)
          list_Nx.append(auxSum)
        return list_Nx

    
    def createChart(self,n):
       self.line_chart = pygal.Line()
       self.line_chart.title = 'Extrema Propagation results with Triangule Closure evolution strategy'
       self.line_chart.x_labels = map(str, range(1,n))

    def drawChart(self,nodesRemoved,n):
        s = str(nodesRemoved)+"edges added"
        self.line_chart.add(s, self.computeN(n))
        self.line_chart.render_to_file('estimates.svg')   


def startSimulation(mode,rd,k,e,nodesToRemove,trans_type=None, trans_n=None):
  if trans_type != None and trans_n != None:
     e.reboot(k,trans_type,trans_n)
  e.start(mode,rd,k,nodesToRemove)
  e.drawChart(trans_n,rd)
  print "Simulation complete"



k = 10000
e = ExtremaPropagation("sampleW.xml",k)
e.createChart(50)
startSimulation(2,50,k,e,0)
startSimulation(2,50,k,e,0,trans_type="trianguleClosure", trans_n=0.25)
startSimulation(2,50,k,e,0,trans_type="trianguleClosure", trans_n=0.5)
startSimulation(2,50,k,e,0,trans_type="trianguleClosure", trans_n=0.75)
startSimulation(2,50,k,e,0,trans_type="trianguleClosure", trans_n=1.0)





