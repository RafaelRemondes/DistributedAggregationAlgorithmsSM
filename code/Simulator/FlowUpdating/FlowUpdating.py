import Network as ntw
import Node as nd
import threading
import time
from random import choice
from math import sqrt, pow
import pygal



class FlowUpdating(object):
    
    net = None
    nodes = None
    line_chart = None


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
        node = choice(self.nodes)
        node.setSize(1.0)

    def reboot(self, n, trans_type, trans_n):
        self.net = ntw.Network(n)
        self.nodes = []
        self.net.applyTransformation(trans_type,trans_n)
        aux = self.net.getNodes()
        for i in range(0,len(aux)):
            self.nodes.append(nd.Node(aux[i],self.net))
        node = choice(self.nodes)
        node.setSize(1.0)


    def computeSize(self,n):
      list_size = []
      realSize = len(self.net.getNodes())
      for i in range(0,n):
        aux = 0.0
        for j in range(0,len(self.nodes)):
          aux += pow(realSize-self.nodes[j].getSizePerRound(i),2)
        aux = sqrt(aux/len(self.nodes))
        aux = (aux/realSize)
        print aux
        list_size.append(aux)


    def computeSum(self,n):
      list_sum = []
      realSum = self.net.getRealSum()
      for i in range(0,n):
        aux = 0.0
        for j in range(0,len(self.nodes)):
          aux += pow(realSum-self.nodes[j].getSumPerRound(i),2)
        aux = sqrt(aux/len(self.nodes))
        aux = (aux/realSum)
        print aux
        list_sum.append(aux)
      return list_sum

    def computeStat(self,n):
      list_stat = []
      realAvg =  self.net.getAvg()
      for i in range(0,n):
        aux = 0.0
        for j in range(0,len(self.nodes)):
          aux += pow(realAvg-self.nodes[j].getAvgPerRound(i),2)
        aux = sqrt(aux/len(self.nodes))
        aux = (aux/realAvg)
        list_stat.append(aux)


    def createChart(self,n, name):
       self.line_chart = pygal.Line()
       self.line_chart.title = 'FlowUpdating results with '+name+' evolution Strategy'
       self.line_chart.x_labels = map(str, range(0,n))

    def drawChart(self,n, trans_type, trans_n):
        s = str(trans_n)
        self.line_chart.add(s+" Edges added", self.computeSum(n))
        s = trans_type+'.svg'
        self.line_chart.render_to_file(s)   
    
    def start(self, n):
     for j in range(0,n):
        #sum_avg = 0.0
        #sum_vi = 0.0
        #sum_flows = 0.0
        #for i in range(0, len(self.nodes)):
         #  self.nodes[i].clearInbox()
         #  sum_avg += self.nodes[i].getLastAvg()
         #  sum_vi  += self.nodes[i].getValue()
         #  sum_flows += (self.nodes[i].getValue()-self.nodes[i].getFlows())
        #print "AVG: %.2f FLOWS:%.2f SUM:%.2f"%(sum_avg,sum_flows,sum_vi)
        #if sum_avg == sum_flows == sum_vi:
        #   print "true"
        #else:
         #  print "false"
        list_t = []
        for i in range(0, len(self.nodes)):
           thread1 = self.serviceNode(self.nodes[i],n)
           thread1.start()
           list_t.append(thread1)
        for i in range(0, len(list_t)):
           if list_t[i].isAlive():
              list_t[i].join()

    def startProtocol(self, n, trans_type = None, trans_n = None):
      nEdges = 0.0
      name = 'estimate'
      if trans_type != None and trans_n != None:
        nEdges = trans_n
        name = trans_type
        self.reboot("sample1.xml", trans_type, trans_n)
      self.start(n)
      self.drawChart(n, name, nEdges)


f = FlowUpdating("sample1.xml")

f.createChart(100, "AssorsativityHD")
f.startProtocol(100, "assorsativityHD",0.25)
f.startProtocol(100, "assorsativityHD",0.5)
f.startProtocol(100, "assorsativityHD",0.75)
f.startProtocol(100, "assorsativityHD",1.0)

f.createChart(100, "AssorsativityLD")
f.startProtocol(100, "assorsativityLD",0.25)
f.startProtocol(100, "assorsativityLD",0.5)
f.startProtocol(100, "assorsativityLD",0.75)
f.startProtocol(100, "assorsativityLD",1.0)


f.createChart(100, "Dissorsativity")
f.startProtocol(100, "dissorsativity",0.25)
f.startProtocol(100, "dissorsativity",0.5)
f.startProtocol(100, "dissorsativity",0.75)
f.startProtocol(100, "dissorsativity",1.0)

f.createChart(100, "TrianguleClosure")
f.startProtocol(100, "trianguleClosure",0.25)
f.startProtocol(100, "trianguleClosure",0.5)
f.startProtocol(100, "trianguleClosure",0.75)
f.startProtocol(100, "trianguleClosure",1.0)

f.createChart(100, "Random")
f.startProtocol(100, "random",0.25)
f.startProtocol(100, "random",0.5)
f.startProtocol(100, "random",0.75)
f.startProtocol(100, "random",1.0)




