import sys
import os
import csv
import mgmnet.syn_nets as sn
import mgmnet.topo_measure as tm

syn = sn.synEco()
topo = tm.topoMeasure()

# level
level = 'ecosystem'
# group
group = 'syn_%s'%(sys.argv[1]) # ex. syn_a ==> synthetic nets of archaea genomes
# species
comSize = int(sys.argv[2])
comSet = int(sys.argv[3])
species = 'size%d_set%d'%(comSize, comSet)

system_name = '%s_%s'%(level, group)

dr = ''
for ds in ('../results_cluster','/%s'%(system_name)):
    dr = dr + ds
    if not os.path.exists(dr):
        os.makedirs(dr)

outputFileName = dr + '/%s-%s.csv'%(system_name, species)

header = topo.header
with open(outputFileName, 'w') as f:
    if os.stat(outputFileName).st_size == 0: # if file not yet written
        csvf = csv.writer(f)
        csvf.writerow(header)

# species_name
species_name = species

# nbr_ec
nbr_ec = sn.number_of_ec(system_name, species)
# nbr_rxn
nbr_rxn = sn.number_of_rxn(system_name, species)
# EC 1.9.3.1 presence
enz = '1.9.3.1'
ec_presence = sn.enz_presence(system_name, species, enz)
