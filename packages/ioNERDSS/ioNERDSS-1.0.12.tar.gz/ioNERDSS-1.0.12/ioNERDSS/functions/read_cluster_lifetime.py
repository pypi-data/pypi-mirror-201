import numpy as np


def read_cluster_lifetime(FileName: str, SpeciesName: str, InitialTime: float, FinalTime: float):
    ti_switch = False
    tf_switch = False
    spec_switch = False
    lifetime_switch = False
    size_list = []
    ti_lifetime = []
    tf_lifetime = []
    with open(FileName, 'r') as file:
        for line in file.readlines():
            if line[0:6] == 'time: ':
                lifetime_switch = False
                spec_switch = False
                if float(line.split(' ')[1].strip('\n')) == InitialTime:
                    ti_switch = True
                if float(line.split(' ')[1].strip('\n')) == FinalTime:
                    tf_switch = True
                if float(line.split(' ')[1].strip('\n')) != InitialTime:
                    ti_switch = False
                if float(line.split(' ')[1].strip('\n')) != FinalTime:
                    tf_switch = False
            if line == 'lifetime for each mol type: \n':
                lifetime_switch = True
            if line == str(SpeciesName) + '\n':
                spec_switch = True
            if ti_switch and lifetime_switch and spec_switch:
                if line != str(SpeciesName) + '\n' and line != 'lifetime for each mol type: \n':
                    if line[0:20] == 'size of the cluster:':
                        size_list.append(int(line.split(':')[1].strip('\n')))
                    else:
                        str_list = line.strip('\n').strip(' ').split(' ')
                        temp = np.array([])
                        for i in str_list:
                            if i != '':
                                temp = np.append(temp, float(i))
                        ti_lifetime.append(temp)
            if tf_switch and lifetime_switch and spec_switch:
                if line != str(SpeciesName) + '\n' and line != 'lifetime for each mol type: \n':
                    if line[0:20] != 'size of the cluster:':
                        str_list = line.strip('\n').strip(' ').split(' ')
                        temp = np.array([])
                        for i in str_list:
                            if i != '':
                                temp = np.append(temp, float(i))
                        tf_lifetime.append(temp)
    return ti_lifetime, tf_lifetime, size_list


