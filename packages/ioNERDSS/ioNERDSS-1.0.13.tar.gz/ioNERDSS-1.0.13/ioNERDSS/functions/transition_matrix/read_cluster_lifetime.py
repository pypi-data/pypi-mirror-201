import numpy as np


def read_cluster_lifetime(FileName: str, SpeciesName: str, InitialTime: float, FinalTime: float):
    """
    Reads and extracts the lifetimes of clusters of a specific species from a transition_matrix_time.dat file.

    Args:
        FileName (str): The name of the file to read the cluster lifetimes from.
        SpeciesName (str): The name of the species to extract cluster lifetimes for.
        InitialTime (float): The initial time at which to extract cluster lifetimes.
        FinalTime (float): The final time at which to extract cluster lifetimes.

    Returns:
        A tuple containing three elements:
        - A list of numpy arrays representing the lifetimes of the species clusters
        at the initial time.
        - A list of numpy arrays representing the lifetimes of the species clusters
        at the final time.
        - A list of integers representing the sizes of the species clusters.
    """
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


