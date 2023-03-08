class topoMeasure:
    def __init__(self):
        self.header0 = ["level",\
                       "group", \
                       "species", \
                       "species_name", \
                       "nbr_rxn"]
        self.header1 = ["nbr_nodes",\
                       "nbr_edges", \
                       "nbr_connected_components", \
                       "nbr_nodes_lcc", \
                       "nbr_edges_lcc", \
                       "ave_degree_lcc", \
                       "std_degree_lcc", \
                       "ave_degree_square_lcc", \
                       "std_degree_square_lcc", \
                       "ave_clustering_coeff_lcc", \
                       "std_clustering_coeff_lcc", \
                       "ave_shortest_path_length_lcc", \
                       "std_shortest_path_length_lcc", \
                       "ave_betweenness_nodes_lcc",\
                       "std_betweenness_nodes_lcc", \
                       "ave_betweenness_edges_lcc", \
                       "std_betweenness_edges_lcc", \
                       "assortativity_lcc", \
                       "attribute_assortativity_lcc", \
                       "diameter_lcc"]
        self.header = self.header0 + self.header1

    def global_measure(self, sEdges, nodeAttr):

        import networkx as nx
        import numpy as np

        G = nx.Graph(sEdges)

        # nbr_nodes
        nbr_nodes = G.number_of_nodes()
        # nbr_edges
        nbr_edges = G.number_of_edges()

        data = [0] * len(self.header1) # if nbr_edges == 0, then data =[0, ... , 0]

        if nbr_edges > 0:
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
            for u in G_lcc.nodes_iter():
                G_lcc.node[u]['node_attr'] = nodeAttr[u]
            attribute_assortativity_lcc = nx.attribute_assortativity_coefficient(G_lcc, 'node_attr')

            # diameter_lcc
            diameter_lcc = max(list_shortest_path_length_lcc)

            data = [ nbr_nodes, nbr_edges, nbr_connected_components, \
                     nbr_nodes_lcc, nbr_edges_lcc, \
                     ave_degree_lcc, std_degree_lcc, \
                     ave_degree_square_lcc, std_degree_square_lcc, \
                     ave_clustering_coeff_lcc, std_clustering_coeff_lcc, \
                     ave_shortest_path_length_lcc, std_shortest_path_length_lcc, \
                     ave_betweenness_nodes_lcc, std_betweenness_nodes_lcc, \
                     ave_betweenness_edges_lcc, std_betweenness_edges_lcc, \
                     assortativity_lcc, attribute_assortativity_lcc, \
                     diameter_lcc]
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
