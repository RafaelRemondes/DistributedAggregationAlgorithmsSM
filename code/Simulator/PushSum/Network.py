import random
import networkx as nx
import threading 
from lxml import etree
from lxml import objectify
from random import choice
from random import randint
import matplotlib.pyplot as plt
import graphUtils as utils



class Network(object):

    graph = None
    x_lock = threading.Lock()
    realVal = 0.0

    def __init__(self,sample, trans_type= None, trans_n= None):
       sample = "/Users/rafaelremondes/UM/MEI/Thesis/DistributedAggregationAlgortihmsSM/code/NetworkSamples/"+sample
       self.graph = utils.loadSample(sample)
       #self.graph = nx.random_geometric_graph(133,0.25)
       if not nx.is_connected(self.graph):
         self.graph = nx.connected_component_subgraphs(self.graph)[0]
       list_nodes = self.graph.nodes()
       for i in range(0,len(list_nodes)):
          x = random.uniform(1.0, 10.0)
          self.realVal += x        
          self.graph.node[list_nodes[i]]['inbox'] = []
          self.graph.node[list_nodes[i]]['consumption'] = x
       if trans_n != None and trans_type != None:
          self.applyTransformation(trans_type, trans_n)
       #self.realVal = self.realVal/133.0

    def getEdges(self):
      return self.graph.edges()

    def getNodeDegree(self):
      return utils.getNodeDegree(self.graph)

    def applyTransformation(self, trans_type, trans_n):
      self.graph  = utils.transformation(trans_type,trans_n,self.graph)

    def draw(self):
       pos = nx.graphviz_layout(self.graph, prog='sfdp', args='')
       list_nodes = self.graph.nodes()
       plt.figure(figsize=(20,10))
       nx.draw(self.graph, pos, node_size=20, alpha=0.4, nodelist=list_nodes, node_color="blue", with_labels=False)
       plt.savefig('graphNX.png')
       plt.show()
      
    def getVal(self,pos):
        return self.graph.node[pos]['consumption']

    def getNode(self,i):
      return self.graph.node[i]

    def getNodes(self):
       return self.graph.nodes()

    def getNeighbors(self, node):
        return self.graph.neighbors(node)

    def getRealVal(self):
        #get the real average
        return self.realVal

    def getMessagesPerRound(self,node,rd):
        list_m = self.graph.node[node]['inbox']
        aux = []
        for i in range(0,len(list_m)):
          if list_m[i][0] == rd:
            aux.append(list_m[i])
        return aux

    def getMessages(self,pos):
      return self.graph.node[pos]['inbox']

    def printS(self, s):
      self.x_lock.acquire()
      #print s
      self.x_lock.release()

    def clearInbox(self,pos):
      self.x_lock.acquire()
      self.graph.node[pos]['inbox'] = []
      self.x_lock.release()

    def sendMessage(self,node,message):
        self.x_lock.acquire()
        list_m = self.graph.node[node]['inbox'] 
        list_m.append(message)
        self.graph.node[node]['inbox'] = list_m
        self.x_lock.release()



