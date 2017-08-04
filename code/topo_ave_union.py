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
