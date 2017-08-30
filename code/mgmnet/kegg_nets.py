class kegg:
    def __init__(self):
        EnzRxn_file = open('../data/kegg/kegg_enz_rxn.dat', 'r')
        RxnReat_file = open('../data/kegg/kegg_rxn_reactants.dat', 'r')
        RxnProd_file = open('../data/kegg/kegg_rxn_products.dat', 'r')

        dict_a = {}
        for line in EnzRxn_file:
            items = line.rstrip().split('\t')
            dict_a[items[0]] = items[1:]
        EnzRxn_file.close()

        dict_b = {}
        for line in RxnReat_file:
            items = line.rstrip().split('\t')
            dict_b[items[0]] = items[1:]
        RxnReat_file.close()

        dict_c = {}
        for line in RxnProd_file:
            items = line.rstrip().split('\t')
            dict_c[items[0]] = items[1:]
        RxnProd_file.close()

        self.enz_rxn = dict_a
        self.rxn_reac = dict_b
        self.rxn_prod = dict_c

        self.enz = self.enz_rxn.keys()
        self.rxn = self.rxn_reac.keys()


    # def species_name(self):
    #     return "kegg"


    # def number_of_rxn(self):
    #     nbr_rxn = len(self.rxn)
    #     return nbr_rxn


    # def sub_edges(self):
    #     edge_list = []
    #     rxn_list = self.rxn
    #     for x in rxn_list:
    #         for r in self.rxn_reac[x]:
    #             for p in self.rxn_prod[x]:
    #                 if r == p: ### remove self-loops from sub-sub nets
    #                     continue
    #                 edge_list.append((r, p))
    #     return edge_list


    # def rxn_edges(self):
    #     edge_list = []
    #     rxn_list = self.rxn
    #     for x in rxn_list:
    #         for r in self.rxn_reac[x]:
    #             edge_list.append((r, x))
    #         for p in self.rxn_prod[x]:
    #             edge_list.append((x, p))
    #     return edge_list


    # def rxn_degree(self):
    #     dict_sub_nbrRxn = {}
    #     sub_set = set()
    #     rxn_list = self.rxn
    #     for x in rxn_list:
    #         for r in self.rxn_reac[x]:
    #             if r not in sub_set:
    #                 dict_sub_nbrRxn[r] = 0
    #                 dict_sub_nbrRxn[r] += 1
    #                 sub_set.add(r)
    #             else:
    #                 dict_sub_nbrRxn[r] += 1
    #         for p in self.rxn_prod[x]:
    #             if p not in sub_set:
    #                 dict_sub_nbrRxn[p] = 0
    #                 dict_sub_nbrRxn[p] += 1
    #                 sub_set.add(p)
    #             else:
    #                 dict_sub_nbrRxn[p] += 1
    #     return dict_sub_nbrRxn
