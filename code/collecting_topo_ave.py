import sys
import os
import csv
import mgmnet.bio_nets as bn
import mgmnet.union_nets as un
import mgmnet.syn_nets as sn
import mgmnet.ranRxn_nets as rn
import mgmnet.bioRanRxn_nets as brn
import mgmnet.kegg_nets as kn
import mgmnet.topo_measure as tm
import shutil
import pandas as pd

#---------- results to be connected ==> topo_ave ----------#
topo = tm.topoMeasure()
header = topo.header

#---------- class of networks ----------#
module_name = sys.argv[1]
module_dict = {'bio': bn.bio(), \
               'union': un.union(), \
               'syn': sn.syn(), \
               'ranRxn': rn.ranRxn(), \
               'bioRanRxn':brn.bioRanRxn()}

class_name = module_dict[module_name]

#---------- directories ----------#
dr_collection = ''
for ds in ('../results_cluster', '/topo_ave', '/%s'%(module_name)):
    dr_collection = dr_collection + ds
    if not os.path.exists(dr_collection):
        os.makedirs(dr_collection)

dr_missing = ''
for ds in ('../results_cluster', '/topo_ave', '/%s'%(module_name)):
    dr_missing = dr_missing + ds
    if not os.path.exists(dr_missing):
        os.makedirs(dr_missing)

dr_missing_batch = ''
for ds in ('../cluster', '/missing', '/topo_ave'):
    dr_missing_batch = dr_missing_batch + ds


#---------- collecting results and identifying missing results ----------#
df_list = []
for system_name in class_name.number_of_species.iterkeys():
# for system_name in ['syn_individual_archaea',\
#                     'syn_individual_bacteria',\
#                     'syn_individual_eukarya',\
#                     'syn_individual_all',\
#                     'syn_ecosystem_JGI']:
    print system_name

    dr_results = ''
    for ds in ('../results_cluster', '/topo_ave', '/%s'%(module_name), '/%s'%(system_name)):
        dr_results = dr_results + ds
        if not os.path.exists(dr_results):
            os.makedirs(dr_results)

    collectedFileName = dr_collection + '/topo_ave_%s.csv'%(system_name)
    with open(collectedFileName, "w") as of:
        cof = csv.writer(of)
        cof.writerow(header)

    missingFileName = dr_missing + '/missing_topo_ave_%s'%(system_name)
    with open(missingFileName, "w") as mf:
       cmf = csv.writer(mf)

    for species in range(1, class_name.number_of_species[system_name] + 1):
        print species
        result_file_string = {'bio': '%s-%d.csv'%(system_name, species), \
                       'union': '%s-upto-%d.csv'%(system_name, species), \
                       'syn': '%s-%d.csv'%(system_name, species), \
                       'ranRxn': '%s-%d.csv'%(system_name, species),\
                       'bioRanRxn': '%s-%d.csv'%(system_name, species)} #==>change the string after generate syn results

        resultFileName = dr_results + '/' + result_file_string[module_name]
        #print resultFileName
        if not os.path.isfile(resultFileName):
            sample = [species]
            with open(missingFileName, "a") as mf:
                cmf = csv.writer(mf)
                cmf.writerow(sample)
            continue

        with open(resultFileName, "r") as rf:
            crf = csv.reader(rf, delimiter = ",")
            data = list(crf)
            row_count = len(data)

        if row_count == class_name.lines_in_topo_ave[system_name]:
            l = class_name.lines_in_topo_ave[system_name] - 1
            outcome = data[l]
        else:
            sample = [species]
            with open(missingFileName, "a") as mf:
                cmf = csv.writer(mf)
                cmf.writerow(sample)
            continue

        with open(collectedFileName, "a") as of:
            cof = csv.writer(of)
            cof.writerow(outcome)

    df_list.append(pd.read_csv(collectedFileName))

    missingBatchName = dr_missing_batch + '/missing_topo_ave_%s'%(system_name)
    if os.path.isfile(missingBatchName):
        os.remove(missingBatchName)

    #------copy missingFile to cluster folder -------#
    if os.stat(missingFileName).st_size > 0:
        if not os.path.exists(dr_missing_batch):
            os.makedirs(dr_missing_batch)
        shutil.copyfile(missingFileName, missingBatchName)
    else:
        os.remove(missingFileName)

#-------- Merge all files into one-----------#
finalFileName = dr_collection + '/topo_ave_%s.csv'%(module_name)
full_df = pd.concat(df_list)
full_df.to_csv(finalFileName)
