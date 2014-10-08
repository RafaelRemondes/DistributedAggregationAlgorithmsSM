import Network as ntw
import Node as nd
import time
import threading
import math
from random import choice

class pushpull(object):
   
    net = None
    nodes  = None

    class serviceNode(threading.Thread):
  
       pos = None

       def __init__(self, pos):
         self.pos = pos
         threading.Thread.__init__(self)

       def run(self):
          self.pos.main()

    def __init__(self):
      self.nodes = []
      self.net = ntw.Network("sample1.xml")
      list_nodes = self.net.getNodes()
      for i in range(0,len(list_nodes)):   
         self.nodes.append(nd.Node(self.net,list_nodes[i],self.net.getInitVal(list_nodes[i])))
      node = choice(self.nodes)
      self.net.setSize(node.getPos(),1.0)
    
    def start(self,n):
     self.net.setOnOff(True)
     for i in range(0,len(self.nodes)):
       self.nodes[i].startReceive()
     for j in range(0,n):
       for i in range(0,len(self.nodes)):
            thread1 = self.serviceNode(self.nodes[i])
            thread1.start()
       time.sleep(1)
     time.sleep(n*(3/2))
     self.net.setOnOff(False)

    def printAll(self):
      self.net.printRealVal()
      x = self.net.getRealVal()
      x_sum = self.net.getRealSum()
      aux=0.0
      aux_sum = 0.0
      for i in range(0,len(self.nodes)):
        aux += pow(x-self.nodes[i].printAVG(),2)
        aux_sum += pow(x_sum-self.nodes[i].getSum(),2)
      aux = math.sqrt(aux/len(self.nodes))
      aux_sum = math.sqrt(aux_sum/len(self.nodes))
      aux = (aux/x)*100.0
      aux_sum = (aux_sum/x_sum)*100.0
      print aux
      print aux_sum

p = pushpull()
p.start(25)
time.sleep(10)
p.printAll()
print "done"

