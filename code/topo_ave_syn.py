import sys
import os
import csv
import mgmnet.syn_nets as sn
import mgmnet.topo_measure as tm

syn = sn.syn()
topo = tm.topoMeasure()

# level
level = syn.level[sys.argv[1]]
# group
group = syn.group[sys.argv[2]]
# species
species = int(sys.argv[3])

system_name = '%s_%s'%(level, group)

dr = ''
for ds in ('../results_test','/topo_ave', '/syn', '/%s'%(system_name)):
    dr = dr + ds
    if not os.path.exists(dr):
        os.makedirs(dr)

outputFileName = dr + '/%s-%d.csv'%(system_name, species)

header = topo.header
with open(outputFileName, 'w') as f:
    if os.stat(outputFileName).st_size == 0: # if file not yet written
        csvf = csv.writer(f)
        csvf.writerow(header)

# species_name
species_name = syn.species_name(system_name, species)

# nbr_rxn
nbr_rxn = syn.number_of_rxn(system_name, species)

data0 = [level, group, species, species_name, nbr_rxn]

#----- To import sub-netwroks with rxn-degree for node attributes -----#
sEdges = syn.sub_edges(system_name, species)
nodeAttr = syn.rxn_degree(system_name, species)

#--- To Compute ---#
data1 = topo.global_measure(sEdges, nodeAttr)
data = data0 + data1

with open(outputFileName, 'a') as f:
    csvf = csv.writer(f)
    csvf.writerow(data)
