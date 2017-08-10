class unionEco:
    def __init__(self):
        self.level ={'ui': 'union_individual'}

        self.group = {'a': 'archaea', \
                    'b': 'bacteria', \
                    'ap':'archaea_parsed', \
                    'bp':'bacteria_parsed', \
                    'e': 'eukarya', \
                    'all': 'all', \
                    'allp': 'all_parsed'}

        self.number_of_species = {'union_individual_archaea':845, \
                                'union_individual_bacteria':21637, \
                                'union_individual_archaea_parsed':199, \
                                'union_individual_bacteria_parsed':1153,\
                                'union_individual_eukarya':77, \
                                'union_individual_all': 22559,\
                                'union_individual_all_parsed': 1429}


    def species_name(self, system_name, species):
        species_name = system_name + '-upto-%d'%(species)
        return species_name


    def load_list_ec(self, system_name, species):
        ec_list = []
        inputfile = open('../data/ec_lists/%s/ec_%s-%d.dat'%(system_name, system_name, species), 'r')
        inputfile.readline()
        for line in inputfile:
            items = line.rstrip().split('\t')
            ec_list.append(items[0])
        inputfile.close()
        return ec_list


    def load_list_rxn(self, system_name, species):
        rxn_list = []
        inputfile = open('../data/rxn_lists/%s/rxn_%s-%d.dat'%(system_name, system_name, species), 'r')
        species_name = inputfile.readline()
        for line in inputfile:
            rxn = line.rstrip()
            # if rxn in rxn_list: ==> rxn_lists contain unique rxns for each genome
            #     continue
            rxn_list.append(rxn)
        inputfile.close()
        return rxn_list


    def number_of_ec(self, system_name, species):
        ec_set = set()
        for species in range(1, self.number_of_species[system_name] +1):
            ec_list = self.load_list_ec(system_name, species)
            ec_set = ec_set.union(set(ec_list))
        nbrEc = len(ec_set)
        return nbrEc


    def number_of_rxn(self, system_name, species):
        rxn_set = set()
        for species in range(1, self.number_of_species[system_name] +1):
            rxn_list = self.load_list_rxn(system_name, species)
            rxn_set = rxn_set.union(set(rxn_list))
        nbr_rxn
        return nbr_rxn


    # def enz_presence(self, system_name, species, enz):
    #     import kegg_nets as kg
    #     kegg = kg.Kegg()
    #     ep = False
    #     if enz in kegg.enz: #check if the enzyme exists in kegg database
    #         inputfile = open('../data/ec_array/ec_%s.dat'%(system_name), 'r')
    #         list_system_ec = inputfile.readline().rstrip().split('\t')
    #         if enz in list_system_ec: #check if the enzyme exists in the list for the system_name
    #             index_enz = list_system_ec.index(enz) # index() returns the first index
    #             line_number = 1
    #             for line in inputfile:
    #                 if species == line_number:
    #                     items = line.rstrip().split('\t')
    #                     if items[index_enz] == '0': #no empty element for ec_array
    #                         ep = False
    #                     else:
    #                         ep = True
    #                     break
    #                 line_number += 1
    #         inputfile.close()
    #     return int(ep)
    #
    #
    # def enz_presence_from_ECset(self, ec_set, enz):
    #     if enz in ec_set: #check if the enzyme exists in the list for the system_name
    #         ep = True
    #     else:
    #         ep = False
    #     return int(ep)


    # def load_array_ec(self, system_name):
    #     ec_array = {}
    #     inputfile = open('../data/ec_array/ec_%s.dat'%(system_name), 'r')
    #     list_system_ec = inputfile.readline().rstrip().split('\t')
    #     species = 1
    #     for line in inputfile:
    #         ec_array[species] = []
    #         items = line.rstrip().split('\t')
    #         for i in range(2, len(items)):
    #             if items[i] != '0':
    #                 ec_array[species].append(list_system_ec[i])
    #         species += 1
    #     inputfile.close()
    #     return ec_array

    def load_list_ec(self, system_name, species):
        ec_list = []
        inputfile = open('../data/ec_lists/%s/ec_%s-%d.dat'%(system_name, system_name, species), 'r')
        inputfile.readline()
        for line in inputfile:
            items = line.rstrip().split('\t')
            ec_list.append(items[0])
        inputfile.close()
        return ec_list

    def load_list_rxn(self, system_name, species):
        rxn_list = []
        inputfile = open('../data/rxn_lists/%s/rxn_%s-%d.dat'%(system_name, system_name, species), 'r')
        species_name = inputfile.readline()
        for line in inputfile:
            rxn = line.rstrip()
            # if rxn in rxn_list: ==> rxn_lists contain unique rxns for each genome
            #     continue
            rxn_list.append(rxn)
        inputfile.close()
        return rxn_list


    def sub_edges(self, system_name, species):
        import kegg_nets as kg
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
        import kegg_nets as kg
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
        import kegg_nets as kg
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
