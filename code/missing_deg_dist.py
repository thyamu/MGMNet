import sys
import os
import csv
import mgmnet.bio_nets as bn
import mgmnet.union_nets as un
import mgmnet.syn_nets as sn
import mgmnet.ranRxn_nets as rn
import shutil
import pandas as pd

#---------- class of networks ----------#
module_name = sys.argv[1]
module_dict = {'bio': bn.bio(), \
               'union': un.union(), \
               'syn': sn.syn(), \
               'ranRxn': rn.ranRxn()}

class_name = module_dict[module_name]

#---------- directories ----------#
dr_missing = ''
for ds in ('../results_cluster', '/deg_dist', '/%s'%(module_name)):
    dr_missing = dr_missing + ds
    if not os.path.exists(dr_missing):
        os.makedirs(dr_missing)

dr_missing_batch = ''
for ds in ('../cluster', '/missing', '/deg_dist'):
    dr_missing_batch = dr_missing_batch + ds


#---------- collecting the list of missing samples----------#
for system_name in class_name.number_of_species.iterkeys():
    print system_name

    dr_results = ''
    for ds in ('../results_cluster', '/deg_dist', '/%s'%(module_name), '/sub_degree', '/%s'%(system_name)):
        dr_results = dr_results + ds
        if not os.path.exists(dr_results):
            os.makedirs(dr_results)

    missingFileName = dr_missing + '/missing_deg_dist_%s'%(system_name)
    with open(missingFileName, "w") as mf:
       cmf = csv.writer(mf)

    for species in range(1, class_name.number_of_species[system_name] + 1):
        print species
        result_file_string = {'bio': '%s-%d.csv'%(system_name, species), \
                       'union': '%s-%d.csv'%(system_name, species), \
                       'syn': '%s-%d.csv'%(system_name, species), \
                       'ranRxn': '%s-%d.csv'%(system_name, species)} #==>change the string after generate syn results

        resultFileName = dr_results + '/deg_dist_lcc_' + result_file_string[module_name]
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

        if row_count < 2:
            sample = [species]
            with open(missingFileName, "a") as mf:
                cmf = csv.writer(mf)
                cmf.writerow(sample)


    #     with open(collectedFileName, "a") as of:
    #         cof = csv.writer(of)
    #         cof.writerow(outcome)
    #
    # df_list.append(pd.read_csv(collectedFileName))

    missingBatchName = dr_missing_batch + '/missing_deg_dist_%s'%(system_name)
    if os.path.isfile(missingBatchName):
        os.remove(missingBatchName)

    #------copy missingFile to cluster folder -------#
    if os.stat(missingFileName).st_size > 0:
        if not os.path.exists(dr_missing_batch):
            os.makedirs(dr_missing_batch)
        shutil.copyfile(missingFileName, missingBatchName)
    else:
        os.remove(missingFileName)

# #-------- Merge all files into one-----------#
# finalFileName = dr_collection + '/topo_ave_%s.csv'%(module_name)
# full_df = pd.concat(df_list)
# full_df.to_csv(finalFileName)
