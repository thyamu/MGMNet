import os
import random as ran


# def load_set_species(size, group, level='individual'):
#
#     BIOSYSTEMS = {'ecosystem_YNP':26, 'ecosystem_JGI':5587, \
#             'individual_archaea':845, 'individual_bacteria':21637, \
#             'individual_archaea_parsed':199, 'individual_bacteria_parsed':1153}
#
#     for n in size:
#         print n

def load_rxns(level, group, set_species):
    rxn_list = []
    for species in set_species:
        inputfile = open('../data/rxn_lists/%s_%s/%d.dat'%(level, group, species), 'r')
        species = inputfile.readline()
        for line in inputfile:
            rxn = line.rstrip()
            if rxn in rxn_list:
                continue
            rxn_list.append(rxn)
        inputfile.close()
    return rxn_list


def rxn_edges(rxn_list, rxn_reac, rxn_prod):
    edge_list = []
    for x in rxn_list:
        for r in rxn_reac[x]:
            edge_list.append((r, x))
        for p in rxn_prod[x]:
            edge_list.append((x, p))
    return edge_list


def sub_edges(rxn_list, rxn_reac, rxn_prod):
    edge_list = []
    for x in rxn_list:
        for r in rxn_reac[x]:
            for p in rxn_prod[x]:
                if r == p: ### remove self-loops from sub-sub nets
                    continue
                edge_list.append((r, p))
    return edge_list


if __name__=='__main__':
    list_ran = ran.sample(range(1,3), 2)
    print list_ran
