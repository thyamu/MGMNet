class union:
    def __init__(self):
        self.level ={'ui': 'union_individual', 'ue': 'union_ecosystem'}

        self.group = {'a': 'archaea', \
                    'b': 'bacteria', \
                    'ap':'archaea_parsed', \
                    'bp':'bacteria_parsed', \
                    'e': 'eukarya', \
                    'j': 'JGI', \
                    'all': 'all', \
                    'allp': 'all_parsed'}

        self.number_of_species = {'union_individual_archaea':188, \
                                'union_individual_bacteria':183, \
                                'union_individual_archaea_parsed':105, \
                                'union_individual_bacteria_parsed':154,\
                                'union_individual_eukarya':58, \
                                'union_individual_all': 383,\
                                'union_individual_all_parsed': 291, \
                                'union_ecosystem_JGI':309}

        self.lines_in_topo_ave = {'union_individual_archaea':2, \
                                'union_individual_bacteria':2, \
                                'union_individual_archaea_parsed':2, \
                                'union_individual_bacteria_parsed':2,\
                                'union_individual_eukarya':2, \
                                'union_individual_all': 2,\
                                'union_individual_all_parsed': 2, \
                                'union_ecosystem_JGI':2}


    def species_name(self, system_name, species):
        species_name = system_name + '-upto-%d'%(species)
        return species_name


    def number_of_rxn(self, system_name, species):
        inputfile = open('../data/union/rxn_lists/rxn_%s.dat'%(system_name), 'r')
        inputfile.readline() #header
        nbr_rxn = 0
        for line in inputfile:
            items = line.rstrip().split('\t')
            label = int(items[0])
            nbr_rxn += 1
            if label > species:
                break
        inputfile.close()
        return nbr_rxn


    def load_list_rxn(self, system_name, species):
        rxn_list = []
        inputfile = open('../data/union/rxn_lists/rxn_%s.dat'%(system_name), 'r')
        inputfile.readline()
        for line in inputfile:
            items = line.rstrip().split('\t')
            label = int(items[0])
            if label > species:
                break
            rxn = items[1]
            rxn_list.append(rxn)
        inputfile.close()
        return rxn_list


    def sub_edges(self, system_name, species):
        import kegg_nets as kg
        kegg = kg.kegg()
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
        kegg = kg.kegg()
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
        kegg = kg.kegg()
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
