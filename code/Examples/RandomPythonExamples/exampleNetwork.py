from lxml import etree
from lxml import objectify
import networkx as nx
import matplotlib.pyplot as plt


file = "VoorRafael.xml"
nodes = []
edges = []
tree = etree.parse(file)
root = tree.getroot()
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
print len(nodes)
print len(edges)
for i in range(0,len(edges)):
	graph.add_edge(edges[i][0],edges[i][1], weight = int(float(edges[i][2])))
pos = nx.graphviz_layout(graph, prog='sfdp', args='')
list_nodes = graph.nodes()
plt.figure(figsize=(20,10))
nx.draw(graph, pos, node_size=20, alpha=0.4, nodelist=list_nodes, node_color="blue", with_labels=False)
plt.savefig('graphNX.png')
plt.show()





