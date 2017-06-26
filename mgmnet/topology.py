import os
import numpy as np
import kegg as kg
import bionets as bn
import igraph as ig

import time


start_time = time.time() # remove it
kegg = kg.Kegg()
print "time to load kegg"
print time.time() - start_time

start_time = time.time() # remove it
rxn_list = bn.loadRxns('ecosystem', 'YNP', 3)
print "time to load rxn info"
print time.time() - start_time

start_time = time.time() # remove it
se = bn.subEdges(rxn_list, kegg.rxn_reac, kegg.rxn_prod)
print "time to generate edge list"
print time.time() - start_time

start_time = time.time() # remove it
G = ig.Graph.TupleList(directed = False, edges = se)
print "time to load edge to network object"
print time.time() - start_time

start_time = time.time() # remove it
cl = G.clusters()
lcc = cl.giant()
print 'Time for largest connected component', time.time() - start_time
print lcc.vcount()


start_time = time.time()
ave_spl_lcc = lcc.average_path_length(directed=False, unconn=True)
print 'Time for ave_shortest_length', time.time() - start_time
print "ave_spl_lcc = ", ave_spl_lcc

start_time = time.time()
ave_cc_lcc = lcc.transitivity_undirected()
print 'Time for ave_clustering_coefficient', time.time() - start_time
print "ave_cc_lcc = ", ave_cc_lcc

start_time = time.time()
list_local_cc_lcc = lcc.transitivity_local_undirected(mode='zero')
# print 'Time for list of local_clustering_coefficient', time.time() - start_time
# print list_local_cc_lcc
#
# start_time = time.time()
# list_local_computed_cc_lcc = []
# #print list_local_cc_lcc
# for n in list_local_cc_lcc:
#     if str(n) != 'nan':
#         list_local_computed_cc_lcc.append(n)
# print "length", len(list_local_computed_cc_lcc)




ave_cc_lcc_from_local = np.mean(list_local_cc_lcc)
print 'Time for ave_clustering_coefficient by computing the mean of list of local cc', time.time() - start_time
print "ave_cc_lcc from local = ", ave_cc_lcc_from_local

















# rxnEdges('ecosystem', 'YNP', 3)
# subEdges('ecosystem', 'YNP', 3)
