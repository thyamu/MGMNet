import os
import sys
import xlrd
import networkx as nx
import collections as cll
import numpy as np
import mgmnet.kegg_nets as kg

##### build chirality dictionary
file_chirality = "../original_data/chirality/KEGG_biosphere_chirality_right_left_protein_forming_amino_acids.xls"
book = xlrd.open_workbook(file_chirality)
sh = book.sheet_by_index(0)

chirality_string = {'Chiral': "chiral", \
                    'Achiral': "achiral", \
                    'chiral': "chiral", \
                    'Left': "chiral", \
                    'Racemic': "chiral", \
                    'Right': "chiral", \
                    'Both Achiral & Chiral': "unknown", \
                    'Unknown Achiral or Chiral': "unknown", \
                    'Both Achiral & Racemic': "unknown",\
                    'Both Achiral & Chiral Pieces': "unknown"}

dict_chiral = {}
for s in range(1, sh.nrows):
    compound = sh.cell_value(rowx = s, colx = 0)
    ch = sh.cell_value(rowx = s, colx = 1)
    dict_chiral[compound] = chirality_string[ch]

##### load reaction list from each domain
kegg = kg.kegg()

list_system = ["union_individual_archaea_parsed", "union_individual_bacteria_parsed", "union_individual_eukarya"]
list_rxn = {}
set_rxn = {}
for system_name in list_system:
    inputfile_name = "../data/union/rxn_lists/rxn_%s.dat"%(system_name)
    rxn_domain = np.loadtxt(inputfile_name, dtype='str', comments="#", delimiter="\t", unpack=False)
    list_rxn[system_name] = [rxn_domain[i][1] for i in range(len(rxn_domain))]
    set_rxn[system_name] = set(list_rxn[system_name])

###### obtain intersection and differences of reaction list amongst every domain
intersection_rxn = set_rxn[list_system[0]]
for system_name in list_system[1:]:
     intersection_rxn = intersection_rxn.intersection(set_rxn[system_name])
        
exclusive_rxn = {}
for system_name in list_system:
    exclusive_rxn[system_name] = set_rxn[system_name]
    for compare_group in list_system:
        if compare_group == system_name:
            continue
        exclusive_rxn[system_name] = exclusive_rxn[system_name].difference(set_rxn[compare_group])

##### map each reaction to chirality of chemical compounds participating in the reaction excluisvely for each domain
for system_name in list_system:
    ### array_chiral: chirality distribution \
    array_chiral = ["reaction", "nbr_total", "nbr_chiral", "nbr_achiral", "nbr_unknown", "ratio_c_to_a", "percentage_c", "percentage_a", "percentage_u"]
    for x in exclusive_rxn[system_name]:
        if x not in kegg.rxn_prod.keys() or x not in kegg.rxn_reac.keys():
            continue
        list_com = kegg.rxn_reac[x] + kegg.rxn_prod[x]
        nbr_chiral = 0
        nbr_achiral = 0
        nbr_unknown = 0
        for s in list_com:
            if dict_chiral[s] == 'chiral':
                nbr_chiral += 1
            elif dict_chiral[s] == 'achiral':
                nbr_achiral += 1
            else:
                nbr_unknown += 1
        nbr_total = len(list_com)
        if nbr_achiral == 0:
            ratio_c_to_a = -1
        else:
            ratio_c_to_a = nbr_chiral * 1.0 / nbr_achiral
        ac = [x, nbr_total, nbr_chiral, nbr_achiral, nbr_unknown, ratio_c_to_a, \
            nbr_chiral * 1.0 / nbr_total, nbr_achiral * 1.0 / nbr_total, nbr_unknown * 1.0 / nbr_total]
        array_chiral = np.vstack((array_chiral, ac))

    ### path for results
    dir_output = "../results"
    for ds in ("/chirality", "/stat"):
        dir_output += ds
        if not os.path.exists(dir_output):
            os.makedirs(dir_output)
    output_file_name_dist = dir_output + "/rxn_chiral_distribution_exclusive_%s.dat"%(system_name)

    ### save the chirality arrays in the output files
    array_chiral.dump(output_file_name_dist)

##### map each reaction to chirality of chemical compounds participating in the reaction included in all domains
### array_chiral: chirality distribution \
array_chiral = ["reaction", "nbr_total", "nbr_chiral", "nbr_achiral", "nbr_unknown", "ratio_c_to_a", "percentage_c", "percentage_a", "percentage_u"]
for x in intersection_rxn:
    if x not in kegg.rxn_prod.keys() or x not in kegg.rxn_reac.keys():
        continue
    list_com = kegg.rxn_reac[x] + kegg.rxn_prod[x]
    nbr_chiral = 0
    nbr_achiral = 0
    nbr_unknown = 0
    for s in list_com:
        if dict_chiral[s] == 'chiral':
            nbr_chiral += 1
        elif dict_chiral[s] == 'achiral':
            nbr_achiral += 1
        else:
            nbr_unknown += 1
    nbr_total = len(list_com)
    if nbr_achiral == 0:
        ratio_c_to_a = -1
    else:
        ratio_c_to_a = nbr_chiral * 1.0 / nbr_achiral
    ac = [x, nbr_total, nbr_chiral, nbr_achiral, nbr_unknown, ratio_c_to_a, \
        nbr_chiral * 1.0 / nbr_total, nbr_achiral * 1.0 / nbr_total, nbr_unknown * 1.0 / nbr_total]
    array_chiral = np.vstack((array_chiral, ac))

### path for results
dir_output = "../results"
for ds in ("/chirality", "/stat"):
    dir_output += ds
    if not os.path.exists(dir_output):
        os.makedirs(dir_output)
output_file_name_dist = dir_output + "/rxn_chiral_distribution_intersection_all_domains.dat"

### save the chirality arrays in the output files
array_chiral.dump(output_file_name_dist)
