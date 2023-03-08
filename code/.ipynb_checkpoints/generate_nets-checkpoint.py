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

module_name = sys.argv[1] #module name (see module_dict.keys())
name = sys.argv[2] #system name (eg. individual_archaea_parsed)
s1 = int(sys.argv[3]) #species number to begin
s2 = int(sys.argv[4]) #species number to end
t = sys.argv[5] #the type of networks (s for sub_sub; r for rxn_sub)
module_dict = {'bio': bn.bio(), \
               'union': un.union(), \
               'syn': sn.syn(), \
               'ran': rn.ranRxn()}
class_name = module_dict[module_name]

if t == "s":
    for system_name in [name]:
        dr_sub = ''
        for ds in ('../results', '/networks', '/%s'%(module_name), '/%s'%(system_name)):
            dr_sub = dr_sub + ds
            if not os.path.exists(dr_sub):
                os.makedirs(dr_sub)
        for species in range(s1, s2 + 1):
            sEdges = class_name.sub_edges(system_name, species)
            if len(sEdges) > 0:
                file_name = dr_sub + '/sub_sub_net_%s-%d'%(system_name, species)
            G = nx.Graph(sEdges)
            nx.write_gpickle(G, file_name + ".gpickle")

if t == "r":
    for system_name in [name]:
        dr_rxn = ''
        for ds in ('../results', '/rxn_networks', '/%s'%(module_name), '/%s'%(system_name)):
            dr_rxn = dr_rxn + ds
            if not os.path.exists(dr_rxn):
                os.makedirs(dr_rxn)
        for species in range(s1, s2 + 1):
            rEdges = class_name.rxn_edges(system_name, species)
            if len(rEdges) > 0:
                file_name = dr_rxn + '/rxn_sub_net_%s-%d'%(system_name, species)
            G = nx.Graph(rEdges)
            nx.write_gpickle(G, file_name + ".gpickle")
