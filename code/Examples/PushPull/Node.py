import Network
import threading
import time
from random import choice


class Node(object):
     
     net = None
     pos = None
     val = None
     list_neighbors = None
     list_stat = None
     list_size = None
     list_sum = None
     
     class onSend(threading.Thread):
         
         dest = None
         net = None
         pos = None
         val =  None

         def __init__(self, net, pos,dest, val):
            self.dest = dest 
            self.net = net
            self.pos = pos
            self.val = val
            threading.Thread.__init__(self)

         def run(self):
            i = 0
            x = self.val
            size = self.net.getSize(self.pos)
            m = (self.dest,self.pos,self.val,size)
            self.net.sendMessage(m)
            m = self.net.checkInbox(self.pos, dest=self.dest)
            if m is not None:
               x = m[2]
               self.val = (x+self.val)/2.0
               size = (size+m[3])/2.0
               self.net.setInitVal(self.pos,x)
               self.net.setSize(self.pos,size)

     class onReceive(threading.Thread):

         dest = None
         net = None
         pos = None
         val =  None

         def __init__(self, net, pos):
            self.net = net
            self.pos = pos
            threading.Thread.__init__(self)

         def run(self):
            while 1 and self.net.isProtocolOn():
                size = self.net.getSize(self.pos)
                self.val = self.net.getInitVal(self.pos)
                m =  self.net.checkInbox(self.pos)
                if m is not None:
                   x = m[2]
                   y = m[3]
                   dest = m[1]
                   m = (dest,self.pos,self.val,size)
                   self.net.sendMessage(m)
                   self.val = (self.val+x)/2.0
                   size = (size+y)/2.0
                   self.net.setInitVal(self.pos,self.val)
                   self.net.setSize(self.pos,size)

     def __init__(self,net,pos,sq):
        self.net = net
        self.list_stat = []
        self.pos = pos
        self.list_neighbors = self.net.getNeighbors(self.pos)
        self.list_size = []
        self.list_size.append(self.net.getSize(self.pos))
        self.list_sum = []
        self.list_stat.append(sq)
        self.list_sum.append(sq)
        self.val = sq

     def startReceive(self):
        onreceive = self.onReceive(self.net,self.pos)
        onreceive.start()

     def printAVG(self):
        avg =  self.net.getInitVal(self.pos)
        #print avg
        return avg

     def getPos(self):
        return self.pos 

     def printSize(self):
        size = self.net.getSize(self.pos)
        size = size*133.0
        print size

     def getSum(self):
        return self.list_sum[len(self.list_sum)-1]

     def updateAvg(self):
        x = self.net.getInitVal(self.pos)
        self.list_stat.append(x)

     def updateSize(self):
        x = self.net.getSize(self.pos)
        y =  self.net.getInitVal(self.pos)
        if x > 0.0:
           self.list_sum.append(y/x)
        self.list_size.append(x)

     def main(self):
        dest = choice(self.list_neighbors)
        val = self.net.getInitVal(self.pos)
        onsend = self.onSend(self.net,self.pos,dest,val)
        onsend.start()
        onsend.join()
        time.sleep(1)
        self.updateAvg()
        self.updateSize()

