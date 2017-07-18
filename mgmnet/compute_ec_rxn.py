import sys
import os
import net_attr
import net_generator as ng
import numpy as np
import csv
import kegg as kg

kegg = kg.Kegg()

print len(kegg.enz)
print len(kegg.rxn)

dicta = kegg.rxn_prod
print len(dicta)

# Level_BIOSYSTEMS = {'e': 'ecosystem', 'i': 'individual'}#, 'b':'biosphere'}
# Group_BIOSYSTEMS = {'y': 'YNP', 'j': 'JGI', 'a': 'archaea', 'b': 'bacteria', \
#                     'ap':'archaea_parsed', 'bp':'bacteria_parsed', \
#                     'e': 'eukarya'}#, 'k': 'kegg'}
# Nbr_BIOSYSTEMS = {'ecosystem_YNP':26, 'ecosystem_JGI':5587, \
#         'individual_archaea':845, 'individual_bacteria':21637, \
#         'individual_archaea_parsed':199, 'individual_bacteria_parsed':1153,\
#         'individual_eukarya':77}#, 'biosphere_kegg':1}
#
#
# for system_name in Nbr_BIOSYSTEMS.iterkeys():
#     print system_name
#     items = system_name.split('_')
#     # level
#     level = items[0]
#     # group
#     group = items[1]
#     if len(items) > 2:
#         for i in range(2, len(items)):
#             group = group + '_%s'%(items[i])
#
#     #load nbr_ec from ec_array files
#     dict_species_nbrEc = net_attr.number_of_ec(system_name)
#
#     dr = '../results'
#     if not os.path.exists(dr):
#         os.makedirs(dr)
#
#     header = [ "level", "group", "species", "species_name", "nbr_ec", "nbr_rxn"]
#
#     outputFileName = dr + '/nbr_ec_rxn_%s.csv'%(system_name)
#     with open(outputFileName, 'w') as f:
#         if os.stat(outputFileName).st_size == 0: # if file not yet written
#             csvf = csv.writer(f)
#             csvf.writerow(header)
#
#     for species in range(1, Nbr_BIOSYSTEMS[system_name]+1):
#         print species
#         # #species_name
#         # rxn_list, species_name = ng.load_list_rxn(system_name, species)
#         # #nbr_rxn
#         # nbr_rxn = len(rxn_list)
#
#         inputfile = open('../data/rxn_lists/%s/%d.dat'%(system_name, species), 'r')
#         #species_name
#         species_name = inputfile.readline().rstrip()[2:]
#
#
#         #nbr_ec
#         nbr_ec = dict_species_nbrEc[species]
#
#         #nbr_rxn
#         nbr_rxn = sum(1 for line in inputfile)
#         inputfile.close()
#
#
#         data = [level, group, species, species_name, nbr_ec, nbr_rxn]
#
#         with open(outputFileName, 'a') as f:
#             csvf = csv.writer(f)
#             csvf.writerow(data)
