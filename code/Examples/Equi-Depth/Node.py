from random import choice
import Utils as utils
import time
import Network
import threading

class Node(object):
    
    net = None
    pos = None
    neighbors = None

    class onSend(threading.Thread):

        net = None
        pos = None
        dest = None
        rd = None

        def __init__(self,net, pos, dest, rd):
            self.net = net
            self.pos = pos
            self.dest = dest
            self.rd = rd
            threading.Thread.__init__(self)

        def run(self):
            self.net.sendRequest(self.rd,self.pos,self.dest)
            a1 = None
            while a1 is None and self.net.checkRound(self.rd, self.pos) == True:
                a1 = self.net.checkInbox(self.rd,self.pos,self.dest)
            if (a1 is None) == False:
                a = self.net.getA(self.pos)
                self.net.updateA(self.pos,utils.merge(a,a1))

    class onReceive(threading.Thread):

        net = None
        pos = None
        rd = None

        def __init__(self,net, pos,rd):
           self.net = net
           self.pos = pos
           self.rd = rd
           threading.Thread.__init__(self)

        def run(self):
            while self.net.checkRound(self.rd, self.pos) == True and self.net.isRequestsEmpty(self.pos) == False : 
                pos = self.net.checkRequests(self.rd,self.pos)
                if (pos is None) == False:
                     self.net.sendArray(self.rd,self.pos,pos,self.net.getA(self.pos))

    def __init__(self, pos, net):
        self.net = net
        self.pos = pos
        self.neighbors = self.net.getNeighbors(self.pos)

    def finishRound(self):
        self.net.updateRound(self.pos,0)

    def start(self, n):
        self.net.updateRound(self.pos,n)
        j =  choice(self.neighbors)
        threadOnSend = self.onSend(self.net,self.pos,j,n)
        threadOnReceive = self.onReceive(self.net, self.pos,n)
        threadOnReceive.start()
        threadOnSend.start()
        threadOnSend.join(0.1)
