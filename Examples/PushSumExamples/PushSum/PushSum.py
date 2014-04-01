import Network as netwk
import Node as nd
import Message as msg
import threading
import time
import pygal
from math import pow,sqrt

class pushSum(object):

   net = None
   nodes = []

   class serviceNode(threading.Thread):
  
       pos = None 
       rd = None

       def __init__(self, pos, rd):
         self.pos = pos
         self.rd = rd
         threading.Thread.__init__(self)

       def run(self):
         i = 1
         while i <= self.rd:
           self.pos.main(i)
           i+=1

   def __init__(self):
    #create a new random geometric network
    self.net = netwk.Network(1000)
    #get the list of created node to initialize Node objects
    list_nodes = self.net.getNodes()
    for i in range(0,len(list_nodes)):
      self.nodes.append(nd.Node(self.net,list_nodes[i]))

   def computeStat(self, n):
    list_st = []
    auxSum = 0.0
    realVal = self.net.getRealVal()
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


   def startRounds(self,n):
      print "Real average: %.2f"%self.net.getRealVal()
      print "Number of nodes: %d" %(len(self.nodes))
      #in each new round, start the Push-Sum Algorithm
      #for i in range (1,n):
      for i in range(0,len(self.nodes)):
        #    self.nodes[i].main(n)
        thread1 = self.serviceNode(self.nodes[i],n)
        thread1.start()



#initialize the protocol
p = pushSum()
p.startRounds(25)
time.sleep(10)
p.drawChart(20)
#p.logMessage()
