import Network as nt
import Node as nd
import threading
from random import choice
import time

#TODO
#implement instances
#Verify Results
#Draw Charts
#conclusions

class Adam2(object):
    
    net = None
    nodes = []

    class ServiceNode(threading.Thread):

        pos = None
        rd = None

        def __init__(self,pos,rd):
            self.pos = pos
            self.rd = rd
            threading.Thread.__init__(self)

        def run(self):
            for i in range(1,self.rd+1):
                self.pos.startRound(i)
                time.sleep(1)
            self.pos.finishRound()

    def __init__(self,n):
        self.net = nt.Network(n)
        list_nodes = self.net.getNodes()
        for i in range(0,len(list_nodes)):
            self.nodes.append(nd.Node(self.net,list_nodes[i]))

    def startInstance(self):
        t  = [80,160,240,320,400,480,560,640,720,800,880,960,1024]
        instanceStarter = choice(self.nodes)
        instanceStarter.startInstance(t)

    def start(self, n):
        self.startInstance()
        for i in range(0,len(self.nodes)):
            thread1 = self.ServiceNode(self.nodes[i],n)
            thread1.start()

        

a = Adam2(10)
a.start(5)

