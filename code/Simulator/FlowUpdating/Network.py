import networkx as nx
import threading
from random import uniform
from lxml import etree
from lxml import objectify
import matplotlib.pyplot as plt
import graphUtils as utils


class Network(object):

    graph = None
    realAvg = None
    realSum =  None
    x_lock = threading.Lock()
 
    def __init__(self,sample):
        self.realAvg = 0.0
        self. realSum = 0.0
        #self.graph = nx.erdos_renyi_graph(4, 0.8, seed=None, directed=False)
        sample = "/Users/rafaelremondes/UM/MEI/Thesis/DistributedAggregationAlgortihmsSM/code/NetworkSamples/"+sample
        self.graph = utils.loadSample(sample)
        if not nx.is_connected(self.graph):
          self.graph =  nx.is_connected_component_subgraphs(self.graph)[0]
        for i in range(0,len(self.graph.nodes())):
            self.initializeNodes(self.graph.nodes()[i])
        #self.testingGraph()
        #self.realAvg = 12
        self.realAvg = self.realSum/len(self.graph.nodes())

    def draw(self):
       pos = nx.graphviz_layout(self.graph, prog='sfdp', args='')
       list_nodes = self.graph.nodes()
       plt.figure(figsize=(20,10))
       nx.draw(self.graph, pos, node_size=20, alpha=0.4, nodelist=list_nodes, node_color="blue", with_labels=False)
       plt.savefig('graphNX.png')
       plt.show()
    
    def applyTransformation(self, trans_type, trans_n):
        self.graph = utils.transformation(trans_type,trans_n,self.graph)

    def initializeNodes(self, pos):
        x = uniform(0.0,100.0)
        self.graph.node[pos]['val'] = x
        self.graph.node[pos]['inbox'] = []
        self.realSum += x

    def getNodes(self):
        return self.graph.nodes()

    def getRealSum(self):
        return self.realSum

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

    def log(self,s):
        self.x_lock.acquire()
        print s
        self.x_lock.release()

    def getMessages(self,pos):
        return self.graph.node[pos]['inbox']

    def clearInbox(self,pos):
        self.x_lock.acquire()
        self.graph.node[pos]['inbox'] = []
        self.x_lock.release()






