
import networkx as nx
import vectorUtils
import threading 
import random
import graphUtils as utils
from lxml import etree
from lxml import objectify



class Network(object):

    graph = None
    aggregates = None
    x_lock = threading.Lock()

    def __init__(self,sample,k):
      self.aggregates = 0.0
      sample = "/Users/rafaelremondes/UM/MEI/Thesis/DistributedAggregationAlgortihmsSM/code/NetworkSamples/"+sample
      self.graph = utils.loadSample(sample)
      if not nx.is_connected(self.graph):
         self.graph =  nx.is_connected_component_subgraphs(self.graph)[0]
      for i in range(0,len(self.graph.nodes())):
         self.initializeNode(self.graph.nodes()[i],k)

    def reboot(self,k):
      for i in range(0,len(self.graph.nodes())):
        initVal = self.graph.node[self.graph.nodes()[i]]['consumptiom']
        x = vectorUtils.initializeVector(k,initVal)
        self.graph.node[self.graph.nodes()[i]]['X'] = x
        self.graph.node[self.graph.nodes()[i]]['Messages'] = []

    def applyTransformation(self,trans_type,trans_n):
       self.graph = utils.transformation(trans_type, trans_n, self.graph)

    def initializeNode(self,pos,k):
       #list_c = self.readConsumption()
       initVal = random.randint(1,100)
       self.aggregates += initVal
       x = vectorUtils.initializeVector(k,initVal)
       self.graph.node[pos]['consumptiom'] = initVal
       self.graph.node[pos]['X'] = x
       self.graph.node[pos]['Messages'] = []


    def getNodes(self):
       return self.graph.nodes()

    def readConsumption(self):
      consumptions = []
      path = "/Users/rafaelremondes/UM/MEI/Thesis/DistributedAggregationAlgortihmsSM/code/Simulator/consumptiom.txt"
      f = open(path, "r+")
      for line in f:
          consumptions.append(float(line))
      return consumptions

    def getNeighbors(self,pos):
       return self.graph.neighbors(pos)

    def getChannelCapacity(self,pos,dest):
       if self.graph[pos][dest]['weight'] is not None:
          return self.graph[pos][dest]['weight']
       else 
          return 0.0

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

    def getAggregates(self):
      return self.aggregates
    
    def setX(self, pos, x):
       self.graph.node[pos]['X'] = x
