import os
import sys
import xlrd
import networkx as nx
import collections as cll
import numpy as np


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

kegg_dist_chirality = cll.Counter(dict_chiral.values())

##### load biological networks to obtain the set of nodes for each net
type_chirality = ["chiral", "achiral", "unknown"]
dir_bionet = "../results/networks/bio"
dict_systems = {"ap":"individual_archaea_parsed", "bp":"individual_bacteria_parsed", "e": "individual_eukarya"}
for system_name in dict_systems.itervalues():
    ### path for input network data
    dir_data = dir_bionet + "/" + system_name
    nbr_files = len(next(os.walk(dir_data))[2]) #get the number of files under dir_data

    ### array_chiral: chirality distribution for each networks
    array_chiral = ["net", "nbr_total", "nbr_chiral", "nbr_achiral", "nbr_unknown", "ratio_c_to_a", "percentage_c", "percentage_a", "percentage_u"]
    for i in range(1, nbr_files + 1):
        ### load a network
        file_name = dir_data + "/" + "sub_nodes_%s-%d.gpickle"%(system_name, i)
        G = nx.read_gpickle(file_name)

        nbr_chiral = 0
        nbr_achiral = 0
        nbr_unknown = 0
        for n in G.nodes_iter():
            if dict_chiral[n] == 'chiral':
                nbr_chiral += 1
            elif dict_chiral[n] == 'achiral':
                nbr_achiral += 1
            else:
                nbr_unknown += 1

        nbr_total = len(G.nodes())
        if nbr_achiral == 0:
            ratio_c_to_a = -1
        else:
            ratio_c_to_a = nbr_chiral * 1.0 / nbr_achiral

        x = system_name + '_%d'%(i)
        ac = [x, nbr_total, nbr_chiral, nbr_achiral, nbr_unknown, ratio_c_to_a, \
            nbr_chiral * 1.0 / nbr_total, nbr_achiral * 1.0 / nbr_total, nbr_unknown * 1.0 / nbr_total]
        array_chiral = np.vstack((array_chiral, ac))

    ### path for results
    dir_output = "../results"
    for ds in ("/chirality", "/stat"):
        dir_output += ds
        if not os.path.exists(dir_output):
            os.makedirs(dir_output)
    output_file_name_dist = dir_output + "/bionet_chiral_distribution_%s.dat"%(system_name)

    ### save the chirality arrays in the output files
    array_chiral.dump(output_file_name_dist)
