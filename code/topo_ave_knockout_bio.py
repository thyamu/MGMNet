import sys
import os
import csv
import mgmnet.bio_nets_knockout as bnko
import mgmnet.simple_topo_measure as stm

bio = bnko.bio()
topo = stm.topoMeasure()

# level
level = bio.level[sys.argv[1]]
# group
group = bio.group[sys.argv[2]]
# species
species = int(sys.argv[3])
# knockout_ratio
knockout_ratio = float(sys.argv[4])

system_name = '%s_%s'%(level, group)

dr = ''
for ds in ('../results_cluster', '/topo_ave_knockout', '/bio', '/%s'%(system_name)):
    dr = dr + ds
    if not os.path.exists(dr):
        os.makedirs(dr)

outputFileName = dr + '/knockout%.2f_%s-%d.csv'\
                        %(knockout_ratio, system_name, species)

header = topo.header
with open(outputFileName, 'w') as f:
    if os.stat(outputFileName).st_size == 0: # if file not yet written
        csvf = csv.writer(f)
        csvf.writerow(header)

# species_name
species_name = bio.species_name(system_name, species)

# nbr_rxn
nbr_rxn = bio.number_of_rxn(system_name, species, knockout_ratio)

data0 = [level, group, species, species_name, nbr_rxn]

#----- To import sub-netwroks with rxn-degree for node attributes -----#
sEdges = bio.sub_edges(system_name, species, knockout_ratio)

#--- To Compute ---#
data1 = topo.simple_global_measure(sEdges)
data = data0 + data1

with open(outputFileName, 'a') as f:
    csvf = csv.writer(f)
    csvf.writerow(data)
