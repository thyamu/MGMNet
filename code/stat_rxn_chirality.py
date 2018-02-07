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


inputfile_name = "../data/bio/rxn_lists/biosphere_kegg/rxn_biosphere_kegg-2.dat"
rxn_kegg = np.loadtxt(inputfile_name, dtype='str', comments="#", delimiter="\n", unpack=False)

##### map each reaction to chirality of chemical compounds participating in the reaction
### array_chiral: chirality distribution \
kegg = kg.kegg()
array_chiral = ["reaction", "nbr_total", "nbr_chiral", "nbr_achiral", "nbr_unknown", "ratio_c_to_a", "percentage_c", "percentage_a", "percentage_u"]
for x in rxn_kegg:
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
output_file_name_dist = dir_output + "/rxn_chiral_distribution.dat"

### save the chirality arrays in the output files
array_chiral.dump(output_file_name_dist)
