class syn:
    def __init__(self):
        self.level = {'si': 'syn_individual',\
                    'se':'syn_ecosystem'}

        self.group = {'a': 'archaea', \
                    'b': 'bacteria', \
                    'ap':'archaea_parsed', \
                    'bp':'bacteria_parsed', \
                    'e': 'eukarya', \
                    'j': 'JGI', \
                    'all': 'all', \
                    'allp': 'all_parsed'}

        self.number_of_species = {'syn_individual_archaea':2000, \
                                'syn_individual_bacteria':2000, \
                                'syn_individual_archaea_parsed':1200,\
                                'syn_individual_bacteria_parsed':1800,\
                                'syn_individual_eukarya':770, \
                                'syn_individual_all': 4770,\
                                'syn_individual_all_parsed': 3770, \
                                'syn_ecosystem_JGI':4000}


        self.number_of_samples = {'syn_individual_archaea':200, \
                                'syn_individual_bacteria':200, \
                                'syn_individual_archaea_parsed':120,\
                                'syn_individual_bacteria_parsed':180,\
                                'syn_individual_eukarya':77, \
                                'syn_individual_all': 477,\
                                'syn_individual_all_parsed': 377, \
                                'syn_ecosystem_JGI':400}

        self.lines_in_topo_ave = {'syn_individual_archaea':2, \
                                'syn_individual_bacteria':2, \
                                'syn_individual_archaea_parsed':2, \
                                'syn_individual_bacteria_parsed':2,\
                                'syn_individual_eukarya':2, \
                                'syn_individual_all': 2,\
                                'syn_individual_all_parsed': 2, \
                                'syn_ecosystem_JGI':2}

    def species_name(self, system_name, species):
        species_name = system_name + '-%d'%(species)
        return species_name

    def number_of_rxn(self, system_name, species):
        inputfile = open('../data/syn/rxn_lists/%s/rxn_%s-%d.dat'%(system_name, system_name, species), 'r')
        nbr_rxn = sum(1 for line in inputfile) - 1 #subtract 1 for the header in rxn_lists file
        inputfile.close()
        return nbr_rxn

    def load_list_rxn(self, system_name, species):
        rxn_list = []
        inputfile = open('../data/syn/rxn_lists/%s/rxn_%s-%d.dat'%(system_name, system_name, species), 'r')
        species_name = inputfile.readline()
        for line in inputfile:
            rxn = line.rstrip()  # rxn_lists contain unique rxns for each genome
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
