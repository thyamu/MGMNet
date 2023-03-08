### To generate graphs in gexf format for visulation ###
#0. biosphere with 1, 2 and 3 embeded
#1. archaeasphere
#2. bacteriasphere
#3. eukaryasphere

### Attributes to add
# 0. degree (default)
# 1. domain
# 2.
#

import networkx as nx
g = nx.complete_graph(10)

# dict_freq = {}
# for line in freqFile:
#     items = line.rstrip().split('\t')
#     subName = items[0]
#     dict_freq[subName] = float(items[1])
#
# for n in g.nodes_iter():
#     if n in dict_freq.keys():
#         f = dict_freq[n]
#     else:
#         f = 0.0
#     g.add_node(n, freq = f)


for i, j in g.edges_iter():
    g.add_edge(i,j, weight=1)

g.add_edge(1, 2, weight=10)
g.add_edge(2, 3, weight=10)
g.add_edge(3, 4, weight=10)
g.add_edge(4, 1, weight=10)
g.add_edge(2, 4, weight=10)
g.add_edge(3, 1, weight=10)

for n in g.nodes_iter():
    g.add_node(n, attr=1)

g.add_node(1, attr=10)
g.add_node(2, attr=10)
g.add_node(3, attr=10)
g.add_node(4, attr=10)

nx.write_gexf(g, '../viz/test2.gexf')
