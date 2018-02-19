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
    (2) nbr nodes
    (3) nbr edges
    (4) nbr connected_components
    (5) nbr nodes_lcc
    (6) nbr edges_lcc
    (7) ave_degree_lcc, std_degree_lcc
    (8) ave_clustering_coeff_lcc
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
                        ##### (3) nbr edges
                        "nbr_edges",\
                        ##### (4) nbr connected_components
                       "nbr_connected_components", \
                       ##### (5) nbr nodes_lcc, sub, rxn
                       "nbr_nodes_lcc", \
                       ##### (6) nbr edges_lcc
                       "nbr_edges_lcc", \
                       ##### (7) ave_sub_degree_lcc
                       "ave_degree_lcc", \
                       "std_degree_lcc", \
                       ##### (8) ave_clustering_coeff_lcc
                       "ave_clustering_coeff_lcc", \
                       ##### (9) ave_shortest_path_length_lcc, \
                       "ave_shortest_path_length_lcc", \
                       ##### (10) ave_node_betweenness
                       "ave_betweenness_nodes_lcc", \
                       ##### (11) assortativity_lcc
                       "assortativity_lcc"]


        self.header = self.header0 + self.header1

    def simple_global_measure(self, sEdges):

        import networkx as nx
        import numpy as np

        '''Check sEdges networks'''
        G = nx.Graph(sEdges)

        # (2) nbr_nodes
        nbr_nodes = G.number_of_nodes()
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

            ##### (5) nbr nodes_lcc
            nbr_nodes_lcc = G_lcc.number_of_nodes()
            ##### (6) nbr edges_lcc
            nbr_edges_lcc = G_lcc.number_of_edges()

            ##### (7) ave_degree_lcc
            dict_degree_lcc = G_lcc.degree()
            list_degree_lcc =[dict_degree_lcc[n] for n in G_lcc.nodes()]
            ave_degree_lcc = np.mean(list_degree_lcc)
            std_degree_lcc = np.std(list_degree_lcc)

            ##### (8) ave_clustering_coeff_lcc
            ave_clustering_coeff_lcc = nx.average_clustering(G_lcc)

            ##### (9) ave_shortest_path_length_lcc
            ave_shortest_path_length_lcc = nx.average_shortest_path_length(G_lcc)

            ##### (10) ave_node_betweenness
            list_betweenness_nodes_lcc = nx.betweenness_centrality(G_lcc).values()
            ave_betweenness_nodes_lcc = np.mean(list_betweenness_nodes_lcc)

            ##### (11) assortativity_lcc
            assortativity_lcc = nx.degree_assortativity_coefficient(G_lcc)

            data = [ nbr_nodes,\
                     nbr_edges,\
                     nbr_connected_components,\
                     nbr_nodes_lcc, \
                     nbr_edges_lcc, \
                     ave_degree_lcc, std_degree_lcc, \
                     ave_clustering_coeff_lcc, \
                     ave_shortest_path_length_lcc, \
                     ave_betweenness_nodes_lcc, \
                     assortativity_lcc]

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
