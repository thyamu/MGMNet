import sys
import os
import csv
import mgmnet.bio_nets as bn
import mgmnet.bipartite_topo_measure as bitm


bio = bn.bio()
topo = bitm.topoMeasure()

# level
level = bio.level[sys.argv[1]]
# group
group = bio.group[sys.argv[2]]
# species
species = int(sys.argv[3])

system_name = '%s_%s'%(level, group)

dr = ''
for ds in ('../results_test', '/topo_ave', '/bio_bipartite', '/%s'%(system_name)):
    dr = dr + ds
    if not os.path.exists(dr):
        os.makedirs(dr)

outputFileName = dr + '/bipartite_%s-%d.csv'%(system_name, species)

header = topo.header
with open(outputFileName, 'w') as f:
    if os.stat(outputFileName).st_size == 0: # if file not yet written
        csvf = csv.writer(f)
        csvf.writerow(header)

# species_name
species_name = bio.species_name(system_name, species)

# nbr_rxn
nbr_rxn = bio.number_of_rxn(system_name, species)

data0 = [level, group, species, species_name, nbr_rxn]

#----- To import sub-netwroks with rxn-degree for node attributes -----#
rEdges = bio.rxn_edges(system_name, species)
#nodeAttr = bio.rxn_degree(system_name, species)


#--- To Compute ---#
data1 = topo.bipartite_global_measure(rEdges)
data = data0 + data1

with open(outputFileName, 'a') as f:
    csvf = csv.writer(f)
    csvf.writerow(data)
