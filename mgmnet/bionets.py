import os
import time


def loadRxns(level, group, species):
    rxn_list = []
    inputfile = open('../data/rxn_lists/%s_%s/%d.dat'%(level, group, species), 'r')
    species = inputfile.readline()
    for line in inputfile:
        rxn = line.rstrip()
        if rxn in rxn_list:
            continue
        rxn_list.append(rxn)
    return rxn_list


def loadSetRxns(level, group, set_species):
    rxn_list = []
    for species in set_species:
        inputfile = open('../data/rxn_lists/%s_%s/%d.dat'%(level, group, species), 'r')
        species = inputfile.readline()
        for line in inputfile:
            rxn = line.rstrip()
            if rxn in rxn_list:
                continue
            rxn_list.append(rxn)
    return rxn_list


def rxnEdges(rxn_list, rxn_reac, rxn_prod):
    edge_list = []
    for x in rxn_list:
        for r in rxn_reac[x]:
            edge_list.append((r, x))
        for p in rxn_prod[x]:
            edge_list.append((x, p))
    return edge_list


def subEdges(rxn_list, rxn_reac, rxn_prod):
    edge_list = []
    for x in rxn_list:
        for r in rxn_reac[x]:
            for p in rxn_prod[x]:
                if r == p: ### remove self-loops from sub-sub nets
                    continue
                edge_list.append((r, p))
    return edge_list
