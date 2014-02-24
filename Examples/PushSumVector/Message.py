import vectorUtils as vector

class Message(object):

    v = None
    rd = None

    def __init__(self, length,indice, rd):
        self.v = vector.initVector(length,indice)
        self.rd = rd

    def __init__(self,v,rd):
        self.v = v
        rd = rd
    
    def getV(self):
        return self.v

    def getRound(self):
    	return self.rd

    def toString(self):
    	return '%d'%self.rd