#import os

def load_list_rxn(level, group, species):
    rxn_list = []
    inputfile = open('../data/rxn_lists/%s_%s/%d.dat'%(level, group, species), 'r')
    species_name = inputfile.readline()
    for line in inputfile:
        rxn = line.rstrip()
        if rxn in rxn_list:
            continue
        rxn_list.append(rxn)
    inputfile.close()
    return rxn_list


def load_list_rxn_from_files(file_name):
    rxn_list = []
    inputfile = open(file_name, 'r')
    species_name = inputfile.readline()
    for line in inputfile:
        rxn = line.rstrip()
        if rxn in rxn_list:
            continue
        rxn_list.append(rxn)
    inputfile.close()
    return rxn_list, species_name


def rxn_edges(rxn_list, rxn_reac, rxn_prod):
    edge_list = []
    for x in rxn_list:
        for r in rxn_reac[x]:
            edge_list.append((r, x))
        for p in rxn_prod[x]:
            edge_list.append((x, p))
    return edge_list


def attribute_nbr_rxn(rxn_list, rxn_reac, rxn_prod):
    dict_sub_rxn = {}
    for x in rxn_list:
        for r in rxn_reac[x]:
            dict_sub_rxn[x] = []


def sub_edges(rxn_list, rxn_reac, rxn_prod):
    edge_list = []
    for x in rxn_list:
        for r in rxn_reac[x]:
            for p in rxn_prod[x]:
                if r == p: ### remove self-loops from sub-sub nets
                    continue
                edge_list.append((r, p))
    return edge_list


def create_networks_files(name):
    import kegg as kg

    kegg = kg.Kegg()

    BIOSYSTEMS = {'ecosystem_YNP':26, 'ecosystem_JGI':5587, \
            'individual_archaea':845, 'individual_bacteria':21637, \
            'individual_archaea_parsed':199, 'individual_bacteria_parsed':1153}

    # for species in range(BIOSYSTEMS[name]):
    #     inputFileName = '../data/%s/%d.dat'%(name, species+1)
    #     outputFileName = '../networks/%s/%d.dat'%(name, species+1)
    #     rxn_list, species_name = bn.load_rxns_file(inputFileName)
    #     se = bn.sub_edges(rxn_list, kegg.rxn_reac, kegg.rxn_prod)
    #     with open(outputFileName, 'w') as outputFile:
    #         outputFile.write('%s'%(species_name))
    #         for e in se:
    #             outputFile.write('\n%s'%(e))





if __name__=='__main__':
    create_networks_files('ecosystem_YNP')
