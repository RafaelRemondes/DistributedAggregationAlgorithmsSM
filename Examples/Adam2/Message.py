class Message(object):

    node = None
    h = None
    w = None
    rd = None
    dest = None

    def __init__(self,rd, pos, h, w,dest):
        self.rd = rd
        self.node = pos
        self.h = h
        self.w = w
        self.dest = dest

    def getNode(self):
        return self.node

    def getRound(self):
        return self.rd

    def getH(self):
        return self.h

    def getW(self):
        return self.w

    def getDest(self):
        return self.dest
