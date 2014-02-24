class Message(object):

    s = None
    w = None
    rd = None

    def __init__(self, s, w, rd):
        self.s = s
        self.w = w
        self.rd = rd
    
    def getS(self):
        return self.s

    def getW(self):
        return self.w

    def getRound(self):
    	return self.rd

    def toString(self):
    	return '%d'%self.rd