'''
Main text
    (0) Number of reactions == > Check if this is same as the number of rxn_nodes
    (0) average shortest_path_length
    (0) average clustering coefficient
    (x) attribute assortitivity ==> attribute assortativity

In supplement
    (0) Number of edges,
    (x) Number of ECs
    (x) Average edge_betweenness_centrality
    (x) Average node_betweenness_centrality
    (0) assortivitiy == > compare this matches the attribute assotitivity
    (0) average degree


===> NEW calculation
    (1) nbr rxns
    (2) nbr nodes, sub, rxn
    (3) nbr edges
    (4) nbr connected_components
    (5) nbr nodes_lcc, sub, rxn
    (6) nbr edges_lcc
    (7) ave_sub_degree_lcc
    (8) ave_rxn_degree_lcc
    (9) ave_sub_clustering_coeff_lcc
    (10) ave_sub_shortest_path_length_lcc
 '''

class topoMeasure:
    def __init__(self):
        self.header0 = ["level",\
                       "group", \
                       "species", \
                       "species_name", \
                       ##### (1) nbr rxns
                       "nbr_rxn"]

        self.header1 = [#### (2) nbr nodes, sub, rxn
                        "nbr_nodes",\
                        "nbr_sub_nodes",\
                        "nbr_rxn_nodes",\
                        ##### (3) nbr edges
                        "nbr_edges",\
                        ##### (4) nbr connected_components
                       "nbr_connected_components", \
                       ##### (5) nbr nodes_lcc, sub, rxn
                       "nbr_nodes_lcc", \
                       "nbr_sub_nodes_lcc", \
                       "nbr_rxn_nodes_lcc", \
                       ##### (6) nbr edges_lcc
                       "nbr_edges_lcc", \
                       ##### (7) ave_sub_degree_lcc
                       "ave_sub_degree_lcc", \
                       "std_sub_degree_lcc", \
                       ##### (8) ave_rxn_degree_lcc
                       "ave_rxn_degree_lcc", \
                       "std_rxn_degree_lcc", \
                       ##### (9-1) ave_clustering_coeff_lcc (default)
                       "ave_clustering_coeff_lcc", \
                       ##### (9-2) ave_clustering_coeff_lcc_min (mode='min')
                       "ave_clustering_coeff_lcc_min", \
                       ##### (9-3) ave_clustering_coeff_lcc_max (mode='max')
                       "ave_clustering_coeff_lcc_max"] #, \
                       ##### (10) ave_shortest_path_length_lcc, \
                       ##### (11) ave_node_betweenness]




        self.header = self.header0 + self.header1

    def bipartite_global_measure(self, rEdges):

        import networkx as nx
        from networkx.algorithms import bipartite
        import numpy as np

        '''Check rEdges networks'''
        G = nx.Graph(rEdges)

        '''Divide the set of nodes into sub and rxn group
        ==> group(bipartite=1), group(bipartitie=0) = bipartite.sets(G)
        '''

        # (2) nbr_nodes
        nbr_nodes = G.number_of_nodes()
        nbr_sub_nodes = 0
        for n in G.nodes():
            if n[0] == 'C':
                nbr_sub_nodes += 1
        nbr_rxn_nodes = nbr_nodes - nbr_sub_nodes

        # (3) nbr_edges
        nbr_edges = G.number_of_edges()


        data = [0] * len(self.header1) # if nbr_edges == 0, then data =[0, ... , 0]

        if nbr_edges > 0:
            ##### (4) nbr connected_components (with G_lcc)
            if nx.is_connected(G):
                nbr_connected_components = 1
                G_lcc = G
            else:
                nbr_connected_components = nx.number_connected_components(G)
                G_lcc = max(nx.connected_component_subgraphs(G), key=len)

            for n in G_lcc.nodes():
                if n[0] == 'C':
                    G_lcc.add_node(n, bipartite=1)
                if n[0] == 'R':
                    G_lcc.add_node(n, bipartite=0)

            sub_group_lcc = [n for n in G_lcc.nodes if G_lcc.nodes[n]['bipartite']==1]
            rxn_group_lcc = list(set(G_lcc) - set(sub_group_lcc))

            ##### (5) nbr nodes_lcc, sub, rxn
            nbr_nodes_lcc = G_lcc.number_of_nodes()
            nbr_sub_nodes_lcc = len(sub_group_lcc)
            nbr_rxn_nodes_lcc = len(rxn_group_lcc)

            ##### (6) nbr edges_lcc
            nbr_edges_lcc = G_lcc.number_of_edges()

            ##### (7) ave_sub_degree_lcc
            dict_degree_lcc = G_lcc.degree()
            list_sub_degree_lcc = [dict_degree_lcc[n] for n in sub_group_lcc]
            ave_sub_degree_lcc = np.mean(list_sub_degree_lcc)
            std_sub_degree_lcc = np.std(list_sub_degree_lcc)

            ##### (8) ave_rxn_degree_lcc
            list_rxn_degree_lcc = [dict_degree_lcc[n] for n in rxn_group_lcc]
            ave_rxn_degree_lcc = np.mean(list_rxn_degree_lcc)
            std_rxn_degree_lcc = np.std(list_rxn_degree_lcc)

            ##### (9-1) ave_clustering_coeff_lcc
            ave_clustering_coeff_lcc = bipartite.average_clustering(G_lcc)

            ##### (9-2) ave_clustering_coeff_lcc_min (mode='min')
            ave_clustering_coeff_lcc_min = bipartite.average_clustering(G_lcc, mode='min')

            ##### (9-3) ave_clustering_coeff_lcc_max (mode='max')
            ave_clustering_coeff_lcc_max = bipartite.average_clustering(G_lcc, mode='max')


            # ##### (10) ave_shortest_path_length_lcc
            # ave_shortest_path_length_lcc = nx.average_shortest_path_length(G_lcc)
            #
            # ##### (11) ave_node_betweenness
            # list_betweenness_nodes_lcc = nx.betweenness_centrality(G_lcc).values()
            # ave_betweenness_nodes_lcc = np.mean(list_betweenness_nodes_lcc)




            data = [ nbr_nodes, nbr_sub_nodes, nbr_rxn_nodes,\
                     nbr_edges,\
                     nbr_connected_components,\
                     nbr_nodes_lcc, nbr_sub_nodes_lcc, nbr_rxn_nodes_lcc,\
                     nbr_edges_lcc, \
                     ave_sub_degree_lcc, std_sub_degree_lcc, \
                     ave_rxn_degree_lcc, std_rxn_degree_lcc, \
                     ave_clustering_coeff_lcc, \
                     ave_clustering_coeff_lcc_min, \
                     ave_clustering_coeff_lcc_max ]
        return data

def sub_degree_histogram_old(sEdges, file_name):
    import networkx as nx
    import collections
    import csv
    G = nx.Graph(sEdges)
    # nbr_connected_components (with G_lcc)
    if nx.is_connected(G):
        nbr_connected_components = 1
        G_lcc = G
    else:
        nbr_connected_components = nx.number_connected_components(G)
        G_lcc = max(nx.connected_component_subgraphs(G), key=len)
    # degree_lcc
    list_degree_lcc = G_lcc.degree().values()
    dict_a = collections.Counter(list_degree_lcc)
    max_list = max(dict_a.keys())
    with open(file_name, 'w') as f:
        csvf = csv.writer(f)
        csvf.writerow(("degree","frequency"))
        for i in range(1, max_list + 1):
            freq = 0
            if i in dict_a.keys():
                freq = dict_a[i]
            csvf.writerow((i, freq))

def degree_histogram(list_degree_lcc, file_name):
    #import networkx as nx
    import collections
    import csv
    dict_a = collections.Counter(list_degree_lcc)
    max_list = max(dict_a.keys())
    with open(file_name, 'w') as f:
        csvf = csv.writer(f)
        csvf.writerow(("degree","frequency"))
        for i in range(1, max_list + 1):
            freq = 0
            if i in dict_a.keys():
                freq = dict_a[i]
            csvf.writerow((i, freq))
