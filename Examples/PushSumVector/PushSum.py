import Network as netwk
import Node as nd
import Message as msg
import threading
import time

class pushSum(object):

   net = None
   nodes = {}

   class serviceNode(threading.Thread):
  
       pos = None 
       rd = None

       def __init__(self, pos, rd):
         self.pos = pos
         self.rd = rd
         threading.Thread.__init__(self)

       def run(self):
         i = 1
         while i <= self.rd:
           self.pos.main(i)
           time.sleep(1)
           i+=1

   def __init__(self):
    #create a new random geomatric network
    self.net = netwk.Network(1000)
    #get the list of created node to initialize Node objects
    list_nodes = self.net.getNodes()
    for i in range(0,len(list_nodes)):
      self.nodes[i] = nd.Node(self.net,list_nodes[i])

   def startRounds(self,n):
      #in each new round, start the Push-Sum Algorithm
      for i in range(0,len(self.nodes)-1):
        thread1 = self.serviceNode(self.nodes[i],n)
        thread1.start()

   def logMessage(self):
    #log the avarage
   	self.net.logMessages()


#initialize the protocol
p = pushSum()
p.startRounds(50)
p.logMessage()