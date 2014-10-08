import networkx as nx
import threading
from random import uniform

class Network(object):

    graph = None
    realAvg = None
    x_lock = threading.Lock()
 
    def __init__(self,n):
        self.realAvg = 0.0
        self.graph = nx.erdos_renyi_graph(4, 0.8, seed=None, directed=False)
        if not nx.is_connected(self.graph):
          self.graph =  nx.is_connected_component_subgraphs(self.graph)[0]
        for i in range(0,len(self.graph.nodes())):
            self.initializeNodes(i)
        self.realAvg = self.realAvg/len(self.graph.nodes())

    def initializeNodes(self, pos):
        x = uniform(0.0,100.0)
        self.graph.node[pos]['val'] = x
        self.graph.node[pos]['inbox'] = []
        self.realAvg += x

    def getNodes(self):
        return self.graph.nodes()

    def getVal(self,pos):
        return self.graph.node[pos]['val']
    
    def getAvg(self):
        print "REAL AVG %.2f"%self.realAvg
        return self.realAvg

    def getNeighbors(self,pos):
        return self.graph.neighbors(pos)

    def sendMessage(self,m):
        self.x_lock.acquire()
        dest = m[0]
        list_m = []
        list_m = self.graph.node[dest]['inbox']
        list_m.append(m)
        self.graph.node[dest]['inbox'] = list_m
        self.x_lock.release()

    def getMessages(self,pos):
        return self.graph.node[pos]['inbox']

    def clearInbox(self,pos):
        self.x_lock.acquire()
        self.graph.node[pos]['inbox'] = []
        self.x_lock.release()






