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
      print "new network"
      self.net = ntw.Network(n)
      list_nodes = self.net.getNodes()
      for i in range(0,len(list_nodes)):
         self.nodes.append(nd.Node(self.net,list_nodes[i]))

    def start(self,n):
      for i in range(0,n):
         print "New Round"
         list_t = []
         for j in range(0,len(self.nodes)):
            thread1 = self.serviceNode(self.nodes[j])
            thread1.start()
            list_t.append(thread1)
         for j in range(0,len(list_t)):
            if list_t[j].isAlive():
               list_t[j].join()
      for i in range(0,len(self.nodes)):
         self.nodes[i].printSum()

    def computeSumNode(self,n):
      realSum = self.net.getRealSum()
      node = random.choice(self.nodes)
      list_sums = []
      for i in range(0,n):
        auxSum = 0.0
        auxSum = pow(realSum-node.getSum(n),2)
        auxSum = random.sqrt(auxSum)
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
       self.line_chart.title = 'RIA-LC/DC results'
       self.line_chart.x_labels = map(str, range(1,n))

    def drawChart(self,n):
        self.line_chart.add("Sum per round", self.computeSums(n))
        self.line_chart.render_to_file('estimates.svg')   




ria = RIA("sample1.xml")
ria.start(10)
ria.createChart(10)
ria.drawChart(10)
