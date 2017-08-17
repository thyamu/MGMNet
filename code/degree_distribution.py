import sys
import os
import csv
import networkx as nx
import numpy as np
import collections
import mgmnet.bio_nets as bn


def write_histogram(file_name, list_a):
    dict_a = collections.Counter(list_a)
    max_list = max(dict_a.keys())
    with open(file_name, 'w') as f:
        csvf = csv.writer(f)
        for i in range(max_list + 1):
            freq = 0
            if i in dict_a.keys():
                freq = dict_a[i]
            csvf.writerow((i, freq))

# file_name = 'test-histo.dat'
# list_a = [0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 5]
# write_histogram(file_name, list_a)

bio = bn.bio()

# level
level = bio.level[sys.argv[1]]
# group
group = bio.group[sys.argv[2]]
# species
species = int(sys.argv[3])

system_name = '%s_%s'%(level, group)

sEdges = bio.sub_edges(system_name, species)

dd_file_name = 'test_degree_distribution_%s-%d'%(system_name, species)

G = nx.Graph(sEdges)

# nbr_edges
nbr_edges = G.number_of_edges()

if nbr_edges > 0:
    # nbr_connected_components (with G_lcc)
    if nx.is_connected(G):
        nbr_connected_components = 1
        G_lcc = G
    else:
        nbr_connected_components = nx.number_connected_components(G)
        G_lcc = max(nx.connected_component_subgraphs(G), key=len)

    # degree_lcc
    list_degree_lcc = G_lcc.degree().values()
    write_histogram(dd_file_name, list_degree_lcc)
