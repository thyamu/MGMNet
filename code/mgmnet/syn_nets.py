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

        self.number_of_species = {'syn_individual_archaea':250, \
                                'syn_individual_bacteria':300, \
                                'syn_individual_archaea_parsed':150 \
                                'syn_individual_bacteria_parsed':200,\
                                'syn_individual_eukarya':77, \
                                'syn_individual_all': 627,\
                                'syn_individual_all_parsed': 427, \
                                'syn_ecosystem_JGI':500}

        self.lines_in_topo_ave = {'syn_individual_archaea':2, \
                                'syn_individual_bacteria':2, \
                                'syn_individual_archaea_parsed':2, \
                                'syn_individual_bacteria_parsed':2,\
                                'syn_individual_eukarya':2, \
                                'syn_individual_all': 2,\
                                'syn_individual_all_parsed': 2, \
                                'syn_ecosystem_JGI':2}


    def species_name(self, system_name, species):
        species_name = system_name + '-upto-%d'%(species)
        return species_name


    def number_of_rxn(self, system_name, species):
        inputfile = open('../data/union_data/rxn_%s.dat'%(system_name), 'r')
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
        inputfile = open('../data/union_data/rxn_%s.dat'%(system_name), 'r')
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


    # def assign_seed(self, index1, index2):
    #     import numpy as np
    #     seed1 = 268332
    #     seed2 = 800304
    #     np.random.seed(seed1)
    #     list_first_seed = np.random.random_integers(0, 1000000, index1+1)
    #     #print list_first_seed
    #     np.random.seed(seed2)
    #     list_second_seed = np.random.random_integers(0, 1000000, index2+1)
    #     #print list_second_seed
    #     new_seed = list_first_seed[index1] + list_second_seed[index2]
    #     return new_seed

    # def combine_set_genome(self, group_dict, comSize, comSet):
    #     import numpy as np
    #     new_seed = self.assign_seed(comSize, comSet)
    #     np.random.seed(new_seed)
    #     genome_dict = {}
    #     for group in group_dict.iterkeys():
    #         if group_dict[group] == 0:
    #             continue
    #         genome_dict[group] = np.random.choice(\
    #                             range(1, self.number_of_species[group] + 1), \
    #                             int(group_dict[group] * comSize), replace = False)
    #     return genome_dict
