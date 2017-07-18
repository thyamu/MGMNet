#add number of total ec
#add number of total rxn

def enz_presence(system_name, nbr_species, enz):
    dict_species_enzPresence = {}
    inputfile = open('../data/ec_array/ec_%s.dat'%(system_name), 'r')
    list_system_ec = inputfile.readline().rstrip().split('\t')
    if enz in list_system_ec: #check if the enzyme exists in the list for the system_name
        index_enz = list_system_ec.index(enz) # list_system_ec has unique EC numbers. In general, index() returns the first index
        species = 0
        for line in inputfile:
            items = line.rstrip().split('\t')
            species += 1
            if items[index_enz] == '0':
                dict_species_enzPresence[species] = 0
            else:
                dict_species_enzPresence[species] = 1
    else: #==> if the enzyme doesnt exist in the list for the system_name
        for i in range(1, nbr_species + 1 ):
            dict_species_enzPresence[i] = 0
    return dict_species_enzPresence


def number_of_ec(system_name):
    dict_species_nbrEc = {}
    inputfile = open('../data/ec_array/ec_%s.dat'%(system_name), 'r')
    list_system_ec = inputfile.readline().rstrip().split('\t')
    species = 0
    for line in inputfile:
        items = line.rstrip().split('\t')
        species += 1
        dict_species_nbrEc[species] = items[1]
    return dict_species_nbrEc
