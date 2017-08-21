import sys
import os
import csv
import mgmnet.bio_nets as bn
import mgmnet.union_nets as un
import mgmnet.topo_measure as tm

# Line_BIOSYSTEMS = {'ecosystem_YNP':2, 'ecosystem_JGI':2, \
#         'individual_archaea':1, 'individual_bacteria':1, \
#         'individual_archaea_parsed':1, 'individual_bacteria_parsed':1, \
#         'individual_eukarya':1}

# Line_UNIONS = {'union_archaea':2, \
#             'union_bacteria':2, \
#             'union_eukarya':2, \
#             'union_all': 2}
#
# # Nbr_BIOSYSTEMS = {'ecosystem_YNP':26, 'ecosystem_JGI':5587, \
# #         'individual_archaea':845, 'individual_bacteria':21637, \
# #         'individual_archaea_parsed':199, 'individual_bacteria_parsed':1153, \
# #         'individual_eukarya':77}
#
# Nbr_UNIONS = {'union_archaea':188, \
#             'union_bacteria':183, \
#             'union_eukarya':58, \
#             'union_all': 383}
#
#
# header = [ "level", "group", "species", "species_name", "nbr_rxn", \
#            "nbr_nodes", "nbr_edges", "nbr_connected_components", \
#            "nbr_nodes_lcc", "nbr_edges_lcc", \
#            "ave_degree_lcc", "std_degree_lcc", \
#            "ave_degree_square_lcc", "std_degree_square_lcc", \
#            "ave_clustering_coeff_lcc", "std_clustering_coeff_lcc", \
#            "ave_shortest_path_length_lcc", "std_shortest_path_length_lcc", \
#            "ave_betweenness_nodes_lcc", "std_betweenness_nodes_lcc", \
#            "ave_betweenness_edges_lcc", "std_betweenness_edges_lcc", \
#            "assortativity_lcc", "attribute_assortativity_lcc", \
#            "diameter_lcc"]


for system_name in Nbr_UNIONS.iterkeys():
    print system_name

    # outputFileName = 'topo_average_%s.csv'%(system_name)
    # with open(outputFileName, "w") as of:
    #     cof = csv.writer(of)
    #     cof.writerow(header)
    #
    # missingFileName = 'intermediate_processing/missing_samples_%s.csv'%(system_name)
    # missingHeader = [system_name]
    # with open(missingFileName, "w") as mf:
    #     cmf = csv.writer(mf)
    #     cmf.writerow(missingHeader)

    for species in range(1, Nbr_UNIONS[system_name] + 1): #[3431]:
        print species
        resultFileName = '%s/%s-upto-%d.csv'%(system_name, system_name, species)
        if not os.path.isfile(resultFileName):
            sample = [species]
            with open(missingFileName, "a") as mf:
                cmf = csv.writer(mf)
                cmf.writerow(sample)
            #missing_results[system_name].append(species)
            continue

        with open(resultFileName, "r") as rf:
            crf = csv.reader(rf, delimiter = ",")
            data = list(crf)
            row_count = len(data)

        if row_count == Line_UNIONS[system_name]:
            l = Line_UNIONS[system_name] - 1
            outcome = data[l]
        else:
            sample = [species]
            with open(missingFileName, "a") as mf:
                cmf = csv.writer(mf)
                cmf.writerow(sample)
            #missing_results[system_name].append(species)
            #outcome = "missing"
            continue

        with open(outputFileName, "a") as of:
            cof = csv.writer(of)
            cof.writerow(outcome)

    # with open(missingFileName, "a") as mf:
    #     cmf = csv.writer(mf)
    #     cmf.writerow(sample)
