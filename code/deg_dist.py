import sys
import os
import mgmnet.bio_nets as bn
import mgmnet.union_nets as un
import mgmnet.syn_nets as sn
import mgmnet.ranRxn_nets as rn
import mgmnet.kegg_nets as kn
import mgmnet.topo_measure as tm
import networkx as nx

module_name = sys.argv[1]
module_dict = {'bio': bn.bio(), \
               'union': un.union(), \
               'syn': sn.syn(), \
               'ranRxn': rn.ranRxn()}
class_name = module_dict[module_name]

# level
level = class_name.level[sys.argv[2]]
# group
group = class_name.group[sys.argv[3]]
# species
species = int(sys.argv[4])

system_name = '%s_%s'%(level, group)

# for system_name in class_name.number_of_species.iterkeys():
dr_sub = ''
for ds in ('../results_cluster', '/deg_dist', '/%s'%(module_name), '/sub_degree', '/%s'%(system_name)):
    dr_sub = dr_sub + ds
    if not os.path.exists(dr_sub):
        os.makedirs(dr_sub)

sEdges = class_name.sub_edges(system_name, species)
if len(sEdges) > 0:
    ddsub_file_name = dr_sub + '/deg_dist_lcc_%s-%d.csv'%(system_name, species)
    tm.sub_degree_histogram_old(sEdges, ddsub_file_name)
