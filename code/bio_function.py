import sys
import os
import numpy as np
import csv



def evol_func(drf, group, run):
    import mgmnet.bio_nets as bn
    bio = bn.bioSys()

    dre = drf + '/evol_func'
    if not os.path.exists(dre):
        os.makedirs(dre)

    system_name = 'individual_%s'%(group)
    genome_list = list(range(1, bio.number_of_species[system_name] + 1))
    genome_list = np.random.permutation(genome_list)

    ec_file_name = dre + '/evol_nbr_ec_%s-%d.dat'%(group, run)
    ec_file = open(ec_file_name, 'w')
    ec_set = set()
    index = 1
    ec_array = bio.load_array_ec(system_name)
    for species in genome_list:
        ec_list = ec_array[species]
        ec_set = ec_set.union(set(ec_list))
        ec_file.write('%d\t%d\n'%(index, len(ec_set)))
        index += 1
    ec_file.close()

    rxn_file_name = dre + '/evol_nbr_rxn_%s-%d.dat'%(group, run)
    rxn_file = open(rxn_file_name, 'w')
    rxn_set = set()
    index = 1
    for species in genome_list:
        rxn_list = bio.load_list_rxn(system_name, species)
        rxn_set = rxn_set.union(set(rxn_list))
        rxn_set.union(set(rxn_list))
        rxn_file.write('%d\t%d\n'%(index, len(rxn_set)))
        index += 1
    rxn_file.close()


def dist_func():
    import mgmnet.bio_nets as bn
    bio = bn.bioSys()

    drs = drf + '/dist_func'
    if not os.path.exists(dre):
        os.makedirs(dre)

    system_name = '%s_%s'%(level, group)
    genome_list = list(range(1, bio.number_of_species[system_name] + 1))


    ec_file_name = drs + '/ec_%s-%d.dat'%(group, run)
    ec_file = open(ec_file_name, 'w')

    ec_set = set()
    index = 1
    ec_array = bio.load_array_ec(system_name)
    for species in genome_list:
        ec_list = ec_array[species]
        ec_set = ec_set.union(set(ec_list))
        ec_file.write('%d\t%d\n'%(index, len(ec_set)))
        index += 1
    ec_file.close()

    rxn_file_name = drr + '/rxn_%s-%d.dat'%(group, run)
    rxn_file = open(rxn_file_name, 'w')
    rxn_set = set()
    index = 1
    for species in genome_list:
        rxn_list = bio.load_list_rxn(system_name, species)
        rxn_set = rxn_set.union(set(rxn_list))
        rxn_set.union(set(rxn_list))
        rxn_file.write('%d\t%d\n'%(index, len(rxn_set)))
        index += 1
    rxn_file.close()

#####################################################################

analysis = sys.argv[1]

dr = '../results'
if not os.path.exists(dr):
    os.makedirs(dr)
drf = dr + '/bio_function'
if not os.path.exists(drf):
    os.makedirs(drf)

if analysis == 'evol':
    group = sys.argv[2]
    run = int(sys.argv[3])
    evol_func(drf, group, run)
if analysis == 'dist':
    dist_func(drf)
