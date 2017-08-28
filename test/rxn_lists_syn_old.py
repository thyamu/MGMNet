import os
import sys
import numpy as np


syn_type = sys.argv[1]
max_run = 10

number_of_species = {'individual_archaea':845, \
                    'individual_bacteria':21637, \
                    'individual_archaea_parsed':199, \
                    'individual_bacteria_parsed':1153,\
                    'individual_eukarya':77, \
                    'ecosystem_JGI':5587}

number_of_samples = {'individual_archaea':250, \
                        'individual_bacteria':300, \
                        'individual_archaea_parsed':150, \
                        'individual_bacteria_parsed':200,\
                        'individual_eukarya':77, \
                        'individual_all': 627,\
                        'individual_all_parsed': 427, \
                        'ecosystem_JGI': 500}

#----- syn of each individual system -----#
if syn_type == 'i':
    file_names = ['individual_archaea',\
                'individual_bacteria', \
                'individual_archaea_parsed', \
                'individual_bacteria_parsed',\
                'individual_eukarya', \
                'ecosystem_JGI']

    for system_name in file_names:

        dr = ''
        for ds in ('../data', '/syn', '/rxn_lists', '/%s'%(system_name)):
            dr = dr + ds
            if not os.path.exists(dr):
                os.makedirs(dr)

        drNet = ''
        for ds in ('../data', '/syn', '/distNet_labels', '/%s'%(system_name)):
            drNet = drNet + ds
            if not os.path.exists(drNet):
                os.makedirs(drNet)

        for run in range(1, max_run + 1):
            print system_name, 'run', run

            resultRxn = open(dr + '/rxn_syn_%s-run-%d.dat'%(system_name, run), 'w')
            resultRxn.write('# %s\t%s'%('distinctive_net_label', 'Rxn'))

            resultDistNet = open(drNet + '/distNet_syn_%s-run-%d.dat'%(system_name, run), 'w')
            resultDistNet.write('# %s\t%s\t%s'%('distinctive_net_label', 'system_name', 'species'))

            rxn_set= set()
            rxn_distinctive_genome = 0
            genome_list = list(range(1, number_of_species[system_name] + 1))
            genome_list = np.random.choice(genome_list, number_of_samples[system_name], replace=False)
            for species in genome_list:
                rxnFile = open('../data/bio/rxn_lists/%s/rxn_%s-%d.dat'%(system_name, system_name, species), 'r')
                rxn_list = []
                rxnFile.readline()
                for line in rxnFile:
                    rxn = line.rstrip()  # rxn_lists contain unique rxns for each genome
                    rxn_list.append(rxn)
                rxnFile.close()
                diff_rxn_set = set(rxn_list).difference(rxn_set)
                if len(diff_rxn_set) > 0:
                    rxn_distinctive_genome += 1
                    for x in diff_rxn_set:
                        resultRxn.write('\n%d\t%s'%(rxn_distinctive_genome, x))
                    rxn_set = rxn_set.union(set(rxn_list))
                resultDistNet.write('\n%d\t%s\t%d'%(rxn_distinctive_genome, system_name, species))


#----- syn of all individual systems -----#
if syn_type == 'a':
    file_names = ['all', \
                 'all_parsed']

    list_systems = {'all': ['individual_archaea', 'individual_bacteria', 'individual_eukarya'], \
                    'all_parsed': ['individual_archaea_parsed', 'individual_bacteria_parsed', 'individual_eukarya']}

    for name in file_names:

        dr = ''
        for ds in ('../data', '/syn', '/rxn_lists', '/individual_%s'%(name)):
            dr = dr + ds
            if not os.path.exists(dr):
                os.makedirs(dr)
        drNet = ''
        for ds in ('../data', '/syn', '/distNet_labels', '/individual_%s'%(name)):
            drNet = drNet + ds
            if not os.path.exists(drNet):
                os.makedirs(drNet)


        for run in range(1, max_run + 1):

            resultRxn = open(dr + '/rxn_syn_individual_%s-run-%d.dat'%(name, run), 'w')
            resultRxn.write('# %s\t%s'%('distinctive_net_label', 'Rxn'))

            resultDistNet = open(drNet + '/distNet_syn_individual_%s-run-%d.dat'%(name, run), 'w')
            resultDistNet.write('# %s\t%s\t%s'%('distinctive_net_label', 'system_name', 'species'))

            genome_list_all = []
            for system_name in list_systems[name]:
                print name, system_name, 'run', run
                genome_list = list(range(1, number_of_species[system_name] + 1))
                genome_list = np.random.choice(genome_list, number_of_samples[system_name], replace=False)
                genome_list_group = [(system_name, g) for g in genome_list]
                genome_list_all = genome_list_all + genome_list_group

            genome_list_all = np.random.permutation(genome_list_all)

            rxn_set= set()
            rxn_distinctive_genome = 0
            for k in genome_list_all:
                system_name = k[0]
                species = int(k[1])
                rxnFile = open('../data/bio/rxn_lists/%s/rxn_%s-%d.dat'%(system_name, system_name, species), 'r')
                rxn_list = []
                rxnFile.readline()
                for line in rxnFile:
                    rxn = line.rstrip()  # rxn_lists contain unique rxns for each genome
                    rxn_list.append(rxn)
                rxnFile.close()
                diff_rxn_set = set(rxn_list).difference(rxn_set)
                if len(diff_rxn_set) > 0:
                    rxn_distinctive_genome += 1
                    for x in diff_rxn_set:
                        resultRxn.write('\n%d\t%s'%(rxn_distinctive_genome, x))
                    rxn_set = rxn_set.union(set(rxn_list))
                resultDistNet.write('\n%d\t%s\t%d'%(rxn_distinctive_genome, system_name, species))
