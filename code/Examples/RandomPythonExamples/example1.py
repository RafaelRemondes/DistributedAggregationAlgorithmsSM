import networkx as nx
import pygraphviz as pyGR
import math


H = pyGR.AGraph()
G = nx.Graph(day='Friday')
G1 = nx.Graph()
e=[('a','b',0.3),('b','c',0.9),('a','c',0.5),('c','d',1.2)]
H.add_edge('a','b',0.3)
H.add_edge('b','c',0.9)
H.add_edge('a','c',0.5)
H.add_edge('c','d',1.2)
G.add_weighted_edges_from(e)
G1.add_edges_from(G.edges())
#dijkstra algorithm for the graph
print(nx.dijkstra_path(G, 'a','d'))
print(nx.dijkstra_path(G1, 'a','d'))

print(len(G))

#for each node and node's neighbors dict
for n,nbrsdict in G.adjacency_iter():
	#for each neighbor and edge atribute
	for nbr, eattr in nbrsdict.items():
		#print the node neighbor and the edge's weight
		if 'weight' in eattr:
			print(n,nbr,eattr['weight'])
H.layout()
H.draw('example.png')
