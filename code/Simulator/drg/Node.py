import Network
import time

class Node(object):

    net = None
    pos = None
    leader = None
    list_sums = None
    list_stat = None
    list_count = None
    avg = None
    count =  None
    list_Neighbors = None

    def __init__(self,net, pos):     
        self.net = net
        self.pos = pos
        self.list_Neighbors = self.net.getNeighbors(self.pos)
        self.avg = self.net.getInitVal(self.pos)
        self.count = 0.0
        self.list_stat = []
        self.list_sums = []
        self.list_count = []
        self.list_count.append(self.count)
        self.list_stat.append(self.avg)
        self.list_sums.append(self.avg)
    
    def sendLeaderMessage(self,st,value=None,count=None):
        if value is None and count is None:
              m = (st,self.pos)
        else:
              m =(st,self.pos,value,count)
        for i in range(0,len(self.list_Neighbors)):
            self.net.sendMessage(self.list_Neighbors[i],m)

    def setCount(self):
        self.count = 1.0

    def sendValue(self):
        if self.net.checkStatus(self.pos) == 'member':
            vj = self.avg
            cj = self.count
            dest = self.leader
            m = ('JACK',dest,vj,cj,1.0) 
            self.net.sendMessage(dest,m)

    def computeAvg(self,list_m):
        n = 1.0
        vk = self.avg
        if len(list_m) == 0:
            return 0
        for i in range(0,len(list_m)):
            vk += list_m[i][2]
            n += 1.0
            return float(vk/n)

    def getCount(self,r):
        return 133*self.list_count[r]
    
    
    def computeCount(self,list_m):
        n = 1.0
        vk = self.count
        if len(list_m) == 0:
            return 0
        for i in range(0,len(list_m)):
            vk+= float(list_m[i][3])
            n += 1.0
        return float(vk/n)

    def getEstimate(self, r):
        return self.list_stat[r]

    def getSumPerRound(self, r):
        return self.list_sums[r]

    def getJACKS(self, list_m):
        aux = []
        for i in range(0,len(list_m)):
            if list_m[i][0] == 'JACK':
                aux.append(list_m[i])
        return aux

    def getGAM(self,list_m):
        list_gams = []
        for i in range(0,len(list_m)):
            if list_m[i][0] == 'GAM':
                 list_gams.append((list_m[i][2],list_m[i][3]))
        return list_gams

    def printLenV(self):
        print len(self.net.getValues(self.pos))

    def start(self, leaderToken):
        if leaderToken == 1 :
            self.net.changeStatus(self.pos,'leader')
            self.sendLeaderMessage('GCM')
            time.sleep(1)
            list_m = self.net.checkInbox(self.pos)
            list_j = self.getJACKS(list_m)
            avg =  self.computeAvg(list_j)
            count = self.computeCount(list_j)
            if avg>0.0:
               self.sendLeaderMessage('GAM',value=avg,count=count)
               self.avg = avg
               self.count = count
            if self.count > 0.0:
                self.list_sums.append(self.avg*self.count)
            else:                
                self.list_sums.append(self.list_sums[len(self.list_sums)-1]*133.0)
            self.list_count.append(self.count)
            self.list_stat.append(self.avg)
            self.net.changeStatus(self.pos,'idle')
            self.net.clearInbox(self.pos)
        else:
            time.sleep(0.5)
            list_m = self.net.checkInbox(self.pos)
            if (list_m is None) == False:
                    self.leader = list_m[0][1]
                    self.sendValue()
                    time.sleep(0.5)
                    list_m = self.net.checkInbox(self.pos)
                    list_gams = self.getGAM(list_m)
                    if len(list_gams) > 0:
                        self.avg = list_gams[0][0]
                        self.count = list_gams[0][1]
            if self.count > 0.0:
                self.list_sums.append(self.avg/self.count)
            else:
                self.list_sums.append(self.list_sums[len(self.list_sums)-1]*133.0)
            self.list_stat.append(self.avg)
            self.list_count.append(self.count)
            self.net.changeStatus(self.pos,'idle')
            self.net.clearInbox(self.pos)

