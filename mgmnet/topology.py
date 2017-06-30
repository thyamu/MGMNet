import os
import kegg as kg
import bio_nets as bn
import networkx as nx
import numpy as np
import time


kegg = kg.Kegg()

BIOSYSTEMS = {'ecosystem_YNP':26, 'ecosystem_JGI':5587, \
        'individual_archaea':845, 'individual_bacteria':21637, \
        'individual_archaea_parsed':199, 'individual_bacteria_parsed':1153}

dir_results = '../results'
if not os.path.exists(dir_results):
    os.makedirs(dir_results)

name_lists = ['ecosystem_YNP']
for name in name_lists:

    outputFileName = dir_results + '/%s.dat'%(name)
    outputFile = open(outputFileName, 'w')
    header = [ "level", "group", "species", "species_name", \
               "nbr_nodes", "nbr_edges", "nbr_connected_components", \
               "nbr_nodes_lcc", "nbr_edges_lcc", \
               "ave_degree_lcc", "std_degree_lcc", \
               "ave_degree^2_lcc", "std_degree^2_lcc", \
               "ave_clustering_coeff_lcc", "std_clustering_coeff_lcc", \
               "ave_shortest_path_length_lcc", "std_shortest_path_length_lcc", \
               "ave_betweeness_nodes_lcc", "std_betweeness_nodes_lcc", \
               "ave_betweeness_edges_lcc", "std_betweeness_edges_lcc", \
               "assortativity_lcc", "attribute_assortativity_lcc", \
               "diameter_lcc", "EC 1.9.3.1 presence"]

    '''
               "ave_shortest_path_length_lcc", "std_shortest_path_length_lcc", \
               "ave_betweeness_nodes_lcc", "std_betweeness_nodes_lcc", \
               "ave_betweeness_edges_lcc", "std_betweeness_edges_lcc", \
               "assortativity_lcc", "attribute_assortativity_lcc", \
               "diameter_lcc", "EC 1.9.3.1 presence"
    '''
    for h in header:
        outputFile.write('%s\t'%(h))

    # level # group
    [level, group] = name.split('_')

    for species in range(BIOSYSTEMS[name]):
        # species
        inputFileName = '../data/rxn_lists/%s/%d.dat'%(name, species+1)
        # species_name
        rxn_list, species_name = bn.load_list_rxn_from_files(inputFileName)

        #--- Import sub-netwroks ---#
        sEdges = bn.sub_edges(rxn_list, kegg.rxn_reac, kegg.rxn_prod)
        G = nx.Graph(sEdges)

        # nbr_nodes
        nbr_nodes = G.number_of_nodes()
        # nbr_edges
        nbr_edges = G.number_of_edges()

        # nbr_connected_components (with G_lcc)
        if nx.is_connected(G):
            nbr_connected_components = 1
            G_lcc = G
        else:
            nbr_connected_components = nx.number_connected_components(G)
            G_lcc = max(nx.connected_component_subgraphs(G), key=len)

        # nbr_nodes_lcc
        nbr_nodes_lcc = G_lcc.number_of_nodes()
        # nbr_edges_lcc
        nbr_edges_lcc = G_lcc.number_of_edges()

        # ave_degree_lcc # std_degree_lcc
        list_degree_lcc = G_lcc.degree().values()
        ave_degree_lcc = np.mean(list_degree_lcc)
        std_degree_lcc = np.std(list_degree_lcc)

        # ave_degree^2_lcc # std_degree^2_lcc
        list_degree_square_lcc = [d^2 for d in list_degree_lcc]
        ave_degree_square_lcc = np.mean(list_degree_square_lcc)
        std_degree_square_lcc = np.std(list_degree_square_lcc)

        # ave_clustering_coeff_lcc # std_clustering_coeff_lcc
        list_clustering_coeff_lcc = nx.clustering(G_lcc).values()
        ave_clustering_coeff_lcc = np.mean(list_clustering_coeff_lcc)
        std_clustering_coeff_lcc = np.mean(list_clustering_coeff_lcc)







        '''
        stime = time.time()

        etime = time.time()
        print nbr_nodes, "time node nbr from number_of_nodes()", etime - stime
        '''


        rEdges = bn.rxn_edges(rxn_list, kegg.rxn_reac, kegg.rxn_prod)
        rxnG = nx.DiGraph(rEdges)

        data = [level, group, species, species_name]
        outputFile.write('\n')
        for d in data:
            outputFile.write('%s\t'%(d))

    outputFile.close()
