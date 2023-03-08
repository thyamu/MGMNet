import os
import numpy as np
import kegg as kg
import bionets as bn
import igraph as ig
import networkx as nx
import time

kegg = kg.Kegg()


#### igraph vs networkx ####


# igraph
rxn_list = bn.loadRxns('ecosystem', 'YNP', 3)
se = bn.subEdges(rxn_list, kegg.rxn_reac, kegg.rxn_prod)

## graph object
G = ig.Graph.TupleList(se)
## largest component
cl = G.clusters()
lcc = cl.giant()
## average shortest length
ave_spl_lcc = lcc.average_path_length(directed=False, unconn=True)

start_time = time.time()
list_local_cc_lcc = lcc.transitivity_local_undirected(mode='zero')
ave_cc_lcc_from_local = np.mean(list_local_cc_lcc)
print("time for clustering coefficient: igraph", time.time() - start_time)

#networkx
g_nx = nx.Graph(se)
g_lcc_nx =  max(nx.connected_component_subgraphs(g_nx), key=len)
start_time = time.time()
cluster_list = nx.clustering(g_lcc_nx)
avg_clustering_lcc_nx = np.mean(cluster_list.values())
print("time for clustering coefficient: networkx", time.time() - start_time)
