import sys
import os
import mgmnet.bio_nets as bn
import mgmnet.topo_measure as tm


bio = bn.bio()

# # level
# level = bio.level[sys.argv[1]]
# # group
# group = bio.group[sys.argv[2]]
# # species
# species = int(sys.argv[3])

# list_systems = ['ecosystem_YNP',\
#             'ecosystem_JGI',\
#             'individual_archaea_parsed',\
#             'individual_archaea',\
#             'individual_bacteria_parsed',\
#             'individual_bacteria']

list_systems = ['individual_archaea_parsed',\
            'individual_archaea',\
            'individual_bacteria_parsed',\
            'individual_bacteria']

for system_name in list_systems:
    dr = ''
    for ds in ('../results_cluster', '/deg_dist', '/%s'%(system_name)):
        dr = dr + ds
        if not os.path.exists(dr):
            os.makedirs(dr)

    for species in range(1, bio.number_of_species[system_name] + 1):
        sEdges = bio.sub_edges(system_name, species)
        if len(sEdges) > 0:
            dd_file_name = dr + '/deg_dist_lcc_%s-%d.csv'%(system_name, species)
            tm.degree_histogram(sEdges, dd_file_name)
