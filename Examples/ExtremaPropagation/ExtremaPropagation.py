import Network as ntw
import Node as nd
from random import randint
import time
import pygal
import threading


class ExtremaPropagation(object):

    net = None
    nodes = None

    class serviceNode(threading.Thread):

       pos = None
       rd = None

       def __init__(self,pos,rd):
          self.pos = pos
          self.rd = rd
          threading.Thread.__init__(self)

       def run(self):
           for i in range(0,self.rd):
              self.pos.update()
              self.pos.send()
              time.sleep(0.01)


    def __init__(self,n,k):
        self.net = ntw.Network(n,k)
        self.nodes = []
        for i in range(0,len(self.net.getNodes())):
           self.nodes.append(nd.Node(self.net.getNodes()[i],self.net))
           self.nodes[i].send()

    def start(self, n):
       for i in range(0, len(self.nodes)):
          thread1 = self.serviceNode(self.nodes[i],n)
          thread1.start()

    def computeN(self,k):
    	list_n = []
    	for i in range(0,len(self.nodes)):
    		list_n.append(self.nodes[i].computeNx(k))
    	return list_n


    def drawChart(self,k):
       line_chart = pygal.Line()
       line_chart.title = 'Extrema Propagation results'
       line_chart.x_labels = map(str, range(1, len(self.nodes)+1))
       list_estimate = self.computeN(k)
       line_chart.add('Estimate', list_estimate)
       line_chart.render_to_file('estimates.svg')   



k = 387
e = ExtremaPropagation(20,k)
e.start(50)
e.drawChart(k)