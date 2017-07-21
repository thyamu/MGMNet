class Kegg:
    def __init__(self):
        EnzRxn_file = open('../data/kegg_mapping/kegg_enz_rxn.dat', 'r')
        RxnReat_file = open('../data/kegg_mapping/kegg_rxn_reactants.dat', 'r')
        RxnProd_file = open('../data/kegg_mapping/kegg_rxn_products.dat', 'r')

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
