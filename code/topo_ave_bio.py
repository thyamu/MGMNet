import sys
import os
import csv
import mgmnet.bio_nets as bn
import mgmnet.topo_measure as tm

bio = bn.bioSys()
topo = tm.topoMeasure()

# level
level = bio.level[sys.argv[1]]
# group
group = bio.group[sys.argv[2]]
# species
species = int(sys.argv[3])

system_name = '%s_%s'%(level, group)
dr = '../results_test'
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
species_name = bio.species_name(system_name, species)

# nbr_ec
nbr_ec = bio.number_of_ec(system_name, species)
# nbr_rxn
nbr_rxn = bio.number_of_rxn(system_name, species)
# EC 1.9.3.1 presence
enz = '1.9.3.1'
ec_presence = bio.enz_presence(system_name, species, enz)

data0 = [level, group, species, species_name, nbr_ec, nbr_rxn, ec_presence]

#--- Import sub-netwroks ---#
sEdges = bio.sub_edges(system_name, species)
nodeAttr = bio.rxn_degree(system_name, species)

data1 = topo.global_measure(sEdges, nodeAttr)
data = data0 + data1

with open(outputFileName, 'a') as f:
    csvf = csv.writer(f)
    csvf.writerow(data)
