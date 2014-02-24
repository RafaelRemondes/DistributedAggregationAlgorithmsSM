import random
import networkx as nx 
import matplotlib.pyplot as plt
from random import choice #usar para escolher aleatoriamente um nodo para ser SINK


class Network(object):

    graph = None
    ACTUAL_SINK = None
    VISITED_NODES = {}
    nr = None


    def __init__(self, n):
       n 
       self.randomSINK()

    def randomSINK(self):
       nodes_list = self.graph.nodes()
       self.ACTUAL_SINK = choice(nodes_list) # escolher aleatoriamente um nodo para ser sink a partir da lista de nodos usando o choice
       self.graph.node[self.ACTUAL_SINK]['sink'] = self.ACTUAL_SINK

    def randomTour(self,n):
    	nodes_list = self.graph.nodes()
    	current_node = choice(nodes_list)
    	i=0
    	while i<=n:
    	   if ('visited' in self.graph.node[current_node]) == False and ('sink' in self.graph.node[current_node]) == False:
    	     self.VISITED_NODES[len(self.VISITED_NODES)-1] = current_node
    	     self.graph.node[current_node]['visited'] = current_node
           list_neighbors = self.graph.neighbors(current_node)
    	   current_node = choice(list_neighbors)
    	   i+=1
    	print 'Visited Nodes %d.'%len(self.VISITED_NODES)

    def draw(self):
       pos = nx.graphviz_layout(self.graph, prog='sfdp', args='')
       list_nodes = self.graph.nodes()
       for j in range(0,len(self.VISITED_NODES)-1):
          list_nodes.remove(self.VISITED_NODES[j])
       list_nodes.remove(self.ACTUAL_SINK) # remover o sink para desenhar todos a azul menos o sink
       plt.figure(figsize=(20,10))
       nx.draw(self.graph, pos, node_size=20, alpha=0.4, nodelist=list_nodes, node_color="blue", with_labels=False)
       nx.draw_networkx_nodes(self.graph, pos,
							   node_size=60, alpha=0.5, nodelist=[self.ACTUAL_SINK], 
							   node_color='red',with_labels=False)
       for i in range(0,len(self.VISITED_NODES)-1):
         nx.draw_networkx_nodes(self.graph, pos,
							   node_size=60, alpha=0.5, nodelist=[self.VISITED_NODES[i]], 
							   node_color='green',with_labels=False)
       plt.savefig('graphNX.png')
       plt.show()


G = Network(500)
G.randomTour(500)
G.draw()