class artEco:
    def __init__(self):
        self.level = 'artificial'
        self.group = {'a': 'archaea', 'b': 'bacteria', 'e': 'eukarya'}
        self.number_of_species = {'archaea':845, 'bacteria':21637, 'eukarya':77}


    def assign_seed(self, index1, index2):
        import numpy as np
        seed1 = 268332
        seed2 = 800304
        np.random.seed(seed1)
        list_first_seed = np.random.random_integers(0, 1000000, index1+1)
        #print list_first_seed
        np.random.seed(seed2)
        list_second_seed = np.random.random_integers(0, 1000000, index2+1)
        #print list_second_seed
        new_seed = list_first_seed[index1] + list_second_seed[index2]
        return new_seed


    def combine_set_genome(self, group_dict, comSize, comSet):
        import numpy as np
        new_seed = self.assign_seed(comSize, comSet)
        np.random.seed(new_seed)
        genome_dict = {}
        for group in group_dict.iterkeys():
            if group_dict[group] == 0:
                continue
            genome_dict[group] = np.random.choice(\
                                range(1, self.number_of_species[group] + 1), \
                                int(group_dict[group] * comSize), replace = False)
        return genome_dict

    def load_list_ec(self, system_name, species):
        ec_list = []
        inputfile = open('../data/ec_lists/%s/ec_%s-%d.dat'%(system_name, system_name, species), 'r')
        inputfile.readline()
        for line in inputfile:
            items = line.rstrip().split('\t')
            ec_list.append(items[0])
        inputfile.close()
        return ec_list

    def combine_set_ec(self, genome_dict):
        ec_set = set()
        for group in genome_dict.iterkeys():
            system_name = 'individual_%s'%(group)
            for species in genome_dict[group]:
                ec_list = self.load_list_ec(system_name, species)
                ec_set = ec_set.union(set(ec_list))
        return ec_set

    def combined_enz_presence(self, ec_set, enz):
        ep = 0
        if enz in ec_set:
            ep = 1
        return ep


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

    def combined_set_rxn(self, genome_dict):
        rxn_set = set()
        for group in genome_dict.iterkeys():
            system_name = 'individual_%s'%(group)
            for species in genome_dict[group]:
                rxn_list = self.load_list_rxn(system_name, species)
                rxn_set = rxn_set.union(set(rxn_list))
        return rxn_set

    def combined_sub_edges(self, genome_dict):
        import kegg_nets as kg
        kegg = kg.Kegg()
        edge_list = []
        rxn_set = self.combined_set_rxn(genome_dict)
        for x in rxn_set:
            for r in kegg.rxn_reac[x]:
                for p in kegg.rxn_prod[x]:
                    if r == p: ### remove self-loops from sub-sub nets
                        continue
                    edge_list.append((r, p))
        return edge_list


    def combined_rxn_edges(self, genome_dict):
        import kegg_nets as kg
        kegg = kg.Kegg()
        edge_list = []
        rxn_set = self.combined_set_rxn(genome_dict)
        for x in rxn_set:
            for r in kegg.rxn_reac[x]:
                edge_list.append((r, x))
            for p in kegg.rxn_prod[x]:
                edge_list.append((x, p))
        return edge_list


    def combined_rxn_degree(self, genome_dict):
        import kegg_nets as kg
        kegg = kg.Kegg()
        rxn_set = self.combined_set_rxn(genome_dict)
        sub_set = set()
        dict_sub_nbrRxn = {}
        for x in rxn_set:
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
