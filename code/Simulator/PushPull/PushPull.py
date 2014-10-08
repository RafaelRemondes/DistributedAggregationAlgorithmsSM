import Network as ntw
import Node as nd
import time
import threading
import math
from random import choice
import pygal


class pushpull(object):
   
    net = None
    nodes  = None
    line_chart = None

    class serviceNode(threading.Thread):
  
       pos = None

       def __init__(self, pos):
         self.pos = pos
         threading.Thread.__init__(self)

       def run(self):
          self.pos.main()

    def __init__(self):
      self.nodes = []
      self.net = ntw.Network("sample1.xml",0.5)
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
       list_t = []
       for i in range(0,len(self.nodes)):
            thread1 = self.serviceNode(self.nodes[i])
            list_t.append(thread1)
            thread1.start()
       for i in range(0,len(list_t)):
         if list_t[i].isAlive():
           list_t[i].join()
     self.net.setOnOff(False)

    def reboot(self, trans_type, trans_n):
      self.nodes = []
      self.net = ntw.Network("sample1.xml",0.5)
      self.net.applyTransformation(trans_type, trans_n)
      list_nodes = self.net.getNodes()
      for i in range(0,len(list_nodes)):   
         self.nodes.append(nd.Node(self.net,list_nodes[i],self.net.getInitVal(list_nodes[i])))
      node = choice(self.nodes)
      self.net.setSize(node.getPos(),1.0)


    def createChart(self,n):
       self.line_chart = pygal.Line()
       self.line_chart.title = 'PushPull results with Dissorsativity evolution Strategy'
       self.line_chart.x_labels = map(str, range(0,n))

    def drawChart(self,n, trans_n):
        s = str(trans_n)
        self.line_chart.add(s+" Edges added", self.getSums(n))
        self.line_chart.render_to_file('Dissorsativity.svg')   

    def getSumNode(self,n):
      list_sum = []
      node = choice(self.nodes)
      x_sum = self.net.getSum()
      for j in range(0,n):
        aux = 0.0
        size = 0.0
        if node.getSize(j) > 0.0:
           size = pow(node.getSize(j),(-1.0))
        aux = pow(x_sum-size,2)
        aux = math.sqrt(aux)
        aux = aux/x_sum
        list_sum.append(aux)
      return list_sum

    def getSums(self,n):
      list_sum = []
      list_avg = []
      self.net.printRealVal()
      x = self.net.getRealVal()
      x_sum = self.net.getRealSum()
      for j in range(3,n):
          aux=0.0
          aux_sum = 0.0
          for i in range(0,len(self.nodes)):
             aux += pow(x-self.nodes[i].getAVG(j),2)
             aux_sum += pow(x_sum-self.nodes[i].getSum(j),2)
          aux = math.sqrt(aux/len(self.nodes))
          aux_sum = math.sqrt(aux_sum/len(self.nodes))
          aux = (aux/x)
          aux_sum = (aux_sum/x_sum)
          list_sum.append(aux_sum)
          list_avg.append(aux)
      return list_sum

    def startProtocol(self, n, trans_type = None, trans_n =  None):
      if trans_type != None and trans_n != None:
        self.reboot(trans_type, trans_n)
      self.start(n)
      if trans_n != None:
         self.drawChart(n-20, trans_n)
      else:
         self.drawChart(n-20, 0.0)

p = pushpull()
p.createChart(100)
#p.startProtocol(220)
p.startProtocol(120, trans_type="dissorsativity", trans_n=0.25)
p.startProtocol(120, trans_type="dissorsativity", trans_n=0.5)
p.startProtocol(120, trans_type="dissorsativity", trans_n=0.75)
p.startProtocol(120, trans_type="dissorsativity", trans_n=1.0)


