import vectorUtils

class Node(object):

    list_neighbors = None
    pos = None
    net = None
    
    def __init__(self,pos,net):    
       self.pos = pos    
       self.net = net    
       self.list_neighbors = self.net.getNeighbors(self.pos)

    def send(self):
       x = self.net.getX(self.pos)
       for i in range(0,len(self.list_neighbors)):
          self.net.send(x,i)

    def update(self):
        list_m = self.net.getM(self.pos)
        x = self.net.getX(self.pos)
        for i in range(0,len(list_m)):
           x = vectorUtils.pointWiseMinimum(x,list_m[i])
        self.net.setX(self.pos,x)

    def computeNx(self, k):
    	x = self.net.getX(self.pos)
    	sumX = 0.0
    	for i in range(0,k):
    		sumX += x[i]
    	return (k-1)/sumX



