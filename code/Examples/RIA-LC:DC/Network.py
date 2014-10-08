import networkx as nx
import numpy as np
from random import randint,uniform
import math
import threading
from lxml import etree
from lxml import objectify


class Network(object):

    graph = None
    m =  None
    x_lock = threading.Lock()
    realSum = None

    def __init__(self,sample):
       print "new network"
       self.realSum = 0
       m = 0.0
       #sample = "/Users/rafaelremondes/UM/MEI/Thesis/DistributedAggregationAlgortihmsSM/code/NetworkSamples/"+sample
       #self.graph = self.loadSample(sample)
       self.graph = nx.random_geometric_graph(20,0.7)
       #self.loadSample(sample)
       if not nx.is_connected(self.graph):
         self.graph = nx.connected_component_subgraphs(self.graph)[0]
       for i in range(0,len(self.graph.nodes())):
         self.initializeNode(self.graph.nodes()[i],randint(1,100))
       print "all nodes"
       print "hum"
       bound1 = self.realSum/math.log(2*0.01*self.realSum+2)
       print "log is not the problem"
       bound2 =  self.realSum/math.log(self.realSum/5)
       print "nop not the log"
       bound3 = max(bound1,bound2)
       print "nor the bound3"
       while m < bound3:
        print "loop"
        m =  uniform(0.0,bound3+1)
       self.m = round(m)


    def loadSample(self, sample):
        file = sample
        nodes = []
        edges = []
        root = etree.parse(file).getroot()
        for element in root.iter("*"):
            if(element.tag == "node" ):
                aux = []
                for subelement in element.iter("*"):
                      aux.append(subelement.text)
                nodes.append(aux)
            if(element.tag == "edge"):
                aux = []
                for subelement in element.iter("*"):
                      if(subelement.tag == "source" or subelement.tag == "sink" or subelement.tag == "lengthInMeters"):
                           aux.append(subelement.text)
                edges.append(aux)
        graph = nx.Graph()
        for i in range(0,len(edges)):
            graph.add_edge(edges[i][0],edges[i][1], weight = int(float(edges[i][2])))
        return graph


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

    def sendMessage(self,m):
      self.x_lock.acquire()
      dest = m[0]
      for i in range(0,len(self.graph.nodes())):
        list_m = self.graph.node[dest]['inbox']
        list_m.append(m)
        self.graph.node[dest]['inbox']
      self.x_lock.release()

    def getMessages(self, pos):
      return self.graph.node[pos]['inbox']

    def clearInbox(self,pos):
      self.x_lock.acquire()
      self.graph.node[pos]['inbox'] = []
      self.x_lock.release()