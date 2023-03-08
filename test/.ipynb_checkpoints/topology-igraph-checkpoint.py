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
G = ig.Graph.TupleList(directed=False, edges=se)
## largest component
cl = G.clusters()
lcc = cl.giant()
## average shortest length
ave_spl_lcc = lcc.average_path_length(directed=False, unconn=True)
## average clustering coefficient
ave_cc_lcc = lcc.transitivity_undirected()
print(ave_cc_lcc)

start_time = time.time()
list_local_cc_lcc = lcc.transitivity_local_undirected(mode='nand')
ave_cc_lcc_from_local = np.mean(list_local_cc_lcc)
print("time for clustering coefficient: igraph ", time.time() - start_time)
print(ave_cc_lcc_from_local)

g_nx = nx.Graph()
g_nx.add_edges_from(se)
g_lcc_nx =  max(nx.connected_component_subgraphs(g_nx), key=len)

start_time = time.time()
cluster_list = nx.clustering(g_lcc_nx)
avg_clustering_lcc_nx = np.mean(cluster_list.values())
print("time for clustering coefficient: networkx", time.time() - start_time)
print(avg_clustering_lcc_nx)

