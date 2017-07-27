import os
import numpy as np
import kegg as kg
import bionets as bn
import igraph as ig
import networkx as nx

import time

kegg = kg.Kegg()


rxn_list = bn.loadRxns('ecosystem', 'YNP', 3)
se = bn.subEdges(rxn_list, kegg.rxn_reac, kegg.rxn_prod)

#igraph

## graph object
G = ig.Graph.TupleList(se)
## largest component
cl = G.clusters()
lcc = cl.giant()
#print lcc.vcount()
## average shortest length
ave_spl_lcc = lcc.average_path_length(directed=False, unconn=True)


## average clustering coefficient
#ave_cc_lcc = lcc.transitivity_undirected()
#print ave_cc_lcc

start_time = time.time()
list_local_cc_lcc = lcc.transitivity_local_undirected(mode='zero')

print list_local_cc_lcc[:5]

ave_cc_lcc_from_local = np.mean(list_local_cc_lcc)

#print "time for clustering coefficient: igraph ", time.time() - start_time
print ave_cc_lcc_from_local


g_nx = nx.Graph(se)
g_lcc_nx =  max(nx.connected_component_subgraphs(g_nx), key=len)


#print g_lcc_nx.number_of_nodes()

start_time = time.time()
cluster_list = nx.clustering(g_lcc_nx)

print cluster_list.values()[:5]
avg_clustering_lcc_nx = np.mean(cluster_list.values())
print "time for clustering coefficient: networkx", time.time() - start_time
print avg_clustering_lcc_nx

















# rxnEdges('ecosystem', 'YNP', 3)
# subEdges('ecosystem', 'YNP', 3)
