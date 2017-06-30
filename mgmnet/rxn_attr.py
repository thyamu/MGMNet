import os

def nbr_of_rxns(rxn_list, rxn_reac, rxn_prod):
    sub_rxnNbr = {}
    set_sub = set()
    for x in rxn_list:
        for r in rxn_reac[x]:
            if r not in set_sub:
                sub_rxnNbr[r] = 0
                set_sub.add(r)
            sub_rxnNbr[r] += 1
        for p in rxn_prod[x]:
            if p not in set_sub:
                sub_rxnNbr[p] = 0
                set_sub.add(p)
            sub_rxnNbr[p] += 1
    return sub_rxnNbr
