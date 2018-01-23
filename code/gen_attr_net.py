import os
import sys
import xlrd
import networkx as nx


dir_bionet = "../results/networks/bio"
dict_systems = {"ap":"individual_archaea_parsed", "bp":"individual_bacteria_parsed", "e": "individual_eukarya"}
system_name = dict_systems[sys.argv[1]]

#build chirality dictionary
file_chirality = "../original_data/chirality/KEGG_biosphere_chirality_right_left_protein_forming_amino_acids.xls"
book = xlrd.open_workbook(file_chirality)
sh = book.sheet_by_index(0)

dict_chiral = {}
for s in range(1, sh.nrows):
    compound = sh.cell_value(rowx = s, colx = 0)
    chirality = sh.cell_value(rowx = s, colx = 1)
    dict_chiral[compound] = chirality

#print dict_chiral['C00025']

dir_data = dir_bionet + "/" + system_name
nbr_files = len(os.listdir(dir_data))#get the number of files under dir_data
print nbr_files

dir_results = "../results"
for ds in ("networks_node_attributes", "bio", system_name):
    dir_results = dir_results + "/" + ds
    if not os.path.exists(dir_results):
        os.makedirs(dir_results)

# for i in os.listdir(dir_data):
#     file_name = dir_data + "/" + i
#     #print file_name
#     G = nx.read_gpickle(file_name)
#     for n in G.nodes_iter():
