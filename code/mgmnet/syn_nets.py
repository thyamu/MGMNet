class synEco:
    def load_list_ec(self, system_name, species):
        ec_list = []
        inputfile = open('../data/ec_lists/%s/ec_%s-%d.dat'%(system_name, system_name, species), 'r')
        inputfile.readline()
        for line in inputfile:
            ec_array[species] = []
            items = line.rstrip().split('\t')
            for i in range(2, len(items)):
                if items[i] != '0':
                    ec_array[species].append(list_system_ec[i])
            species += 1
        inputfile.close()
        return ec_list

    def combine_set_ec(self, list_genome):
        ec_set = set()
        for genome in list_genome:
            system_name = genome[0]
            species = genome[1]
            ec_list = self.load_list_ec(system_name, species)
            ec_set = ec_set.union(set(ec_list))
        return ec_set

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

    def combined_set_rxn(self, list_genome):
        rxn_set = set()
        for genome in list_genome:
            system_name = genome[0]
            species = genome[1]
            rxn_list = self.load_list_rxn(system_name, species)
            rxn_set = rxn_set.union(set(rxn_list))
        return rxn_set

    def sub_edges(self, list_genome):
        import kegg_nets as kg
        kegg = kg.Kegg()
        edge_list = []
        rxn_set = self.combined_set_rxn(list_genome)
        for x in rxn_set:
            for r in kegg.rxn_reac[x]:
                for p in kegg.rxn_prod[x]:
                    if r == p: ### remove self-loops from sub-sub nets
                        continue
                    edge_list.append((r, p))
        return edge_list


    def rxn_edges(self, list_genome):
        import kegg_nets as kg
        kegg = kg.Kegg()
        edge_list = []
        rxn_set = self.combined_set_rxn(list_genome)
        for x in rxn_set:
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
