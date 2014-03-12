import random
import networkx as nx
import Message as msg
import threading 
from random import choice
from random import randint


class Network(object):

    graph = None
    x_lock = threading.Lock()
    realVal = 0.0

    def __init__(self,n):
       r = 0.0
       self.graph = nx.random_geometric_graph(n,0.7)
       if not nx.is_connected(self.graph):
         self.graph = nx.connected_component_subgraphs(self.graph)[0]
       list_nodes = self.graph.nodes()
       #initialize nodes with a random value
       for i in range(0,len(list_nodes)):
          x = random.uniform(1.0, 1000.0)
          r += x
          list_m = []
          list_m.append(msg.Message(x,1.0,0))
          self.graph.node[list_nodes[i]]['msg'] = list_m
       self.realVal = r/len(self.graph.nodes())

    def selectNode(self,i):
      return self.graph.node[i]

    def getNodes(self):
       return self.graph.nodes()

    def getReal(self):
      return self.realVal

    def sendMessage(self,node,message):
        list_m = self.graph.node[node]['msg'] 
        list_m.append(message)
        self.graph.node[node]['msg'] = list_m


    def computeSumS(self,node,rd):
      r = rd
      list_m = self.graph.node[node]['msg']
      n = len(list_m)
      sum = 0
      for i in range(0,n):
         m = list_m[i]
         if r == m.getRound():
            sum = sum+ m.getS()
      return sum

    def computeSumW(self,node,rd):
      r = rd
      list_m = self.graph.node[node]['msg']
      n = len(list_m)
      sum = 0
      for i in range(0,n):
         m = list_m[i]
         if r == m.getRound():
            sum = sum+ m.getW()
      return sum

    def getNeighbors(self, node):
        return self.graph.neighbors(node)

    def getRealVal(self):
      #get the real average
      return self.realVal
