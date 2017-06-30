
def load_list_rxn(level, group, species):
    rxn_list = []
    inputfile = open('../data/rxn_lists/%s_%s/%d.dat'%(level, group, species), 'r')
    species_name = inputfile.readline().rstrip()
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
    species_name = inputfile.readline().rstrip()[2:]
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


def sub_edges(rxn_list, rxn_reac, rxn_prod):
    edge_list = []
    for x in rxn_list:
        for r in rxn_reac[x]:
            for p in rxn_prod[x]:
                if r == p: ### remove self-loops from sub-sub nets
                    continue
                edge_list.append((r, p))
    return edge_list


#def create_networks_files(name):


if __name__=='__main__':

    import kegg as kg
    kegg = kg.Kegg()

    BIOSYSTEMS = {'ecosystem_YNP':26, 'ecosystem_JGI':5587, \
            'individual_archaea':845, 'individual_bacteria':21637, \
            'individual_archaea_parsed':199, 'individual_bacteria_parsed':1153}
