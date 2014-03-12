import vectorUtils as vector

class Message(object):

    v = None
    rd = None

    def __init__(self,rd,l=None, indice=None,v=None):
        if (indice is None) and (l is None)  :
           self.v = v
           rd = rd
        else :
           self.v = vector.initVector(l,indice)
           self.rd = rd
    
    def getV(self):
        return self.v

    def getRound(self):
    	return self.rd

    def toString(self):
    	return '%d'%self.rd