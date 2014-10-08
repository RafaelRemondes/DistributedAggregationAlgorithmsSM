import random
import Network
import time
import Message as msg


class Node(object):

    net = None
    pos = None
    nodesToBroadCast = None
    qti = None
    alpha = None

    def __init__(self, net, pos):
      self.net = net
      self.pos = pos
      self.nodesToBroadCast = self.net.getNodes()
      self.alpha = 1.0/len(self.nodesToBroadCast)

    def calculateW(self,list_m):
       sm = 0.0
       for i in range(0,len(list_m)):
           sm = sm + list_m[i].getW()
       return sm

    def calculateProbabilities(self, list_m, w):
      list_p = []
      for i in range(0,len(list_m)):
        list_p.append(list_m[i].getW()/w)
      return list_p

    def listQ(self,list_m):
        list_q = []
        for i in range(0,len(list_m)):
          list_q.append(list_m[i].getQ())
        return list_q

    def chooseAtRandom(self,list_q,list_p):
      x = random.uniform(0,1)
      cumulative_probabilty = 0.0
      for item, item_probabilty in zip(list_q,list_p):
        cumulative_probabilty += item_probabilty
        if x < cumulative_probabilty: 
          break
      return item


    def calculateQ(self,list_m):
       list_q = self.listQ(list_m)
       list_p = self.calculateProbabilities(list_m,self.calculateW(list_m))
       q = self.chooseAtRandom(list_q,list_p)
       return q

    def computeMessage(self,rd):
      list_m = self.net.getMessagesByRound(self.pos,rd-1)
      w = self.calculateW(list_m)
      q = self.calculateQ(list_m)
      return msg.Message(self.alpha*q,w*self.alpha,rd) 

    def broadcast(self, m):
       for i in range(0, len(self.nodesToBroadCast)):
         self.net.sendMessage(m,self.nodesToBroadCast[i])

    def sendMessage(self,rd):
       m =  self.computeMessage(rd)
       self.broadcast(m)

    def updateQ(self,rd):
        list_q = self.listQ(self.net.getMessagesByRound(self.pos,rd))
        self.qti = random.choice(list_q)

    def getQti(self):
    	return self.qti

    def main(self,rd):
      self.sendMessage(rd)
      self.updateQ(rd)
