import networkx as nx
import random


class Network(object):

	graph = None

	def __init__(self, n):
		self.graph = nx.random_geometric_graph(n,0.8)
		if not nx.is_connected(self.graph):
			self.graph =  nx.is_connected_component_subgraphs(self.graph)[0]
		for i in range(0,len(self.graph.nodes()))
		    list_m = []
		    
