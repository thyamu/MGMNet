import os
import kegg as kg
import bio_nets as bn



kegg = kg.Kegg()

BIOSYSTEMS = {'ecosystem_YNP':26, 'ecosystem_JGI':5587, \
        'individual_archaea':845, 'individual_bacteria':21637, \
        'individual_archaea_parsed':199, 'individual_bacteria_parsed':1153}

dir = '../results'
if not os.path.exists(dir):
    os.makedirs(dir)

name_lists = ['ecosystem_YNP']
for name in name_lists:
    outputFileName = dir + '/%s.csv'%(name)
    outputFile = open(outputFileName, 'w')
    for species in range(BIOSYSTEMS[name]):
        inputFileName = '../data/rxn_lists/%s/%d.dat'%(name, species+1)
        rxn_list, species_name = bn.load_rxns_file(inputFileName)
        se = bn.sub_edges(rxn_list, kegg.rxn_reac, kegg.rxn_prod)
