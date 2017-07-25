import sys
import os
import csv
import mgmnet.kegg_nets as kn
import mgmnet.topo_measure as tm

#bio = bn.bioSys()
kegg = kn.Kegg()
topo = tm.topoMeasure()

# level
level = "biosphere" # = kegg.level[sys.argv[1]]
# group
group = "kegg" # = kegg.group[sys.argv[2]]
# species
species = 1 # = int(sys.argv[3])

system_name = '%s_%s'%(level, group) #"biosphere_kegg"

dr = '../results_cluster'
if not os.path.exists(dr):
    os.makedirs(dr)
drs = dr + '/%s'%(system_name)
if not os.path.exists(drs):
    os.makedirs(drs)
outputFileName = drs + '/%s-%d.csv'%(system_name, species)

header = topo.header
with open(outputFileName, 'w') as f:
    if os.stat(outputFileName).st_size == 0: # if file not yet written
        csvf = csv.writer(f)
        csvf.writerow(header)

# species_name
species_name = kegg.species_name()

# nbr_ec
nbr_ec = kegg.number_of_ec()
# nbr_rxn
nbr_rxn = kegg.number_of_rxn()
# EC 1.9.3.1 presence
enz = '1.9.3.1'
ec_presence = kegg.enz_presence(enz)

data0 = [level, group, species, species_name, nbr_ec, nbr_rxn, ec_presence]

#--- Import sub-netwroks ---#
sEdges = kegg.sub_edges()
nodeAttr = kegg.rxn_degree()

data1 = topo.global_measure(sEdges, nodeAttr)
data = data0 + data1

with open(outputFileName, 'a') as f:
    csvf = csv.writer(f)
    csvf.writerow(data)
