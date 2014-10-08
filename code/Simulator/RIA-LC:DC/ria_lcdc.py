import Network as ntw
import Node as nd 
import threading
import pygal
import math
import random


class RIA(object):

    net = None
    nodes = []
    line_chart = None

    class serviceNode(threading.Thread):
  
      pos = None

      def __init__(self, pos):
         self.pos = pos
         threading.Thread.__init__(self)

      def run(self):
          self.pos.main()      

    def __init__(self,n):
      self.net = ntw.Network(n)
      list_nodes = self.net.getNodes()
      for i in range(0,len(list_nodes)):
         self.nodes.append(nd.Node(self.net,list_nodes[i]))

    def reboot(self, trans_type, trans_n):
       self.net = ntw.Network("sample1.xml")
       self.net.applyTransformation(trans_type, trans_n)
       self.nodes = []
       list_nodes = self.net.getNodes()
       for i in range(0,len(self.net.getNodes())):
         self.nodes.append(nd.Node(self.net,list_nodes[i]))

    def start(self,n):
      #if mode == 1: #Random node Remove
       #  if nodesToRemove > 0:
        #   for i in range(0,nodesToRemove):
         #    node = random.choice(self.nodes)
          #   self.nodes.remove(node)
      #if mode == 2: #Node degree Remove
       #   self.nodes.sort(key=lambda x: x.getDegree(), reverse=True)
        #  for i in range(0,nodesToRemove):
         #   self.nodes.remove(self.nodes[i])
      for i in range(0,n):
         list_t = []
         for j in range(0,len(self.nodes)):
            thread1 = self.serviceNode(self.nodes[j])
            thread1.start()
            list_t.append(thread1)
         for j in range(0,len(list_t)):
            if list_t[j].isAlive():
               list_t[j].join()
    #  for i in range(0,len(self.nodes)):
     #    self.nodes[i].printSum()

    def computeSumNode(self,n):
      realSum = self.net.getRealSum()
      node = random.choice(self.nodes)
      list_sums = []
      for i in range(0,n):
        auxSum = 0.0
        auxSum = pow(realSum-node.getSum(i),2)
        auxSum = math.sqrt(auxSum)
        auxSum = auxSum/realSum
        list_sums.append(auxSum)
      return list_sums

    
    def computeSums(self,n):
        list_sums = []
        realSum = self.net.getRealSum()
        for i in range(0,n):
          auxSum = 0.0
          for j in range(0,len(self.nodes)):
              auxSum += pow(realSum-self.nodes[j].getSum(i),2)
          auxSum = math.sqrt(auxSum/len(self.nodes))
          auxSum = auxSum/realSum
          list_sums.append(auxSum)
        return list_sums
   
    def createChart(self,n):
       self.line_chart = pygal.Line()
       self.line_chart.title = 'RIA-LC/DC results with dissorsativity evolution strategy'
       self.line_chart.x_labels = map(str, range(1,n))

    def drawChart(self,n,nodesToRemove):
        self.line_chart.add(str(nodesToRemove)+" edges", self.computeSumNode(n))
        self.line_chart.render_to_file('estimates.svg')   

    def startSimulation(self,n, trans_type=None, trans_n=None):
      if trans_type != None and trans_n != None:
          self.reboot(trans_type, trans_n)
      self.start(n)
      if trans_n != None:
         self.drawChart(n, trans_n)
      else:
        self.drawChart(n,0)




ria = RIA("sample1.xml")
ria.createChart(100)
ria.startSimulation(100)
ria.startSimulation(100,trans_type="dissorsativity",trans_n=0.25)
ria.startSimulation(100,trans_type="dissorsativity",trans_n=0.5)
ria.startSimulation(100,trans_type="dissorsativity",trans_n=0.75)
ria.startSimulation(100,trans_type="dissorsativity",trans_n=1.0)


