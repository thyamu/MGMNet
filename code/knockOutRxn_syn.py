import sys
import os
import mgmnet.syn_nets as sn
import numpy as np

syn = sn.syn()

# level
level = syn.level[sys.argv[1]]
# group
group = syn.group[sys.argv[2]]
# species
species = int(sys.argv[3])

system_name = '%s_%s'%(level, group)

dr = ''
for ds in ('../data', '/syn', '/knock_out_rxn_list', '/%s'%(system_name)):
    dr = dr + ds
    if not os.path.exists(dr):
        os.makedirs(dr)

output5 = dr + '/rxn0.95_%s-%d.dat'%(system_name, species)
output10 = dr + '/rxn0.9_%s-%d.dat'%(system_name, species)

rxn_list = syn.load_list_rxn(system_name, species)

nbr_removal_10 = len(rxn_list) / 10
nbr_removal_5 = nbr_removal_10 / 2

removal_list10 = np.random.choice(rxn_list, nbr_removal_10, replace=False)
removal_list5 = removal_list10[:nbr_removal_5]

# print len(rxn_list)
# print len(removal_list5)
# print len(removal_list10)

output5_file = open(output5, 'w')
output10_file = open(output10, 'w')


output10_file.write('# 0.9rxn-%s-%d'%(system_name, species))
for i in range(len(rxn_list)):
    if rxn_list[i] in removal_list10:
        continue
    output10_file.write('\n%s'%(rxn_list[i]))


output5_file.write('# 0.95rxn-%s-%d'%(system_name, species))
for i in range(len(rxn_list)):
    if rxn_list[i] in removal_list5:
        continue
    output5_file.write('\n%s'%(rxn_list[i]))
