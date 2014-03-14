import Network as ntw
import Node as nd
import threading
import time
import pygal

class PushSum(object):
    
    net = None
    nodes = None

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
           time.sleep(0.1)

    def __init__(self,n):
    	self.nodes = []
        self.net = ntw.Network(n)
        for i in range(0,len(self.net.getNodes())):
           self.nodes.append(nd.Node(self.net,self.net.getNodes()[i]))

    def computeQs(self):
    	list_q = []
    	for i in range(0,len(self.nodes)):
           list_q.append(self.nodes[i].getQti())
        return list_q

    def drawChart(self,n):
       line_chart = pygal.Bar()
       line_chart.title = 'The quantiles per node'
       line_chart.x_labels = map(str, range(1, n+1))
       list_estimate = self.computeQs()
       line_chart.add('Estimate', list_estimate)
       line_chart.render_to_file('estimates.svg') 

    def start(self, rd):
    	for i in range(0,len(self.nodes)):
    		thread1 = self.serviceNode(self.nodes[i],rd)
    		thread1.start()


p = PushSum(100)
p.start(500)
time.sleep(100)
p.drawChart(5)