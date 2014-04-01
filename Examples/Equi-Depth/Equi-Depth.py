import Network as ntw
import Node as nd
import threading
import time

class EquiDepth(object):
 
    net  = None
    nodes  = None

    class serviceNode(threading.Thread):

        pos = None
        rd = None

        def __init__(self,pos,rd):
            self.pos = pos
            self.rd = rd
            threading.Thread.__init__(self)

        def run(self):
            for i in range(0,self.rd):
                self.pos.start(i)
                time.sleep(1)
            self.pos.finishRound()


    def __init__(self,n,k):
       self.nodes = []
       self.net = ntw.Network(n,k)
       for i in range(0,len(self.net.getNodes())):
             self.nodes.append(nd.Node(self.net.getNodes()[i],self.net))
    
    def start(self,n):
        for i in range(0,len(self.nodes)):
            thread1 = self.serviceNode(self.nodes[i],n)
            thread1.start()


e = EquiDepth(10,20)
e.start(5)


