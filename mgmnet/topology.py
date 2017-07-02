import os
import kegg as kg
import bio_nets as bn
import networkx as nx
import numpy as np
import csv


kegg = kg.Kegg()

BIOSYSTEMS = {'ecosystem_YNP':26, 'ecosystem_JGI':5587, \
        'individual_archaea':845, 'individual_bacteria':21637, \
        'individual_archaea-parsed':199, 'individual_bacteria-parsed':1153}

dir_results = '../results'
if not os.path.exists(dir_results):
    os.makedirs(dir_results)

#name_lists = ['ecosystem_YNP', 'ecosystem_JGI']
name_lists = ['individual_bacteria']


for system_name in name_lists:

    header = [ "level", "group", "species", "species_name", \
               "nbr_nodes", "nbr_edges", "nbr_connected_components", \
               "nbr_nodes_lcc", "nbr_edges_lcc", \
               "ave_degree_lcc", "std_degree_lcc", \
               "ave_degree_square_lcc", "std_degree_square_lcc", \
               "ave_clustering_coeff_lcc", "std_clustering_coeff_lcc", \
               "ave_shortest_path_length_lcc", "std_shortest_path_length_lcc", \
               "ave_betweenness_nodes_lcc", "std_betweenness_nodes_lcc", \
               "ave_betweenness_edges_lcc", "std_betweenness_edges_lcc", \
               "assortativity_lcc", "attribute_assortativity_lcc", \
               "diameter_lcc", "EC 1.9.3.1 presence"]

    outputFileName = dir_results + '/%s.csv'%(system_name)
    with open(outputFileName, 'w') as f:
        csvf = csv.writer(f)
        csvf.writerow(header)

    # level # group
    [level, group] = system_name.split('_')
    # EC 1.9.3.1
    dict_species_enzPresence = bn.enz_presence(system_name, BIOSYSTEMS[system_name], '1.9.3.1')


    for species in range(1, BIOSYSTEMS[system_name] + 1):
        if species > 1:
            continue
        # species # species_name
        rxn_list, species_name = bn.load_list_rxn(system_name, species)

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
        rEdges = bn.rxn_edges(rxn_list, kegg.rxn_reac, kegg.rxn_prod)
        rxnG = nx.DiGraph(rEdges)
        rxn_degree = rxnG.degree()
        for u in G_lcc.nodes_iter():
            G_lcc.node[u]['nbr_rxns'] = rxn_degree[u]
        attribute_assortativity_lcc = nx.attribute_assortativity_coefficient(G_lcc, 'nbr_rxns')

        # diameter_lcc
        diameter_lcc = max(list_shortest_path_length_lcc)

        # EC 1.9.3.1 presence
        ec_presence = dict_species_enzPresence[species]


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



        '''
        stime = time.time()

        etime = time.time()
        print nbr_nodes, "time node nbr from number_of_nodes()", etime - stime
        '''
