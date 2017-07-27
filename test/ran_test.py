import numpy as np


def assign_seed(seed1, seed2, index1, index2):
    np.random.seed(seed1)
    list_first_seed = np.random.random_integers(0, 1000000, index1+1)
    #print list_first_seed
    np.random.seed(seed2)
    list_second_seed = np.random.random_integers(0, 1000000, index2+1)
    #print list_second_seed
    new_seed = list_first_seed[index1] + list_second_seed[index2]
    return new_seed




for index1 in [10, 100, 1000, 10000]:
    #print index1
    for index2 in range(100):
        #print index2
        new_seed = assign_seed(seed1, seed2, index1, index2)
        #print new_seed
