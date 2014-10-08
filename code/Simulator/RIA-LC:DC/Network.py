import networkx as nx
import numpy as np
from random import randint,uniform
import math
import threading
from lxml import etree
from lxml import objectify
import graphUtils as utils
import matplotlib.pyplot as plt



class Network(object):

    graph = None
    m =  None
    x_lock = threading.Lock()
    realSum = None

    def __init__(self,sample):
       self.realSum = 0
       m = 0.0
       sample = "/Users/rafaelremondes/UM/MEI/Thesis/DistributedAggregationAlgortihmsSM/code/NetworkSamples/"+sample
       self.graph = utils.loadSample(sample)
       #self.graph = nx.erdos_renyi_graph(133, 0.15, seed=None, directed=False)
       if not nx.is_connected(self.graph):
         self.graph = nx.connected_component_subgraphs(self.graph)[0]
       #self.draw()
       for i in range(0,len(self.graph.nodes())):
         self.initializeNode(self.graph.nodes()[i],randint(1,100))
       bound1 = self.realSum/math.log(2*0.01*self.realSum+2)
       bound2 =  self.realSum/math.log(self.realSum/5)
       bound3 = max(bound1,bound2)
       while m < bound3:
        m =  uniform(0.0,bound3+1)
       self.m = round(m)
    
    def applyTransformation(self,trans_type, trans_n):
      self.graph = utils.transformation(trans_type,trans_n,self.graph)

    
    def draw(self):
       pos = nx.graphviz_layout(self.graph, prog='sfdp', args='')
       list_nodes = self.graph.nodes()
       plt.figure(figsize=(20,10))
       nx.draw(self.graph, pos, node_size=20, alpha=0.4, nodelist=list_nodes, node_color="blue", with_labels=False)
       plt.savefig('graphNX.png')
       plt.show()

    def getRealSum(self):
      return self.realSum

    def log(self, s):
      self.x_lock.acquire()
      print s
      self.x_lock.release()

    def getVn(self):
      aux =  -(self.realSum/self.m)
      vn =  pow(np.e,aux)
      return vn


    def initializeNode(self,pos,x):
       self.graph.node[pos]['val'] = x
       self.realSum += x
       self.graph.node[pos]['inbox'] = []

    def getVal(self,pos):
       return self.graph.node[pos]['val']

    def getNeighbors(self,pos):
       return self.graph.neighbors(pos)
  
    def getNodes(self):
       return self.graph.nodes()
  
    def getM(self):
        return self.m

    def sendMessage(self,m, dest):
      self.x_lock.acquire()
      list_m = self.graph.node[dest]['inbox']
      list_m.append(m)
      self.graph.node[dest]['inbox']
      self.x_lock.release()

    def getMessages(self, pos):
      list_m = self.graph.node[pos]['inbox']
      return list_m

    def clearInbox(self,pos):
      self.graph.node[pos]['inbox'] = []
