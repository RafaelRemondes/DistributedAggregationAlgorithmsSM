import networkx as nx
from random import uniform
import threading
import matplotlib.pyplot as plt



class Network(object):

    graph = None
    x_lock = threading.Lock()
    average = None

    def __init__(self,n):
        self.average = 0.0
        self.graph = nx.random_geometric_graph(n,0.15)
        if not nx.is_connected(self.graph):
            self.graph = nx.is_connected_component_subgraphs(self.graph)[0]
        for i in range(0,len(self.graph.nodes())):
            self.initializeNode(i)
        self.average = self.average/len(self.graph.nodes())

    def initializeNode(self, pos):
        list_v = []
        list_v.append(uniform(1.0,100.0))
        self.average += list_v[0]
        self.setNodeAtribute(pos,'value',list_v)
        self.setNodeAtribute(pos,'mode','idle')
        self.setNodeAtribute(pos,'inbox',[])

    def getAverage(self):
        return self.average

    def setNodeAtribute(self,pos, str, value):
        self.graph.node[pos][str] = value

    def getNodes(self):
        return self.graph.nodes()

    def getNeighbors(self,pos):
        return self.graph.neighbors(pos)

    def getValue(self,pos):
        list_v = self.graph.node[pos]['value']
        return list_v[len(list_v)-1]

    def getValues(self,pos):
        return self.graph.node[pos]['value']

    def changeStatus(self,pos,status):
        self.setNodeAtribute(pos,'mode',status)

    def checkStatus(self,pos):
        return self.graph.node[pos]['mode']

    def updateValue(self,pos,val):
        list_v = self.graph.node[pos]['value']
        list_v.append(val)
        self.setNodeAtribute(pos,'value',list_v)
    
    def clearInbox(self,pos):
        self.graph.node[pos]['inbox'] = []

    def checkInbox(self,pos):
        self.x_lock.acquire() 
        list_m = self.graph.node[pos]['inbox']
        if  self.graph.node[pos]['mode'] == 'idle' and len(list_m)==1:
            self.setNodeAtribute(pos,'mode','member')
            self.x_lock.release()
            return list_m
        if  self.graph.node[pos]['mode'] == 'idle' and len(list_m)>1:
            self.updateValue(pos,self.getValue(pos))
            self.x_lock.release()
            return None
        if self.graph.node[pos]['mode'] == 'member':
            self.x_lock.release()
            return list_m
        if self.graph.node[pos]['mode'] == 'leader':
            self.x_lock.release()
            return list_m
        else:
            self.updateValue(pos,self.getValue(pos))
            self.x_lock.release()
            return None

    def sendMessage(self, dest, m):
        self.x_lock.acquire()
        list_m = self.graph.node[dest]['inbox']
        list_m.append(m)
        self.setNodeAtribute(dest,'inbox',list_m)
        self.x_lock.release()


