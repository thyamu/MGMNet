import numpy.random as ran


def load_list_rxn(system_name, species):
    rxn_list = []
    inputfile = open('../data/rxn_lists/%s/%d.dat'%(system_name, species), 'r')
    species_name = inputfile.readline().rstrip()[2:]
    for line in inputfile:
        rxn = line.rstrip()
        if rxn in rxn_list:
            continue
        rxn_list.append(rxn)
    inputfile.close()
    return rxn_list, species_name


def enz_presence(system_name, nbr_species, enz):
    dict_species_enzPresence = {}
    inputfile = open('../data/ec_array/ec_%s.dat'%(system_name), 'r')
    list_system_ec = inputfile.readline().rstrip().split('\t')
    if enz in list_system_ec:
        index_enz = list_system_ec.index(enz) # list_system_ec has unique EC numbers. In general, index() returns the first index
        species = 0
        for line in inputfile:
            items = line.rstrip().split('\t')
            species += 1
            if items[index_enz] == '0':
                dict_species_enzPresence[species] = 0
            else:
                dict_species_enzPresence[species] = 1
    else:
        for i in range(1, nbr_species + 1 ):
            dict_species_enzPresence[i] = 0
    return dict_species_enzPresence


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
