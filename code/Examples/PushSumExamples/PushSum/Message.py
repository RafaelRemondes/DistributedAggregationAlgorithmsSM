class Message(object):

    s = 0.0
    w = 0.0
    rd = 0

    def __init__(self, s, w, rd):
        self.s = s
        self.w = w
        self.rd = rd
    
    def getS(self):
        return self.s
    
    def setS(self,s):
        self.s += s

    def getW(self):
        return self.w

    def getRound(self):
    	return self.rd

    def toString(self):
    	return '%d'%self.rd