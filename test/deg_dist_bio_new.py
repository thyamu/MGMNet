import sys
import os
import mgmnet.bio_nets as bn
import mgmnet.topo_measure as tm
import networkx as nx



bio = bn.bio()

# list_systems = ['ecosystem_YNP',\
#             'ecosystem_JGI',\
#             'individual_archaea_parsed',\
#             'individual_archaea',\
#             'individual_bacteria_parsed',\
#             'individual_bacteria']

list_systems = ['ecosystem_YNP']

for system_name in list_systems:

    dr_sub = ''
    for ds in ('../results_test', '/deg_dist', '/sub_degree', '/%s'%(system_name)):
        dr_sub = dr_sub + ds
        if not os.path.exists(dr_sub):
            os.makedirs(dr_sub)

    dr_rxn = ''
    for ds in ('../results_test', '/deg_dist', '/rxn_degree', '/%s'%(system_name)):
        dr_rxn = dr_rxn + ds
        if not os.path.exists(dr_rxn):
            os.makedirs(dr_rxn)

    for species in range(1, 2):#bio.number_of_species[system_name] + 1):
        #sEdges = bio.sub_edges(system_name, species)
        dict_rxn_degree = bio.rxn_degree(system_name, species)
        rEdges = bio.rxn_edges(system_name, species)
        G = nx.DiGraph(rEdges)
        net_degrees = G.degree()
        rxn_degree_graph = {}
        for n in G.nodes_iter():
            if n[0] == 'C':
                rxn_degree_graph[n] = net_degrees[n]
                if rxn_degree_graph[n] != dict_rxn_degree[n]:
                    print n, rxn_degree_graph[n], dict_rxn_degree[n]
                    print "error"

        sEdges = bio.sub_edges(system_name, species)
        sG = nx.Graph(sEdges)

        sub_net_degrees = sG.degree()
        # print sub_net_degrees['C00002']
        # print sub_net_degrees['C15854']
        # print net_degrees['C15854']
        print sG.neighbors('C15854')
        print G.neighbors('C15854'), G.predecessors('C15854')
        print G.neighbors('R07478')
        print G.neighbors('R07480')
        print G.neighbors('R07479')


        # if len(sEdges) > 0:
        #     G = nx.Graph(sEdges)
        #     if nx.is_connected(G):
        #         nbr_connected_components = 1
        #         G_lcc = G
        #     else:
        #         nbr_connected_components = nx.number_connected_components(G)
        #         G_lcc = max(nx.connected_component_subgraphs(G), key=len)
        #
        #     list_sub_degree_lcc = G_lcc.degree().values()
        #     ddsub_file_name = dr_sub + '/deg_dist_lcc_%s-%d.csv'%(system_name, species)
        #     tm.degree_histogram(list_sub_degree_lcc, ddsub_file_name)
        #
        #     list_rxn_degree_lcc = [dict_rxn_degree[n] for n in G_lcc.nodes_iter()]
        #     ddrxn_file_name = dr_rxn + '/deg_dist_lcc_%s-%d.csv'%(system_name, species)
        #     tm.degree_histogram(list_rxn_degree_lcc, ddrxn_file_name)
