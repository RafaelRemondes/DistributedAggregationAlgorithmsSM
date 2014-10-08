import networkx as nx
from random import choice
import numpy
import math
from lxml import etree
from lxml import objectify

def loadSample(sample):
        file = sample
        nodes = []
        edges = []
        root = etree.parse(file).getroot()
        for element in root.iter("*"):
            if(element.tag == "node" ):
                aux = []
                for subelement in element.iter("*"):
                      aux.append(subelement.text)
                nodes.append(aux)
            if(element.tag == "edge"):
                aux = []
                for subelement in element.iter("*"):
                      if(subelement.tag == "source" or subelement.tag == "sink" or subelement.tag == "lengthInMeters"):
                           aux.append(subelement.text)
                edges.append(aux)
        graph = nx.Graph()
        for i in range(0,len(edges)):
            graph.add_edge(edges[i][0],edges[i][1], weight = int(float(edges[i][2])))
        return graph


#--------TRANSFORMATIONS---------#

def transformation(t_type,n,graph):
    nrEdges = int(round(n*len(graph.edges())))
    print t_type
    if t_type == "random":
        for i in range(0,nrEdges):
          node1 = choice(graph.nodes())
          node2 =  choice(graph.nodes())
          while(graph.has_edge(node1,node2)):
             node1 = choice(graph.nodes())
             node2 = choice(graph.nodes())
          graph.add_edge(node1,node2)
    else:
     if t_type == "trianguleClosure":
         while nrEdges > 0:
            node1 = choice(graph.nodes())
            list_n = graph.neighbors(node1)
            for i in range(0,len(list_n)):
                for j in range(0,len(list_n)):
                    if list_n[i] != list_n[j] and graph.has_edge(list_n[i],list_n[j]) is False:
                        graph.add_edge(list_n[i],list_n[j])                    
                        nrEdges-=1
     else:
        if t_type == "dissorsativity":
           list_nodes = nodesPerNodeDregreeDissorsativity(graph)
        if t_type == "assorsativityHD":
            list_nodes = nodesPerNodeDregreeAssorsativityHD(graph)
        if t_type == "assorsativityLD":
            list_nodes = nodesPerNodeDregreeAssorsativityLD(graph)
        for i in range(0,nrEdges):
          j = 0
          node1 = list_nodes[j][0]
          node2 = list_nodes[j][1]
          while(graph.has_edge(node1,node2)):
            j+=1
            node1 = list_nodes[j][0]
            node2 = list_nodes[j][1]
          graph.add_edge(node1,node2)
    return graph

def nodesPerNodeDregreeDissorsativity(graph):
    list_aux = graph.nodes()
    list_nodes = []
    for i in range(0,len(list_aux)):
        for j in range(0,len(list_aux)):
            if list_aux[i] != list_aux[j]:
               dif = int(math.sqrt(pow(len(graph.neighbors(list_aux[i]))-len(graph.neighbors(list_aux[j])),2)))
               list_nodes.append((list_aux[i],list_aux[j],dif))
    list_nodes.sort(key=lambda tup: tup[2],reverse=True)
    return list_nodes

def nodesPerNodeDregreeAssorsativityHD(graph):
    list_aux = graph.nodes()
    list_nodes = []
    for i in range(0,len(list_aux)):
        for j in range(0,len(list_aux)):
            if list_aux[i] != list_aux[j] and len(graph.neighbors(list_aux[i]))==len(graph.neighbors(list_aux[j])):
               list_nodes.append((list_aux[i],list_aux[j],len(graph.neighbors(list_aux[i]))))
    list_nodes.sort(key=lambda tup: tup[2],reverse=True)
    return list_nodes


def nodesPerNodeDregreeAssorsativityLD(graph):
    list_aux = graph.nodes()
    list_nodes = []
    for i in range(0,len(list_aux)):
        for j in range(0,len(list_aux)):
            if list_aux[i] != list_aux[j] and len(graph.neighbors(list_aux[i]))==len(graph.neighbors(list_aux[j])):
               list_nodes.append((list_aux[i],list_aux[j],len(graph.neighbors(list_aux[i]))))
    list_nodes.sort(key=lambda tup: tup[2])
    return list_nodes


#------------PROPRIETIES-----------#

def getNodeDegree(graph):
     n = len(graph.nodes())
     m = len(graph.edges())
     return round(2*m/n)

def getCCperNode(graph,node):
    return nx.clustering(graph,nodes=node)

def getAvgCC(graph):
    return nx.average_clustering(graph)

def getWeight(graph, path):
    distance = 0.0
    for i in range(0,len(path)):
        if i+1 < len(path):
           node1 = path[i]
           node2 = path[i+1]
           distance += graph.edge[node1][node2]['weight']
    return distance

def getCPL(graph):
    list_cpl =  []
    aux = 0.0
    for i in range(0,len(graph.nodes())):
        node = graph.nodes()[i]
        for j in range(0,len(graph.nodes())):
            node1 = graph.nodes()[j]
            if (node1 == node) is False and nx.has_path(graph, node, node1):
               aux += getWeight(graph,nx.shortest_path(graph,source=node,target=node1))
        cpl = (1.0/(len(graph.nodes())-1.0))*aux
        list_cpl.append(cpl)
        aux = 0.0
    cpl =  numpy.median(list_cpl)
    return cpl


def getAPL(graph):
    for i in range(0,len(graph.nodes())):
        node = graph.nodes()[i]
        aux = 0.0
        for j in range(0,len(graph.nodes())):
            node1 = graph.nodes()[j]
            if (node1 == node) is False and nx.has_path(graph, node, node1):
               aux += getWeight(graph,nx.shortest_path(graph,source=node,target=node1))
    apl = (1.0/(len(graph.nodes())*(len(graph.nodes())-1.0)))*aux
    return apl






