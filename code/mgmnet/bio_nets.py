class bioSys:
    def __init__(self):
        self.level = {'e': 'ecosystem', 'i': 'individual', 'b':'biosphere'}
        self.group = {'y': 'YNP', 'j': 'JGI', 'a': 'archaea', 'b': 'bacteria', \
                        'ap':'archaea_parsed', 'bp':'bacteria_parsed', \
                        'e': 'eukarya', 'k': 'kegg'}
        self.number_of_species = {'ecosystem_YNP':26, 'ecosystem_JGI':5587, \
            'individual_archaea':845, 'individual_bacteria':21637, \
            'individual_archaea_parsed':199, 'individual_bacteria_parsed':1153,\
            'individual_eukarya':77, 'biosphere_kegg':1}


    def species_name(self, system_name, species):
        rxn_list = []
        inputfile = open('../data/rxn_lists/%s/%d.dat'%(system_name, species), 'r')
        species_name = inputfile.readline().rstrip()[2:]
        inputfile.close()
        return species_name


    def number_of_ec(self, system_name, species):
        dict_species_nbrEc = {}
        inputfile = open('../data/ec_array/ec_%s.dat'%(system_name), 'r')
        list_system_ec = inputfile.readline().rstrip().split('\t')
        line_number = 1
        for line in inputfile:
            if species == line_number:
                items = line.rstrip().split('\t')
                nbrEc = items[1]
                break
            line_number += 1
        inputfile.close()
        return nbrEc

    def number_of_rxn(self, system_name, species):
        inputfile = open('../data/rxn_lists/%s/%d.dat'%(system_name, species), 'r')
        nbr_rxn = sum(1 for line in inputfile) - 1 #subtract 1 for the header in rxn_lists file
        inputfile.close()
        return nbr_rxn


    def enz_presence(self, system_name, species, enz):
        inputfile = open('../data/ec_array/ec_%s.dat'%(system_name), 'r')
        list_system_ec = inputfile.readline().rstrip().split('\t')
        ep = 0
        if enz in list_system_ec: #check if the enzyme exists in the list for the system_name
            index_enz = list_system_ec.index(enz) # list_system_ec has unique EC numbers. In general, index() returns the first index
            line_number = 1
            for line in inputfile:
                if species == line_number:
                    items = line.rstrip().split('\t')
                    if items[index_enz] == '0':
                        ep = 0
                    else:
                        ep = 1
                    break
                line_number += 1
        return ep


    def load_list_rxn(self, system_name, species):
        rxn_list = []
        inputfile = open('../data/rxn_lists/%s/%d.dat'%(system_name, species), 'r')
        species_name = inputfile.readline()
        for line in inputfile:
            rxn = line.rstrip()
            if rxn in rxn_list:
                continue
            rxn_list.append(rxn)
        inputfile.close()
        return rxn_list


    def sub_edges(self, system_name, species):
        import kegg as kg
        kegg = kg.Kegg()
        edge_list = []
        rxn_list = self.load_list_rxn(system_name, species)
        for x in rxn_list:
            for r in kegg.rxn_reac[x]:
                for p in kegg.rxn_prod[x]:
                    if r == p: ### remove self-loops from sub-sub nets
                        continue
                    edge_list.append((r, p))
        return edge_list


    def rxn_edges(self, system_name, species):
        import kegg as kg
        kegg = kg.Kegg()
        edge_list = []
        rxn_list = self.load_list_rxn(system_name, species)
        for x in rxn_list:
            for r in kegg.rxn_reac[x]:
                edge_list.append((r, x))
            for p in kegg.rxn_prod[x]:
                edge_list.append((x, p))
        return edge_list


    def rxn_degree(self, system_name, species):
        import kegg as kg
        kegg = kg.Kegg()
        rxn_list = self.load_list_rxn(system_name, species)
        sub_set = set()
        dict_sub_nbrRxn = {}
        for x in rxn_list:
            for r in kegg.rxn_reac[x]:
                if r not in sub_set:
                    dict_sub_nbrRxn[r] = 0
                    dict_sub_nbrRxn[r] += 1
                    sub_set.add(r)
                else:
                    dict_sub_nbrRxn[r] += 1
            for p in kegg.rxn_prod[x]:
                if p not in sub_set:
                    dict_sub_nbrRxn[p] = 0
                    dict_sub_nbrRxn[p] += 1
                    sub_set.add(p)
                else:
                    dict_sub_nbrRxn[p] += 1
        return dict_sub_nbrRxn
