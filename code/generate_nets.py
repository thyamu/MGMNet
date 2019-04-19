import sys
import os
import mgmnet.bio_nets as bn
import mgmnet.union_nets as un
import mgmnet.syn_nets as sn
import mgmnet.kegg_nets as kn
import mgmnet.ranRxn_nets as rn
import mgmnet.topo_measure as tm
import networkx as nx
import pickle

module_name = sys.argv[1]
name = sys.argv[2] # put system name
s1 = int(sys.argv[3])
s2 = int(sys.argv[4])
module_dict = {'bio': bn.bio(), \
               'union': un.union(), \
               'syn': sn.syn(), \
               'ran': rn.ranRxn()}
class_name = module_dict[module_name]

#for system_name in class_name.number_of_species.iterkeys():
for system_name in [name]:
    print module_name, system_name

    dr_sub = ''
    for ds in ('../results', '/networks', '/%s'%(module_name), '/%s'%(system_name)):
        dr_sub = dr_sub + ds
        if not os.path.exists(dr_sub):
            os.makedirs(dr_sub)

    #for species in range(1, class_name.number_of_species[system_name] + 1):
    for species in range(s1, s2):
        print species
        sEdges = class_name.sub_edges(system_name, species)
        if len(sEdges) > 0:
            file_name = dr_sub + '/sub_sub_net_%s-%d'%(system_name, species)
        G = nx.Graph(sEdges)
        #with open(file_name, 'wb') as f:
        #    pickle.dump([G.nodes(data=True), G.edges(data=True)], f)
        nx.write_gpickle(G, file_name + ".gpickle")
