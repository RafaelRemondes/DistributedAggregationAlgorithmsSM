import networkx as nx
import Message as msg
import threading
from random import randint,choice

class Network(object):

    graph = None
    x_lock = threading.Lock()


    def __init__(self,n):
        self.graph = nx.random_geometric_graph(n,0.8)
        if not nx.is_connected(self.graph):
            self.graph = nx.is_connected_component_subgraphs(self.graph)[0]
        for i in range(0,len(self.graph.nodes())):
            self.initNodes(i)

    def initNodes(self, pos):
        self.graph.node[pos]['A'] = randint(80,1024)
        self.graph.node[pos]['H'] = []
        self.graph.node[pos]['Round'] = 0
        self.graph.node[pos]['Inbox'] = []

    def getNodes(self):
        return self.graph.nodes()

    def getA(self, pos):
        return self.graph.node[pos]['A']

    def getH(self, pos):
        return self.graph.node[pos]['H']

    def getRound(self,pos):
        return self.graph.node[pos]['Round']

    def selectRandomNeighbour(self, pos):
        return choice(self.graph.neighbors(pos))

    def send(self, m):
        self.x_lock.acquire()
        list_m = self.graph.node[m.getDest()]['Inbox']
        list_m.append(m)
        self.graph.node[m.getDest()]['Inbox'] = list_m
        self.x_lock.release()

    def checkInbox(self, pos, dest = None, rd = None):
        self.x_lock.acquire()
        list_m = self.graph.node[pos]['Inbox']
        for i in range(0,len(list_m)):
            if rd is None:
               if list_m[i].getNode() == dest:
                   m = list_m[i]
                   list_m.remove(m) 
                   self.graph.node[pos]['Inbox'] = list_m
                   self.x_lock.release()
                   return m
            if dest is None:
               if list_m[i].getRound() == rd:
                    m = list_m[i]
                    list_m.remove(m) 
                    self.graph.node[pos]['Inbox'] = list_m
                    self.x_lock.release()
                    return m               
        self.x_lock.release()
        return None

    def updateH(self,pos,h):
        self.graph.node[pos]['H'] = h

    def updateRound(self,pos,rd):
        self.graph.node[pos]['Round'] = rd

