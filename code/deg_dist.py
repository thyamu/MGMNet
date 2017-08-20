import sys
import os
import mgmnet.bio_nets as bn
import mgmnet.union_nets as un
import mgmnet.syn_nets as sn
import mgmnet.kegg_nets as kn
import mgmnet.topo_measure as tm
import networkx as nx

module_name = sys.argv[1]
module_dict = {'bio': bn.bio, \
               'union': un.union, \
               'syn': sn.synthetic}
class_name = module_dict[module_name]()

for system_name in class_name.number_of_species.iterkeys():
#for system_name in ['union_individual_archaea']:
    print system_name
    dr_sub = ''
    for ds in ('../results_cluster', '/deg_dist', '/%s'%(module_name), '/sub_degree', '/%s'%(system_name)):
        dr_sub = dr_sub + ds
        if not os.path.exists(dr_sub):
            os.makedirs(dr_sub)
    for species in range(1, class_name.number_of_species[system_name] + 1):
        sEdges = class_name.sub_edges(system_name, species)
        if len(sEdges) > 0:
            ddsub_file_name = dr_sub + '/deg_dist_lcc_%s-%d.csv'%(system_name, species)
            tm.sub_degree_histogram_old(sEdges, ddsub_file_name)
