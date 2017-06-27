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
G = ig.Graph.TupleList(directed = False, edges = se)
## largest component
cl = G.clusters()
lcc = cl.giant()
## average shortest length
ave_spl_lcc = lcc.average_path_length(directed=False, unconn=True)
## average clustering coefficient
ave_cc_lcc = lcc.transitivity_undirected()
print ave_cc_lcc
list_local_cc_lcc = lcc.transitivity_local_undirected(mode='zero')
ave_cc_lcc_from_local = np.mean(list_local_cc_lcc)
print ave_cc_lcc_from_local




















# rxnEdges('ecosystem', 'YNP', 3)
# subEdges('ecosystem', 'YNP', 3)
