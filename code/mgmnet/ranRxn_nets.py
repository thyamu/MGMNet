class ranRxn:
    def __init__(self):
        self.level = {'ri': 'ranRxn_individual',\
                     're': 'ranRxn_ecosystem'}

        self.group = {#'a': 'archaea', \
        #             'b': 'bacteria', \
        #             'ap':'archaea_parsed', \
        #             'bp':'bacteria_parsed', \
        #             'e': 'eukarya', \
        #             'j': 'JGI', \
        #             'all': 'all', \
        #             'allp': 'all_parsed', \
                    'k': 'kegg'}

        self.number_of_species = {'ranRxn_individual_kegg':5000}

        self.lines_in_topo_ave = {'ranRxn_individual_kegg':2}


    def species_name(self, system_name, species):
        inputfile = open('../data/ranRxn/rxn_lists/%s/rxn_%s-%d.dat'%(system_name, system_name, species), 'r')
        species_name = inputfile.readline().rstrip()[2:]
        inputfile.close()
        return species_name

    def number_of_rxn(self, system_name, species):
        inputfile = open('../data/ranRxn/rxn_lists/%s/rxn_%s-%d.dat'%(system_name, system_name, species), 'r')
        nbr_rxn = sum(1 for line in inputfile) - 1 #subtract 1 for the header in rxn_lists file
        inputfile.close()
        return nbr_rxn

    def load_list_rxn(self, system_name, species):
        rxn_list = []
        inputfile = open('../data/ranRxn/rxn_lists/%s/rxn_%s-%d.dat'%(system_name, system_name, species), 'r')
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
            if x not in kegg.rxn_reac.keys() or x not in kegg.rxn_prod.keys(): #change this loop by changing kegg.rxn_reac or prod or associdated files
                continue
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
            if x not in kegg.rxn_reac.keys() or x not in kegg.rxn_prod.keys(): #change this loop by changing kegg.rxn_reac or prod or associdated files
                continue
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
