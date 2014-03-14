import networkx as nx
import Message as msg
import threading 
import random
import multiSetUtils  as multiSet

class Network(object):

    graph = None
    x_lock = threading.Lock()

    def __init__(self,n):
       self.graph = nx.random_geometric_graph(n,0.7)
       if not nx.is_connected(self.graph):
         self.graph = nx.connected_component_subgraphs(self.graph)[0]
       list_nodes = self.graph.nodes()
       for i in range(0,len(list_nodes)):
          self.initializeNode(i)


    def initializeNode(self,pos):
       ms =  multiSet.getMultiSet(10)
       self.graph.node[pos]['M'] = ms
       m = msg.Message(random.choice(ms), len(ms),0)
       list_m = []
       list_m.append(m)
       self.graph.node[pos]['Messages'] = list_m

    def getMessagesByRound(self,pos,rd):
      list_m = self.graph.node[pos]['Messages']
      list_mbyRound = []
      for i in range(0,len(list_m)):
        if rd  == list_m[i].getRound():
          list_mbyRound.append(list_m[i])
      return list_mbyRound

    def getNodes(self):
      return self.graph.nodes()

    def sendMessage(self,m,i):
        self.x_lock.acquire()
        list_m = self.graph.node[i]['Messages']
        list_m.append(m)
        self.graph.node[i]['Messages'] = list_m
        self.x_lock.release()
    