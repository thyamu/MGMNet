### To generate graphs in gexf format for visulation ###
#0. biosphere with 1, 2 and 3 embeded
#1. archaeasphere
#2. bacteriasphere
#3. eukaryasphere

### Attributes to add
# 0. degree (default)
# 1. domain


import os
import mgmnet.bio_nets as bn
import mgmnet.union_nets as un
import mgmnet.kegg_nets as kn
import networkx as nx

bio = bn.bio()

# 1. archaeasphere
# 2. bacteriasphere
# 3. eukaryasphere
# 4. ecosphere
### list of rxns from union networks
### (1) separate nets for 1, 2, 3 and 4
### (2) merged net of 1, 2, and 3
### (3) add informtion of net 1, 2 and 3 to the merged net in (2)



#-------- BEGIN: Sphere of archaea, bacteria, and eukarya and Total Ecosystem --------#
G = {}
union = un.union()
for system_name in union.number_of_species.iterkeys():
    species = union.number_of_species[system_name]
    sEdges = union.sub_edges(system_name, species)
    file_name = '../viz/sub_net_%s.gexf'%(system_name)
    G[system_name] = nx.Graph(sEdges)
    nx.write_gexf(G[system_name], file_name)
#-------- END: Sphere of archaea, bacteria, and eukarya and Total Ecosystem --------#



#-------- BEGIN: a  network for all domain including archaea, bacteria, and eukarya as a network attribute --------#
list_domain = ['union_individual_archaea', \
            'union_individual_bacteria', \
            'union_individual_eukarya']

G_all = G['union_individual_all']
for i, j in G_all.edges_iter():
    edge_weight = 1
    for system_name in list_domain:
        if (i, j) in G[system_name]:
            edge_weight += 0.1
    G_all.add_edge(i, j, weight=edge_weight)

list_node_weight = {'union_individual_archaea': 1, 'union_individual_bacteria': 10, 'union_individual_eukarya': 100}

for n in G_all.nodes_iter():
    node_weight = 0
    for system_name in list_domain:
        if n in G[system_name]:
            node_weight += list_node_weight[system_name]
    G_all.add_node(n, weight=node_weight)

file_name = '../viz/sub_net_weighted_all_domain.gexf'
nx.write_gexf(G_all, file_name)
#-------- END: a network for all domain including archaea, bacteria, and eukarya as a network attribute --------#



#-------- BEGIN: small kegg network including archaea, bacteria, and eukarya as a network attribute --------#
bio = bn.bio()
sEdges = bio.sub_edges('biosphere_kegg', 2)
G_kegg = nx.Graph(sEdges)

for n in G_kegg.nodes_iter():
    if n in G_all.nodes():
        nw = G_all.node[n]['weight']
        G_kegg.add_node(n, weight=nw)
    else:
        G_kegg.add_node(n, weight=0)

for i, j in G_kegg.edges_iter():
    if (i, j) in G_all.edges():
        ew = G_all[i][j]['weight']
        G_kegg.add_edge(i, j, weight=ew)
    else:
        G_kegg.add_edge(i, j, weight=0.9)

file_name = '../viz/sub_net_kegg_weighted_all_domain.gexf'
nx.write_gexf(G_kegg, file_name)
#-------- END: small kegg network including archaea, bacteria, and eukarya as a network attribute --------#



#-------- BEGIN: small kegg network including archaea, bacteria, eukarya, and ecosystem as a network attribute --------#
#-------- END: small kegg network including archaea, bacteria, eukarya, and ecosystem as a network attribute --------#




# #-------- BEGIN: big kegg network including archaea, bacteria, eukarya, ecosystem and small kegg as a network attribute --------#
# sEdges = bio.sub_edges('biosphere_kegg', 1)
# G_kegg = nx.Graph(sEdges)
#
# for n in G_kegg.nodes_iter():
#     if n in G_all.nodes():
#         nw = G_all.node[n]['weight']
#         G_kegg.add_node(n, weight=nw)
#     else:
#         G_kegg.add_node(n, weight=0)
#
# for i, j in G_kegg.edges_iter():
#     if (i, j) in G_all.edges():
#         ew = G_all[i][j]['weight']
#         G_kegg.add_edge(i, j, weight=ew)
#     else:
#         G_kegg.add_edge(i, j, weight=0.1)
