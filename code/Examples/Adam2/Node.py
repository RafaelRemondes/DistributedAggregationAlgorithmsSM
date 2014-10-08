import Network
import Message as msg
import Utils as utils
from random import choice
import threading
import time

class Node(object):
    
    pos = None
    net = None

    class onSend(threading.Thread):

       net = None
       pos = None
       rd = None
       w = None

       def __init__(self,net,pos,rd,w):
       	  self.net = net
       	  self.pos = pos
          self.rd = rd
       	  self.w =w
          threading.Thread.__init__(self)

       def run(self):
           dest = self.net.selectRandomNeighbour(self.pos)
           hp =  self.net.getH(self.pos)
       	   m = msg.Message(self.rd, self.pos, hp, self.w, dest)
       	   self.net.send(m)
           m = None
           while m is None:
       	      m = self.net.checkInbox(self.pos,dest = dest)
       	   h = utils.merge(hp,m.getH(),self.net.getA(self.pos))
       	   self.net.updateH(self.pos,h)
     

    class onReceive(threading.Thread):

       net = None
       pos = None
       w = None
       rd = None

       def __init__(self,net,pos,rd,w):
       	  self.net = net
       	  self.pos = pos
       	  self.rd = rd
       	  self.w =w
          threading.Thread.__init__(self)

       def run(self):
       	 while self.net.getRound(self.pos) == self.rd:
       	    m1 = self.net.checkInbox(self.pos,rd = self.rd)
       	    if (m1 is None) == False:
               hp = self.net.getH(self.pos)
               m2 = msg.Message(self.rd, self.pos, hp, self.w, m1.getNode()) 
               self.net.send(m2)
               hq =  m1.getH()
               h = utils.merge(hp,hq,self.net.getA(self.pos))
               self.net.updateH(self.pos,h)

    def __init__(self,net,pos):
      self.net = net
      self.pos = pos

    def startInstance(self, t):
        ti = t
        h = [] 
        for i in range(0,len(t)):
            if self.net.getA(self.pos) <= t[i]:
                fi = 1
            else:
                fi = 0
            h.append((ti,fi))
        self.net.updateH(self.pos,h)

    def finishRound(self):
       self.net.updateRound(self.pos,self.net.getRound(self.pos)+1)

    def startRound(self,rd):
      self.net.updateRound(self.pos,rd)
      print self.net.getRound(self.pos)
      threadOnReceive = self.onReceive(self.net,self.pos,rd,1)
      threadOnSend = self.onSend(self.net,self.pos,rd,1)
      threadOnReceive.start()
      threadOnSend.start()
      threadOnSend.join(0.1)


