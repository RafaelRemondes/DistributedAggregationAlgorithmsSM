import networkx as nx
from lxml import etree
from lxml import objectify
from random import choice
import matplotlib.pyplot as plt
import graphUtils as utils

def initGraph(sample, t):
    sample = "/Users/rafaelremondes/UM/MEI/Thesis/DistributedAggregationAlgortihmsSM/code/NetworkSamples/"+sample
    graph = loadSample(sample)
    if not nx.is_connected(graph):
        graph = nx.connected_component_subgraphs(graph)[0]
    draw(graph)
    graph = utils.transformation("dissorsativity",t,graph)
    draw(graph)
    graph = utils.transformation("assorsativityHD",t,graph)
    draw(graph)
    graph = utils.transformation("assorsativityLD",t,graph)
    draw(graph)
    graph = utils.transformation("trianguleClosure",t,graph)
    draw(graph)
    #print "Node Degree: %.2f"%utils.getNodeDegree(graph)
    #print "AVG CC: %.2f"%utils.getAvgCC(graph)
    #print "Characteristic Path Length: %.2f"%utils.getCPL(graph)
    #print "Average Path Length: %.2f"%utils.getAPL(graph)
    return graph

def draw(graph):
       pos = nx.graphviz_layout(graph, prog='sfdp', args='')
       list_nodes = graph.nodes()
       plt.figure(figsize=(20,10))
       nx.draw(graph, pos, node_size=20, alpha=0.4, nodelist=list_nodes, node_color="blue", with_labels=False)
       plt.savefig('graphNX.png')
       plt.show()

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
                      if(subelement.tag == "source" or subelement.tag == "sink" or subelement.tag == "lengthInMeters" or subelement.tag == "averageResistanceOhmPerKm"):
                           aux.append(subelement.text)
                edges.append(aux)
        graph = nx.Graph()
        for i in range(0,len(edges)):
            weight1 = 1
            if(len(edges[i])>3):
                weight1 = int(float(edges[i][3]))
            weight = int(((float(edges[i][2]))/1000)*weight1)
            graph.add_edge(edges[i][0],edges[i][1], weight = weight)
        return graph


#graph = initGraph("sample1.xml",0.0)
graph = initGraph("sample1.xml",0.75)



