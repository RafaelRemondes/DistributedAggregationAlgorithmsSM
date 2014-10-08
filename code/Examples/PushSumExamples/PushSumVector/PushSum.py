import Network as netwk
import Node as nd
import Message as msg
import threading
import pygal
import time
from math import pow,sqrt

class pushSum(object):

   net = None
   nodes = {}

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
           time.sleep(1)
           i+=1

   def __init__(self):
    #create a new random geomatric network
    self.net = netwk.Network(5)
    #get the list of created node to initialize Node objects
    list_nodes = self.net.getNodes()
    for i in range(0,len(list_nodes)):
      self.nodes[i] = nd.Node(self.net,list_nodes[i])

   def computeStat(self, n):
     list_st = []
     auxSum = 0.0
     realVal = self.net.getRealAverage()
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
     line_chart.title = 'Average Estimate in each node towards the rounds'
     line_chart.x_labels = map(str, range(1, n+1))
     list_estimate = self.computeStat(n)
     line_chart.add('Estimate', list_estimate)
     line_chart.render_to_file('estimates.svg')   

   def startRounds(self,n):
      #in each new round, start the Push-Sum Algorithm
      for i in range(0,len(self.nodes)):
        thread1 = self.serviceNode(self.nodes[i],n)
        thread1.start()



#initialize the protocol
p = pushSum()
p.startRounds(10)
time.sleep(30)
p.drawChart(10)