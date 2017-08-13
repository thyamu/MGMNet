class ecAnalysis:

    def bio_number_of_ec(self, system_name, species):
        inputfile = open('../data/ec_array/ec_%s.dat'%(system_name), 'r')
        list_system_ec = inputfile.readline().rstrip().split('\t')
        line_number = 1
        for line in inputfile:
            if species == line_number:
                items = line.rstrip().split('\t')
                nbrEc = items[1]
                break
            line_number += 1
        inputfile.close()
        return nbrEc


    def bio_load_list_ec(self, system_name, species):
        ec_list = []
        inputfile = open('../data/ec_lists/%s/ec_%s-%d.dat'%(system_name, system_name, species), 'r')
        inputfile.readline()
        for line in inputfile:
            items = line.rstrip().split('\t')
            ec_list.append(items[0])
        inputfile.close()
        return ec_list


    def bio_number_of_effective_ec(self, system_name, species):
        eff_ec_list = []
        inputfile = open('../data/effective_ec_lists/%s/effective_ec_%s-%d.dat'%(system_name, system_name, species), 'r')
        inputfile.readline()
        line_number = 0
        for line in inputfile:
            line_number += 1
        inputfile.close()
        return line_number


    def union_load_list_ec(self, system_name, species):
        ec_list = []
        inputfile = open('../data/ec_lists/%s/ec_%s-%d.dat'%(system_name, system_name, species), 'r')
        inputfile.readline()
        for line in inputfile:
            items = line.rstrip().split('\t')
            ec_list.append(items[0])
        inputfile.close()
        return ec_list

    def union_number_of_ec(self, system_name, species):
        ec_set = set()
        for species in range(1, self.number_of_species[system_name] +1):
            ec_list = self.load_list_ec(system_name, species)
            ec_set = ec_set.union(set(ec_list))
        nbrEc = len(ec_set)
        return nbrEc
