import sys
import mgmnet.net_generator as ng
import numpy as np
import csv

Level_BIOSYSTEMS = {'e': 'ecosystem', 'i': 'individual', 'b':'biosphere'}
Group_BIOSYSTEMS = {'y': 'YNP', 'j': 'JGI', 'a': 'archaea', 'b': 'bacteria', \
                    'ap':'archaea_parsed', 'bp':'bacteria_parsed', \
                    'e': 'eukarya', 'k': 'kegg'}
Nbr_BIOSYSTEMS = {'ecosystem_YNP':26, 'ecosystem_JGI':5587, \
        'individual_archaea':845, 'individual_bacteria':21637, \
        'individual_archaea_parsed':199, 'individual_bacteria_parsed':1153,\
        'individual_eukarya':77, 'biosphere_kegg':1}


Nbr_Individual = Nbr_BIOSYSTEMS['individual_archaea'] + \
                 Nbr_BIOSYSTEMS['individual_bacteria'] + \
                 Nbr_BIOSYSTEMS['individual_eukarya']

Nbr_Individual_Parsed = Nbr_BIOSYSTEMS['individual_archaea_parsed'] + \
                 Nbr_BIOSYSTEMS['individual_bacteria_parsed'] + \
                 Nbr_BIOSYSTEMS['individual_eukarya']

lower_bound = int(sys.argv[1])
for i in range(lower_bound, lower_bound + 5):
    print "####### sample", i
    genomeFile = open('../results/genomeIndividualList-bae-%d.dat'%i, 'w')
    genome_list = np.random.choice(range(1, Nbr_Individual), 21000, replace=False)
    #list_nbr_rxn = []
    rxn_set = set()
    index = 1
    for genome in genome_list:
        print index
        if genome < Nbr_BIOSYSTEMS['individual_archaea'] + 1:
            system_name = 'individual_archaea'
            species = genome
        elif genome < Nbr_BIOSYSTEMS['individual_archaea'] + Nbr_BIOSYSTEMS['individual_bacteria'] + 1:
            system_name = 'individual_bacteria'
            species = genome - Nbr_BIOSYSTEMS['individual_archaea']
        else:
            system_name = 'individual_eukarya'
            species = genome - Nbr_BIOSYSTEMS['individual_archaea'] - Nbr_BIOSYSTEMS['individual_bacteria']
        rxn_list, species_name = ng.load_list_rxn(system_name, species)
        rxn_set = rxn_set.union(set(rxn_list))
        #list_nbr_rxn.append(len(rxn_set))
        genomeFile.write('%d\t%d\n'%(index, len(rxn_set)))
        index += 1
    genomeFile.close()


for i in range(lower_bound, lower_bound + 5):
    print "####### sample", i
    genomeFile = open('../results/genomeIndividualList-b-%d.dat'%i, 'w')
    genome_list = np.random.choice(range(1, Nbr_BIOSYSTEMS['individual_bacteria']), 21000, replace=False)
    #list_nbr_rxn = []
    rxn_set = set()
    index = 0
    for genome in genome_list:
        system_name = 'individual_bacteria'
        species = genome
        # print index
        # if genome < Nbr_BIOSYSTEMS['individual_archaea'] + 1:
        #     system_name = 'individual_archaea'
        #     species = genome
        # elif genome < Nbr_BIOSYSTEMS['individual_archaea'] + Nbr_BIOSYSTEMS['individual_bacteria'] + 1:
        #     system_name = 'individual_bacteria'
        #     species = genome - Nbr_BIOSYSTEMS['individual_archaea']
        # else:
        #     system_name = 'individual_eukarya'
        #     species = genome - Nbr_BIOSYSTEMS['individual_archaea'] - Nbr_BIOSYSTEMS['individual_bacteria']
        rxn_list, species_name = ng.load_list_rxn(system_name, species)
        rxn_set = rxn_set.union(set(rxn_list))
        #list_nbr_rxn.append(len(rxn_set))
        genomeFile.write('%d\t%d\n'%(index, len(rxn_set)))
        index += 1
    genomeFile.close()
