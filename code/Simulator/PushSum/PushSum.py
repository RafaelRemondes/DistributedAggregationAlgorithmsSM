import Network as netwk
import Node as nd
import threading
import time
import random 
import pygal
import math

class pushSum(object):

   net = None
   nodes = []
   line_chart = None

   class serviceNode(threading.Thread):
  
       pos = None 
       rd = None

       def __init__(self, pos, rd):
         self.pos = pos
         self.rd = rd
         threading.Thread.__init__(self)

       def run(self):
          self.pos.main(self.rd)

   def __init__(self):
    #create a new random geometric network
    self.net = netwk.Network("sample1.xml")
    #get the list of created node to initialize Node objects
    list_nodes = self.net.getNodes()
    for i in range(0,len(list_nodes)):
      self.nodes.append(nd.Node(self.net,list_nodes[i]))
    node = random.choice(self.nodes)
    node.setW(1.0)

   def reboot(self, trans_type, trans_n):
    self.net = netwk.Network("sample1.xml", trans_type, trans_n)
    #get the list of created node to initialize Node objects
    self.nodes = []
    list_nodes = self.net.getNodes()
    for i in range(0,len(list_nodes)):
      self.nodes.append(nd.Node(self.net,list_nodes[i]))
    node = random.choice(self.nodes)
    node.setW(1.0)

   def createChart(self,n):
    self.line_chart = pygal.Line()
    self.line_chart.title = 'PushSum results with a random evolution strategy'
    self.line_chart.x_labels = map(str, range(0, n+1))



   def computeStat(self, n):
    list_st = []
    realVal = self.net.getRealVal()
    realVal = realVal
    for j in range(0,n+1):
       auxSum = 0.0
       #calculate the estimator = square((sum (realVal-estimated)^2)/n)
       for i in range(0,len(self.nodes)):
          node = self.nodes[i]
          auxSum += pow((realVal-node.getSumPerRound(j)),2)
       auxSum = auxSum/len(self.nodes)
       auxSum = math.sqrt(auxSum)
       auxSum = (auxSum/realVal)
       list_st.append(auxSum)
    return list_st

   def computeSums(self,list_sum_node):
    list_sum = []
    realSum = self.net.getRealVal() 
    for i in range(0,len(list_sum_node)):
      aux = sqrt(pow((realSum-list_sum_node[i]),2))
      list_sum.append(aux)
    return list_sum

   def drawChart(self,n,transformation):
    #list_estimate = self.computeSums(random.choice(self.nodes).getSum())
    list_estimate = self.computeStat(n)
    s = str(transformation)+" more Edges"
    self.line_chart.add(s, list_estimate)
    self.line_chart.render_to_file('estimates.svg')    

   def startProtocol(self,n, trans_type=None, trans_n = None):
      if trans_type != None and trans_n != None:
        self.reboot(trans_type, trans_n)
      self.startRounds(n)
      if trans_n != None:    
         self.drawChart(n, trans_n)
      else:
        self.drawChart(n,0.0)


   def startRounds(self,n):
      print "Real Sum: %.2f"%self.net.getRealVal()
      print "Number of nodes: %d" %(len(self.nodes))
      print "Node Degree %d" %self.net.getNodeDegree()
      print "Number of edges %d" %len(self.net.getEdges())
      #in each new round, start the Push-Sum Algorithm
      for j in range(1,n+1): 
        list_t = []
        for i in range(0,len(self.nodes)):
          thread1 = self.serviceNode(self.nodes[i],j)
          list_t.append(thread1)
          thread1.start()
        for i in range(0,len(self.nodes)):
          if list_t[i].isAlive():
             list_t[i].join()


#initialize the protocol
p = pushSum()
p.createChart(200)
#p.startProtocol(200)
p.startProtocol(200, "random",0.25)
p.startProtocol(200, "random",0.5)
p.startProtocol(200, "random",0.75)
p.startProtocol(200, "random",1.0)

