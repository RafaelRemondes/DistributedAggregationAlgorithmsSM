import Network
import time

class Node(object):

    net = None
    pos = None
    leader = None
    list_Neighbors = None
    

    def __init__(self,net, pos):
        self.net = net
        self.pos = pos
        self.list_sending = []
        self.list_noM = []
        self.list_Neighbors = self.net.getNeighbors(self.pos)
    
    def sendLeaderMessage(self,str,value=None):
        if value is None:
              m = (str,self.pos)
        else:
              m =(str,self.pos,value)
        for i in range(0,len(self.list_Neighbors)):
            self.net.sendMessage(self.list_Neighbors[i],m)

    def sendValue(self):
        if self.net.checkStatus(self.pos) == 'member':
            vj = self.net.getValue(self.pos)
            dest = self.leader
            m = ('JACK',dest,vj,1) 
            self.net.sendMessage(dest,m)

    def computeAvg(self,list_m):
        n = 0
        vk = 0
        if len(list_m) == 0:
            return 0
        for i in range(0,len(list_m)):
            vk +=list_m[i][2]
            n += list_m[i][3]
            return vk/n

    def getEstimate(self, r):
        return self.net.getValues(self.pos)[r]

    def getJACKS(self, list_m):
        aux = []
        for i in range(0,len(list_m)):
            if list_m[i][0] == 'JACK':
                aux.append(list_m[i])
        return aux

    def getGAM(self,list_m):
        for i in range(0,len(list_m)):
            if list_m[i][0] == 'GAM':
                return list_m[i][2] 
        return 0

    def printLenV(self):
        print len(self.net.getValues(self.pos))

    def start(self, rd, leaderToken):
        if leaderToken == 1 :
            self.net.changeStatus(self.pos,'leader')
            self.sendLeaderMessage('GCM')
            time.sleep(5)
            list_m = self.net.checkInbox(self.pos)
            avg =  self.computeAvg(self.getJACKS(list_m))
            if avg>0:
               self.sendLeaderMessage('GAM',value=avg)
            else:
                avg = self.net.getValue(self.pos)
            self.net.updateValue(self.pos,avg)
            self.net.changeStatus(self.pos,'idle')
            self.net.clearInbox(self.pos)
        else:
            time.sleep(2)
            list_m = self.net.checkInbox(self.pos)
            if (list_m is None) == False:
                    self.leader = list_m[0][1]
                    self.sendValue()
                    time.sleep(2)
                    list_m = self.net.checkInbox(self.pos)
                    value = self.getGAM(list_m)
                    if value > 0:
                        self.net.updateValue(self.pos,value)
                    else:
                        self.net.updateValue(self.pos, self.net.getValue(self.pos))
            self.net.changeStatus(self.pos,'idle')
            self.net.clearInbox(self.pos)

