import networkx as nx
import Utils as u
import threading

class Network(object):

     graph = None
     x_lock = threading.Lock()


     def __init__(self,n,k):
          self.graph = nx.random_geometric_graph(n,0.8)
          if not nx.is_connected(self.graph):
               self.graph = nx.is_connected_component_subgraphs(self.graph)[0]
          for i in range(0,len(self.graph.nodes())):
               self.initializeNode(i,k)

     def initializeNode(self,pos,k):
          x = u.initArray(k)
          self.graph.node[pos]['Round'] = 0
          self.graph.node[pos]['Set'] = x
          self.graph.node[pos]['Requests'] = []
          self.graph.node[pos]['Inbox'] = []

     def getNodes(self):
          return self.graph.nodes()

     def getNeighbors(self,pos):
          return self.graph.neighbors(pos)

     def getA(self, pos):
          return self.graph.node[pos]['Set']

     def updateRound(self,pos,r):
          self.graph.node[pos]['Round'] = r

     def checkRound(self, rd,pos):
          return (rd == self.graph.node[pos]['Round'])

     def checkInbox(self,rd,pos,dest):
     	  self.x_lock.acquire()
          list_m = self.graph.node[pos]['Inbox']
          for i in range(0,len(list_m)):
               if rd == list_m[i][0] and dest == list_m[i][1]:
                  a = list_m[i]
                  list_m.remove(list_m[i])
                  self.graph.node[pos]['Inbox'] = list_m
                  self.x_lock.release()
                  return a[2]
          self.x_lock.release()
          return None
    
     def checkRequests(self,rd,pos):
          self.x_lock.acquire()
          list_r = self.graph.node[pos]['Requests']
          for i in range(0,len(list_r)):
               if rd == list_r[i][0]:
               	    self.x_lock.release()
               	    dest = list_r[i][1]
               	    list_r.remove(list_r[i])
                    return dest
          self.x_lock.release()
          return None

     def sendArray(self,rd,pos,dest,a):
          self.x_lock.acquire()
          m = (rd,pos,a)
          list_m = self.graph.node[dest]['Inbox']
          list_m.append(m)
          self.graph.node[dest]['Inbox'] = list_m
          self.x_lock.release()

     def sendRequest(self,rd,pos,dest):
          self.x_lock.acquire()
          r = (rd,pos)
          list_r = self.graph.node[dest]['Requests']
          list_r.append(r)
          self.graph.node[dest]['Requests'] = list_r
          self.x_lock.release()

     def updateA(self, pos, a):
          self.graph.node[pos]['A'] = a

     def isRequestsEmpty(self,pos):
          return self.graph.node[pos]['Requests'] == []




