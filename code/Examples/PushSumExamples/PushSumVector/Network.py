import random
import networkx as nx
import threading 
import vectorUtils as vector
import Message as msg
from random import choice
from random import randint


class Network(object):

    graph = None
    alpha = None
    average = 0.0
    x_lock = threading.Lock()

    def __init__(self,n):
       self.graph = nx.random_geometric_graph(n,0.8)
       if not nx.is_connected(self.graph):
         self.graph = nx.connected_component_subgraphs(self.graph)[0]
       self.alpha = 1/len(self.graph.nodes())
       #initialize nodes with a random value
       nr_Nodes = len(self.graph.nodes())
       for i in range(0,len(self.graph.nodes())):
          list_m = []
          list_m.append(msg.Message(0,l=nr_Nodes,indice=i))
          self.graph.node[self.graph.nodes()[i]]['vector'] = list_m
          self.graph.node[self.graph.nodes()[i]]['initVal'] = random.uniform(1.0, 1000.0)
          self.average += self.graph.node[self.graph.nodes()[i]]['initVal']
       self.average = self.average/len(self.graph.nodes())

    def getAlpha(self):
      return self.alpha

    def getRealAverage(self):
      return self.average

    def getXj(self):
      list_xj = []
      for i in range (0,len(self.graph.nodes())):
         list_xj.append(self.graph.node[self.graph.nodes()[i]]['initVal'])
      return list_xj

    def getVr(self,node, rd):
      list_m = self.graph.node[node]['vector']
      sum_result = vector.initZeros(len(self.graph.nodes()))
      for i in range(0,len(list_m)):
        if list_m[i].getRound() == rd:
          sum_result = vector.sum(sum_result,list_m[i].getV())
      #compute alpha share to send 
      return sum_result

    def sendMessage(self,message):
        self.x_lock.acquire()
        list_nodes = self.graph.nodes()
        #for each node update the received vector
        for i in range(0,len(list_nodes)):
           #get the vector's list
           listV = self.graph.node[list_nodes[i]]['vector']
           #add in the last position the last vector
           listV.append(message)
           #update the vectors
           self.graph.node[list_nodes[i]]['vector'] = listV
        self.x_lock.release()



    def computeS(self,pos):
      list_m = self.graph.node[pos]['vector']
      x = self.graph.node[self.graph.nodes()[pos]]['initVal']
      list_sum = vector.initZeros(len(self.graph.nodes()))
      for i in range(0,len(list_m)):
        list_a = list_m[i]
        list_a = vector.mul(list_a.getV(),x)
        list_sum = vector.sum(list_sum,list_a.getV())
      #compute alpha share to send 
      list_sum = vector.mul(list_sum,self.alpha)
      return list_sum

    def computeW(self):
      list_w = []
      for i in range(0,len(self.graph.nodes())):
        list_w.append(1)
      return list_w

    def getNodes(self):
        return self.graph.nodes()

    def logMessages(self):
        print 'Messages Exchanged %d'%self.nrMessages
