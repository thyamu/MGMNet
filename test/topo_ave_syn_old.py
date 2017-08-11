import sys
import os
import csv
import mgmnet.syn_nets as sn
import mgmnet.topo_measure as tm

syn = sn.synEco()
topo = tm.topoMeasure()

# level
level = syn.level
# group
group_dict = {} # ex. syn_a ==> synthetic nets of archaea genomes
group_name = ''
for i in range(3, 6):
    group = syn.group[sys.argv[i]]
    group_dict[group] = float(sys.argv[i+3])
    group_name = group_name + sys.argv[i]
print group_name

#----- To genereate list_genome -----#
genome_dict = syn.combine_set_genome(group_dict, comSize, comSet)
#print genome_dict

# species
comSize = int(sys.argv[1])
comSet = int(sys.argv[2])
species = 'size%d_set%d'%(comSize, comSet)
system_name = '%s_%s'%(level, group_name)

dr = ''
for ds in ('../results_test','/%s'%(system_name)):
    dr = dr + ds
    if not os.path.exists(dr):
        os.makedirs(dr)

outputFileName = dr + '/%s-%s.csv'%(system_name, species)

header = topo.header
with open(outputFileName, 'w') as f:
    if os.stat(outputFileName).st_size == 0: # if file not yet written
        csvf = csv.writer(f)
        csvf.writerow(header)

# species_name
species_name = group_name + '_' + species

# # nbr_ec
# ec_set = syn.combine_set_ec(genome_dict)
# nbr_ec = len(ec_set) ; print nbr_ec
# # nbr_rxn
# rxn_set = syn.combined_set_rxn(genome_dict)
# nbr_rxn = len(rxn_set) ; print nbr_rxn
#
# # EC 1.9.3.1 presence
# enz = '1.9.3.1'
# ec_presence = syn.combined_enz_presence(ec_set, enz)
#
# data0 = [level, group_name, species, species_name, nbr_ec, nbr_rxn, ec_presence]
#
# #----- To import sub-netwroks with rxn-degree for node attributes -----#
# sEdges = syn.combined_sub_edges(genome_dict)
# nodeAttr = syn.combined_rxn_degree(genome_dict)
#
# #--- To Compute ---#
# data1 = topo.global_measure(sEdges, nodeAttr)
# data = data0 + data1
#
# with open(outputFileName, 'a') as f:
#     csvf = csv.writer(f)
#     csvf.writerow(data)
