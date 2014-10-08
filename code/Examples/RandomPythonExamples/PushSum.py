import Network as ntw

class PushSum(object):
    
    net = None

	def __init__(self,n):
		self.net = ntw.Network(n)


p = PushSum(5)