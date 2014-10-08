import random
import networkx as nx
import threading 
from lxml import etree
from lxml import objectify
from random import choice
from random import randint


class Network(object):

    graph = None
    isOn = None
    x_lock = threading.Lock()
    realVal = 0.0
    realSum = None

    def __init__(self,sample):
       sample = "/Users/rafaelremondes/UM/MEI/Thesis/DistributedAggregationAlgortihmsSM/code/NetworkSamples/"+sample
       self.graph = nx.random_geometric_graph(200,0.7)#self.loadSample(sample)
       if not nx.is_connected(self.graph):
         self.graph = nx.connected_component_subgraphs(self.graph)[0]
       list_nodes = self.graph.nodes()
       for i in range(0,len(list_nodes)):
          x = random.uniform(1.0, 10.0)
          self.graph.node[list_nodes[i]]['inbox'] = []
          self.graph.node[list_nodes[i]]['initVal'] = x  
          self.graph.node[list_nodes[i]]['size'] = 0.0
          self.realVal += x
       self.realSum = self.realVal
       self.realVal = self.realVal/len(self.graph.nodes())    
       self.isOn = False


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

    def getRealVal(self):
      return self.realVal
 
    def getRealSum(self):
      return self.realSum

    def getSize(self,pos):
      return self.graph.node[pos]['size'] 

    def setSize(self,pos,size):
      self.x_lock.acquire()
      self.graph.node[pos]['size'] = size
      self.x_lock.release()
    
    def setOnOff(self, onoff):
      self.isOn = onoff

    def getInitVal(self,pos):
       return self.graph.node[pos]['initVal']
    
    def getNodes(self):
      return self.graph.nodes()
    
    def getNeighbors(self,pos):
      return self.graph.neighbors(pos)

    def setInitVal(self,pos, val):
      self.x_lock.acquire()
      self.graph.node[pos]['initVal'] = val
      self.x_lock.release()

    def isProtocolOn(self):
      return self.isOn

    def checkInbox(self,pos, dest= None):
      self.x_lock.acquire()
      m = None
      list_m = self.graph.node[pos]['inbox']
      if len(list_m) > 0 :
       for i in range(0,len(list_m)):
        if dest is None:
           m = list_m[i]
           list_m.remove(m)
           self.graph.node[pos]['inbox'] = list_m
           self.x_lock.release()
           return m
        else:
           if list_m[i][1] == dest:
             m = list_m[i]
             list_m.remove(m)
             self.graph.node[pos]['inbox'] = list_m
             self.x_lock.release()
             return m
      self.x_lock.release()
      return m


    def sendMessage(self,m):
      self.x_lock.acquire()
      dest = m[0]
      list_m = self.graph.node[dest]['inbox']
      list_m.append(m)
      self.graph.node[dest]['inbox'] = list_m
      self.x_lock.release()

    def printRealVal(self):
      print "REAL VAL %.2f"%self.realVal

  