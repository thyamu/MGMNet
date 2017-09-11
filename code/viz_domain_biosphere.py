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

G = {}
union = un.union()
for system_name in union.number_of_species.iterkeys():
    species = union.number_of_species[system_name]
    sEdges = union.sub_edges(system_name, species)
    file_name = '../viz/sub_net_%s.gexf'%(system_name)
    G[system_name] = nx.Graph(sEdges)
    nx.write_gexf(G[system_name], file_name)

list_domain = ['union_individual_archaea', \
            'union_individual_bacteria', \
            'union_individual_eukarya']

G_all = G['union_individual_all']
for i, j in G_all.edges_iter():
    edge_weight = 1
    for system_name in list_domain:
        if (i, j) in G[system_name]:
            edge_weight += 1
    G_all.add_edge(i, j, weight=edge_weight)

for n in G_all.nodes_iter():
    node_weight = 1
    for s in range(1, len(list_domain) + 1):
        system_name = list_domain[s-1]
        if n in G[system_name]:
            node_weight += s
    G_all.add_node(n, weight=node_weight)

file_name = '../viz/sub_net_weighted_all_domain.gexf'
nx.write_gexf(G_all, file_name)
