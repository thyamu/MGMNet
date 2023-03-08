### To generate graphs in gexf format for visulation ###
#0. biosphere with 1, 2 and 3 embeded
#1. archaeasphere
#2. bacteriasphere
#3. eukaryasphere

### Attributes to add
# 0. degree (default)
# 1. domain

import mgmnet.union_nets as un
import networkx as nx

union = un.union()
system_name = "union_individual_all"
species = union.number_of_species[system_name]
sEdges = union.sub_edges(system_name, species)
file_name = '../viz/sub_net_%s_chiral'%(system_name)
G = nx.Graph(sEdges)

##### NOTE: 2019 Version of the file_chirality
name_file_chirality =  "/Users/hyunju/research/projects/2019-Chirality/data/kegg/annotation/kegg_chiral_analysis_release.xls"

#####  Format and Import Method (current: .xls through xlrd)
import xlrd

book = xlrd.open_workbook(name_file_chirality)
sh = book.sheet_by_index(1)

dict_com_center = dict()
for s in range(2, sh.nrows):
    c = sh.cell_value(rowx = s, colx = 0)
    compound = c.split('.')[0]
    ch = int(sh.cell_value(rowx = s, colx = 6))
    dict_com_center[compound] = ch

sum_na = 0
for n in G.nodes():
    ##### chiral centers
    if n not in dict_com_center.keys():
        sum_na += 1
        cc = 0
    else:
        cc = dict_com_center[n]
    ##### chirality
    if cc == 0:
        chi  = 0
    else:
        chi = 1
    G.add_node(n,center=cc, chirality=chi)

nx.write_gml(G, '%s.gml'%(file_name))
nx.write_gexf(G, '%s.gexf'%(file_name))
