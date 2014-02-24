import random
import networkx as nx
import threading 
import vectorUtils as vector
import Message as msg
from random import choice
from random import randint


class Network(object):

    nrMessages = None
    graph = None
    alpha = None
    x_lock = threading.Lock()

    def __init__(self,n):
       self.nrMessages = 0
       self.graph = nx.random_geometric_graph(n,0.1)
       if not nx.is_connected(self.graph):
         self.graph = nx.connected_component_subgraphs(self.graph)[0]
       list_nodes = self.graph.nodes()
       self.alpha = 1/len(list_nodes)
       #initialize nodes with a random value
       for i in range(0,len(list_nodes)):
          m = msg.Message(len(list_nodes),i,0)
          list_m = {}
          list_m[0] = m
          self.graph.node[list_nodes[i]]['vector'] = list_m
          self.graph.node[list_nodes[i]]['initVal'] = randint(0,50)

    def selectNode(self,i):
      return self.graph.node[i]

    def sendMessage(self,message):
        self.x_lock.acquire()
        list_nodes = self.graph.nodes()
        #for each node update the received vector
        for i in range(0,len(list_nodes)):
           #get the vector's list
           listV = self.graph.node[list_nodes[i]]['vector']
           #add in the last position the last vector
           listV[len(listV)-1] = message
           #update the vectors
           self.graph.node[list_nodes[i]]['vector'] = listV
        self.x_lock.release()

    def getVr(self,node, rd):
      r = rd-1
      list_m = self.graph.node[node]['vector']
      list_sum = vector.initZeros(len(self.graph.nodes()))
      for i in range(0, 0,len(list_m)):
        list_a = list_m[i]
        if list_a.getRound() == r:
          list_sum = vector.sum(list_sum)
      #compute alpha share to send 
      list_sum = vector.mul(list_sum,alpha)
      return list_sum

    def computeS(self,pos):
      list_m = self.graph.node[pos]['vector']
      x = self.graph.node[list_nodes[pos]]['initVal']
      list_sum = vector.initZeros(len(self.graph.nodes()))
      for i in range(0,len(list_m)):
        list_a = list_m[i]
        list_a = vetor.mul(list_a,x)
        list_sum = vector.sum(list_sum)
      #compute alpha share to send 
      list_sum = vector.mul(list_sum,alpha)
      return list_sum

    def computeW(self):
      list_w = {}
      for i in range(0,self.graph.nodes()-1):
        list_w = 1
      return list_w

    def getNodes(self, node):
        return self.graph.nodes()

    def logMessages(self):
        print 'Messages Exchanged %d'%self.nrMessages
