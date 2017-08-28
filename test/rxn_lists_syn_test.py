import os
import sys
import numpy as np
import time


syn_type = sys.argv[1] # syn_type=a works
                       # only after all syn_type=i files
                       # are created in ../data/syn/genome_lists/*
max_run = 1

number_of_species = {'individual_archaea':845, \
                    'individual_bacteria':21637, \
                    'individual_archaea_parsed':199, \
                    'individual_bacteria_parsed':1153,\
                    'individual_eukarya':77, \
                    'ecosystem_JGI':5587}

number_of_samples = {'individual_archaea':200, \
                    'individual_bacteria':200, \
                    'individual_archaea_parsed':120, \
                    'individual_bacteria_parsed':180,\
                    'individual_eukarya':77, \
                    'individual_all':477,\
                    'individual_all_parsed':377, \
                    'ecosystem_JGI':400}

#----- syn of each individual system -----#
if syn_type == 'i':
    # file_names = {'a':'individual_archaea',\
    #             'b':'individual_bacteria', \
    #             'ap':'individual_archaea_parsed', \
    #             'bp':'individual_bacteria_parsed',\
    #             'e':'individual_eukarya', \
    #             'j':'ecosystem_JGI'}

    file_names = {'a':'individual_archaea',\
                'b':'individual_bacteria'}

    system_name = file_names[sys.argv[2]]

    dr = ''
    for ds in ('../data', '/syn_test', '/rxn_lists', '/%s'%(system_name)):
        dr = dr + ds
        if not os.path.exists(dr):
            os.makedirs(dr)

    drNet = ''
    for ds in ('../data', '/syn_test', '/genome_lists', '/%s'%(system_name)):
        drNet = drNet + ds
        if not os.path.exists(drNet):
            os.makedirs(drNet)

    for run in range(1, max_run + 1):
        print system_name, 'run', run

        for sample in range(1, number_of_samples[system_name] + 1):
            print sample
            syn_species = (run - 1) * number_of_samples[system_name] + sample
            resultRxn = open(dr + '/rxn_syn_%s-%d.dat'%(system_name, syn_species), 'w')
            resultRxn.write('# %s-run-%d-sample-%d'%(system_name, run, sample))

            resultGenome = open(drNet + '/genome_syn_%s-%d.dat'%(system_name, syn_species), 'w')
            resultGenome.write('# %s\t%s'%('system_name', 'species'))

            start_time = time.time()
            genome_list = list(range(1, number_of_species[system_name] + 1))
            genome_list = np.random.choice(genome_list, sample, replace=False)
            end_time = time.time()
            print "time to choose a set of random genomes: ", end_time - start_time

            start_time = time.time()
            for species in genome_list:
                resultGenome.write('\n%s\t%d'%(system_name, species))
            end_time = time.time()
            print "time to write a set of random genomes into a file: ", end_time - start_time

            start_time_rxn_set = time.time()
            rxn_set= set()
            for species in genome_list:
                start_time = time.time()
                rxnFile = open('../data/bio/rxn_lists/%s/rxn_%s-%d.dat'%(system_name, system_name, species), 'r')
                rxn_list = []
                rxnFile.readline()
                for line in rxnFile:
                    rxn = line.rstrip()  # rxn_lists contain unique rxns for each genome
                    rxn_list.append(rxn)
                rxnFile.close()
                end_time = time.time()
                print "time to build a rxn_list for each genome: ", end_time - start_time

                start_time = time.time()
                rxn_set = rxn_set.union(set(rxn_list))
                end_time = time.time()
                print "time to compute union of two rxn_sets: ", end_time - start_time
            end_time_rxn_set = time.time()
            print "time to build a set of rxn: ", end_time_rxn_set - start_time_rxn_set

            start_time = time.time()
            for x in rxn_set:
                resultRxn.write('\n%s'%(x))
            end_time = time.time()
            print "time to write a set of rxn: ", end_time - start_time

# #----- syn of all individual systems -----#
# if syn_type == 'a':
#     file_names = ['all', \
#                  'all_parsed']
#
#     list_systems = {'all': ['individual_archaea', 'individual_bacteria', 'individual_eukarya'], \
#                     'all_parsed': ['individual_archaea_parsed', 'individual_bacteria_parsed', 'individual_eukarya']}
#
#     for name in file_names:
#         dr_all = ''
#         for ds in ('../data', '/syn', '/rxn_lists', '/individual_%s'%(name)):
#             dr_all = dr_all + ds
#             if not os.path.exists(dr_all):
#                 os.makedirs(dr_all)
#         drNet_all = ''
#         for ds in ('../data', '/syn', '/genome_lists', '/individual_%s'%(name)):
#             drNet_all = drNet_all + ds
#             if not os.path.exists(drNet_all):
#                 os.makedirs(drNet_all)
#
#         for run in range(1, max_run + 1):
#             genome_list_all = []
#             for system_name in list_systems[name]:
#                 syn_species = (run - 1) * number_of_samples[system_name]
#                 resultRxn = open(dr_all + '/rxn_syn_individual_%s-%d.dat'%(name, syn_species), 'w')
#                 resultRxn.write('# individual_%s-run-%d-sample-%d'%(name, run, sample))
#
#                 resultGenome = open(drNet_all + '/genome_syn_individual_%s-%d.dat'%(name, syn_species), 'w')
#                 resultGenome.write('# %s\t%s'%('system_name', 'species'))
#
#
#
#                     genomeFile = open(drNet + '/genome_syn_%s-%d.dat'%(system_name, syn_species), 'r')
#                     genome_list = list(range(1, number_of_species[system_name] + 1))
#                     genome_list = np.random.choice(genome_list, number_of_samples[system_name], replace=False)
#                     genome_list_group = [(system_name, g) for g in genome_list]
#                     genome_list_all = genome_list_all + genome_list_group
#
#                 genome_list_all = np.random.permutation(genome_list_all)

            # rxn_set= set()
            # rxn_distinctive_genome = 0
            # for k in genome_list_all:
            #     system_name = k[0]
            #     species = int(k[1])
            #     rxnFile = open('../data/bio/rxn_lists/%s/rxn_%s-%d.dat'%(system_name, system_name, species), 'r')
            #     rxn_list = []
            #     rxnFile.readline()
            #     for line in rxnFile:
            #         rxn = line.rstrip()  # rxn_lists contain unique rxns for each genome
            #         rxn_list.append(rxn)
            #     rxnFile.close()
            #     diff_rxn_set = set(rxn_list).difference(rxn_set)
            #     if len(diff_rxn_set) > 0:
            #         rxn_distinctive_genome += 1
            #         for x in diff_rxn_set:
            #             resultRxn.write('\n%d\t%s'%(rxn_distinctive_genome, x))
            #         rxn_set = rxn_set.union(set(rxn_list))
            #     resultDistNet.write('\n%d\t%s\t%d'%(rxn_distinctive_genome, system_name, species))
