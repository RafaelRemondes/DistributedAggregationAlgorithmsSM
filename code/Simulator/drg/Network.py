import networkx as nx
from random import uniform
import threading
from lxml import etree
from lxml import objectify
import matplotlib.pyplot as plt



class Network(object):

    graph = None
    x_lock = threading.Lock()
    average = None
    realSum = None

    def __init__(self,sample):
        self.average = 0.0
        sample = "/Users/rafaelremondes/UM/MEI/Thesis/DistributedAggregationAlgortihmsSM/code/NetworkSamples/"+sample
        #self.graph = self.loadSample(sample)
        self.graph = nx.erdos_renyi_graph(1000, 0.2, seed=None, directed=False)
        if not nx.is_connected(self.graph):
            self.graph = nx.is_connected_component_subgraphs(self.graph)[0]
        for i in range(0,len(self.graph.nodes())):
            self.initializeNode(self.graph.nodes()[i])
        self.realSum = self.average
        self.average = self.average/len(self.graph.nodes())
        print self.average
        print self.realSum

    def initializeNode(self, pos):
        initVal = uniform(1.0,100.0)
        self.average += initVal
        self.setNodeAtribute(pos,'initVal',initVal)
        self.setNodeAtribute(pos,'mode','idle')
        self.setNodeAtribute(pos,'inbox',[])
    
    def sendMessage(self, m):
        self.x_lock.acquire()
        list_m = self.graph.node[m[2]]['inbox']
        list_m.append(m)
        self.graph.node[m[2]]['inbox'] = list_m
        self.x_lock.release()

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

    def getAverage(self):
        return self.average

    def getRealSum(self):
        return self.realSum

    def setNodeAtribute(self,pos, str, value):
        self.graph.node[pos][str] = value

    def getNodes(self):
        return self.graph.nodes()

    def getInitVal(self,pos):
        return self.graph.node[pos]['initVal']

    def getNeighbors(self,pos):
        return self.graph.neighbors(pos)

    def changeStatus(self,pos,status):
        self.setNodeAtribute(pos,'mode',status)

    def checkStatus(self,pos):
        return self.graph.node[pos]['mode']
    
    def clearInbox(self,pos):
        self.graph.node[pos]['inbox'] = []

    def checkInbox(self,pos):
        list_m = self.graph.node[pos]['inbox']
        if  self.graph.node[pos]['mode'] == 'idle' and len(list_m)==1:
            self.setNodeAtribute(pos,'mode','member')
            return list_m
        if  self.graph.node[pos]['mode'] == 'idle' and len(list_m)>1:
            return None
        if self.graph.node[pos]['mode'] == 'member':
            return list_m
        if self.graph.node[pos]['mode'] == 'leader':
            return list_m
        else:
            return None

    def sendMessage(self, dest, m):
        self.x_lock.acquire()
        list_m = self.graph.node[dest]['inbox']
        list_m.append(m)
        self.setNodeAtribute(dest,'inbox',list_m)
        self.x_lock.release()


