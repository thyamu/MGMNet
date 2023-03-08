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

##### map each reaction in kegg to chirality of chemical compounds participating in the reaction
### array_chiral: chirality distribution \
kegg = kg.kegg()
array_chiral = ["reaction", "nbr_total", "nbr_chiral", "nbr_achiral", "nbr_unknown", \
                "ratio_c_to_a", "percentage_chiral", "percentage_achiral", "percentage_unknown", \
                "nbr_chiral_reactant", "nbr_chiral_product", \
                "nbr_achiral_reactant", "nbr_achiral_product", \
                "nbr_unknown_reactant", "nbr_unknown_product", \
                "percentage_chiral_reactant", "percentage_chiral_product", \
                "percentage_achiral_reactant", "percentage_achiral_product", \
                "percentage_unknown_reactant", "percentage_unknown_product"]

for x in rxn_kegg:
    if x not in kegg.rxn_prod.keys() or x not in kegg.rxn_reac.keys():
        continue
    #list_com = kegg.rxn_reac[x] + kegg.rxn_prod[x]
    nbr_chiral = 0
    nbr_achiral = 0
    nbr_unknown = 0
    nbr_chiral_reactant = 0
    nbr_chiral_product = 0
    nbr_achiral_reactant = 0
    nbr_achiral_product = 0
    nbr_unknown_reactant = 0
    nbr_unknown_product = 0

    ## To identify chirality of reactants for every reactions x
    for s in kegg.rxn_reac[x]:
        if dict_chiral[s] == 'chiral':
            nbr_chiral_reactant += 1
        elif dict_chiral[s] == 'achiral':
            nbr_achiral_reactant += 1
        else:
            nbr_unknown_reactant += 1

    ## To compute the percentage of chirality in reactants for reaction x
    nbr_reactant = len(kegg.rxn_reac[x])
    percentage_chiral_reactant = 1.0 * nbr_chiral_reactant / nbr_reactant
    percentage_achiral_reactant = 1.0 * nbr_achiral_reactant / nbr_reactant
    percentage_unknown_reactant = 1.0 * nbr_unknown_reactant / nbr_reactant


    ## To dentify chirality of products for every reactions x
    for s in kegg.rxn_prod[x]:
        if dict_chiral[s] == 'chiral':
            nbr_chiral_product += 1
        elif dict_chiral[s] == 'achiral':
            nbr_achiral_product += 1
        else:
            nbr_unknown_product += 1

    ## To compute the percentage of chirality in products for reaction x
    nbr_product = len(kegg.rxn_prod[x])
    percentage_chiral_product = 1.0 * nbr_chiral_product / nbr_product
    percentage_achiral_product = 1.0 * nbr_achiral_product / nbr_product
    percentage_unknown_product = 1.0 * nbr_unknown_product / nbr_product

    ## To compute the percentage of chirality in the whole compounds for reaction x
    nbr_total = nbr_reactant + nbr_product
    nbr_chiral = nbr_chiral_reactant + nbr_chiral_product
    nbr_achiral = nbr_achiral_reactant + nbr_achiral_product
    nbr_unknown = nbr_unknown_reactant + nbr_unknown_product

    if nbr_achiral == 0:
        ratio_c_to_a = -1
    else:
        ratio_c_to_a = nbr_chiral * 1.0 / nbr_achiral

    percentage_chiral = 1.0 * nbr_chiral / nbr_total
    percentage_achiral = 1.0 * nbr_achiral / nbr_total
    percentage_unknown = 1.0 * nbr_unknown / nbr_total

    ac = [x, nbr_total, nbr_chiral, nbr_achiral, nbr_unknown, \
        ratio_c_to_a, percentage_chiral, percentage_achiral, percentage_unknown, \
        nbr_chiral_reactant, nbr_chiral_product, \
        nbr_achiral_reactant, nbr_achiral_product, \
        nbr_unknown_reactant, nbr_unknown_product, \
        percentage_chiral_reactant, percentage_chiral_product, \
        percentage_achiral_reactant, percentage_achiral_product, \
        percentage_unknown_reactant, percentage_unknown_product]

    array_chiral = np.vstack((array_chiral, ac))

### path for results
dir_output = "../results"
for ds in ("/chirality", "/stat"):
    dir_output += ds
    if not os.path.exists(dir_output):
        os.makedirs(dir_output)
output_file_name_dist = dir_output + "/rxn_chiral_distribution_kegg_new.dat"

### save the chirality arrays in the output files
array_chiral.dump(output_file_name_dist)
