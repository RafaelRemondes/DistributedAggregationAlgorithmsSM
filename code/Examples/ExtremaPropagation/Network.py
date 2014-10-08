import networkx as nx
import vectorUtils
import threading 


class Network(object):

    graph = None
    x_lock = threading.Lock()

    def __init__(self,n,k):
      self.graph = nx.random_geometric_graph(n,0.8)
      if not nx.is_connected(self.graph):
         self.graph =  nx.is_connected_component_subgraphs(self.graph)[0]
      for i in range(0,len(self.graph.nodes())):
         self.initializeNode(i,k)

    def initializeNode(self,pos,k):
       x = vectorUtils.initializeVector(k)
       self.graph.node[pos]['X'] = x
       self.graph.node[pos]['Messages'] = []

    def getNodes(self):
       return self.graph.nodes()

    def getNeighbors(self,pos):
       return self.graph.neighbors(pos)

    def send(self, message, pos):
       self.x_lock.acquire()
       list_m = self.graph.node[pos]['Messages']
       list_m.append(message)
       self.graph.node[pos]['Messages'] = list_m
       self.x_lock.release()

    def clearM(self,pos):
       self.graph.node[pos]['Messages'] = []

    def getM(self, pos):
       list_m = self.graph.node[pos]['Messages']
       self.clearM(pos)
       return list_m

    def getX(self,pos):
       return self.graph.node[pos]['X']
    
    def setX(self, pos, x):
       self.graph.node[pos]['X'] = x
