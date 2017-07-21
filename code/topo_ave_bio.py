import sys
import os
import networkx as nx
import numpy as np
import csv

import mgmnet.bio_nets as bn
import mgmnet.topo_measure as tm

bio = bn.bioSys()
topo = tm.topoMeasure()


dr = '../results_test'
if not os.path.exists(dr):
    os.makedirs(dr)

drs = dr + '/%s'%(system_name)
if not os.path.exists(drs):
    os.makedirs(drs)

outputFileName = drs + '/%s-%d.csv'%(system_name, species)


header = topo.header
data = topo.data

with open(outputFileName, 'w') as f:
    if os.stat(outputFileName).st_size == 0: # if file not yet written
        csvf = csv.writer(f)
        csvf.writerow(header)


# level
level = bio.level[sys.argv[1]]
# group
group = bio.group[sys.argv[2]]
# species
species = int(sys.argv[3])

system_name = '%s_%s'%(level, group)

species_name = bio.species_name(system_name, species)

#--- Import sub-netwroks ---#
sEdges = bio.sub_edges((system_name, species)
G = nx.Graph(sEdges)

# nbr_nodes
nbr_nodes = G.number_of_nodes()
# nbr_edges
nbr_edges = G.number_of_edges()


if nbr_edges > 0:
    # nbr_connected_components (with G_lcc)
    if nx.is_connected(G):
        nbr_connected_components = 1
        G_lcc = G
    else:
        nbr_connected_components = nx.number_connected_components(G)

    # nbr_nodes_lcc
    nbr_nodes_lcc = G_lcc.number_of_nodes()
    # nbr_edges_lcc
    nbr_edges_lcc = G_lcc.number_of_edges()

    # ave_degree_lcc # std_degree_lcc
    list_degree_lcc = G_lcc.degree().values()
    ave_degree_lcc = np.mean(list_degree_lcc)
    std_degree_lcc = np.std(list_degree_lcc)

    # ave_degree_square_lcc # std_degree_square_lcc
    list_degree_square_lcc = [d^2 for d in list_degree_lcc]
    ave_degree_square_lcc = np.mean(list_degree_square_lcc)
    std_degree_square_lcc = np.std(list_degree_square_lcc)

    # ave_clustering_coeff_lcc # std_clustering_coeff_lcc
    list_clustering_coeff_lcc = nx.clustering(G_lcc).values()
    ave_clustering_coeff_lcc = np.mean(list_clustering_coeff_lcc)
    std_clustering_coeff_lcc = np.std(list_clustering_coeff_lcc)

    # ave_shortest_path_length_lcc # std_shortest_path_length_lcc
    dict_shortest_path_length_lcc = nx.shortest_path_length(G_lcc)
    list_shortest_path_length_lcc = [dict_shortest_path_length_lcc[u][v] for u in G_lcc.nodes_iter() for v in G_lcc.nodes_iter()]
    ave_shortest_path_length_lcc = np.mean(list_shortest_path_length_lcc)
    std_shortest_path_length_lcc = np.std(list_shortest_path_length_lcc)

    # ave_betweenness_nodes_lcc # std_betweenness_nodes_lcc
    list_betweenness_nodes_lcc = nx.betweenness_centrality(G_lcc).values()
    ave_betweenness_nodes_lcc = np.mean(list_betweenness_nodes_lcc)
    std_betweenness_nodes_lcc = np.std(list_betweenness_nodes_lcc)

    # ave_betweenness_edges_lcc # std_betweenness_edges_lcc
    list_betweenness_edges_lcc = nx.edge_betweenness_centrality(G_lcc).values()
    ave_betweenness_edges_lcc = np.mean(list_betweenness_edges_lcc)
    std_betweenness_edges_lcc = np.std(list_betweenness_edges_lcc)

    # assortativity_lcc
    assortativity_lcc = nx.degree_assortativity_coefficient(G_lcc)

    # attribute_assortativity_lcc
    rxn_degree = bio.rxn_degree()
    for u in G_lcc.nodes_iter():
        G_lcc.node[u]['nbr_rxns'] = rxn_degree[u]
    attribute_assortativity_lcc = nx.attribute_assortativity_coefficient(G_lcc, 'nbr_rxns')

    # diameter_lcc
    diameter_lcc = max(list_shortest_path_length_lcc)

    # EC 1.9.3.1 presence
    enz = '1.9.3.1'
    ec_presence = bio.enz_presence(system_name, species, enz)

    data = [ level, group, species, species_name, \
               nbr_nodes, nbr_edges, nbr_connected_components, \
               nbr_nodes_lcc, nbr_edges_lcc, \
               ave_degree_lcc, std_degree_lcc, \
               ave_degree_square_lcc, std_degree_square_lcc, \
               ave_clustering_coeff_lcc, std_clustering_coeff_lcc, \
               ave_shortest_path_length_lcc, std_shortest_path_length_lcc, \
               ave_betweenness_nodes_lcc, std_betweenness_nodes_lcc, \
               ave_betweenness_edges_lcc, std_betweenness_edges_lcc, \
               assortativity_lcc, attribute_assortativity_lcc, \
               diameter_lcc, ec_presence]

with open(outputFileName, 'a') as f:
    csvf = csv.writer(f)
    csvf.writerow(data)
