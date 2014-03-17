class Message(object):

   q = None
   w = None
   rd = None

   def __init__(self, q, w, rd):
      self.q = q
      self.w = w
      self.rd = rd

   def getRound(self):
      return self.rd

   def getQ(self):
      return self.q
   
   def getW(self):
      return self.w
