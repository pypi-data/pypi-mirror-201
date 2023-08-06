import math
import sys
from .real_PDB_data_check import real_PDB_data_check
from .real_PDB_chain_int import real_PDB_chain_int


def real_PDB_separate_read(FileName: str):
    total_atom_count = []
    # specific chain the atom belongs to (such as A or B or C, etc).
    total_chain = []
    total_resi_count = []  # residue number
    total_position = []  # the coordinate of each atom
    total_atom_type = []  # to show whether the atom is a alpha carbon, N, etc.
    total_resi_type = []  # to show the type of residue
    # indicate the position of alpha carbon of the residue the atom is in.
    total_resi_position_every_atom = []
    total_resi_position = []  # list of position of all alpha carbon atom position
    total_alphaC_resi_count = []  # indicate which residue the alphaC belongs to
    # The length of last two lists are the same as total residue numbers in the chain and the length of rest of the lists
    # are the same as total atom numbers in the protein.
    # read in user pdb file
    # out data into corresponding lists
    with open(FileName, "r") as filename:
        for line in filename:
            data = line.split()  # split a line into list
            id = data[0]
            if id == 'ENDMDL':
                break
            if id == 'ATOM':  # find all 'atom' lines
                if real_PDB_data_check(data) == 1:
                    pass
                elif real_PDB_data_check(data) == -2:
                    data[3] = data[3].lstrip(data[3][0])
                elif real_PDB_data_check(data) == -1:
                    amino_name = data[2][-3:]
                    data.insert(3, amino_name)
                    data[2] = data[2].rstrip(amino_name)

                total_atom_count.append(data[1])
                total_chain.append(data[4])
                total_resi_count.append(data[5])
                total_atom_type.append(data[2])
                total_resi_type.append(data[3])
                # change all strings into floats for position values, also converting to nm from angstroms
                position_coords = []
                for i in range(3):
                    position_coords.append(float(data[6+i])/10)
                total_position.append(position_coords)
                if data[2] == "CA":
                    total_resi_position.append(position_coords)
                    total_alphaC_resi_count.append(data[5])
    print('Finish reading pdb file')

    # create total_resi_position_every_atom list
    count = 0
    for i in range(len(total_alphaC_resi_count)):
        if count >= len(total_atom_type):
            break
        for j in range(count, len(total_atom_type)):
            if total_resi_count[j] == total_alphaC_resi_count[i]:
                total_resi_position_every_atom.append(total_resi_position[i])
                count = count + 1
            else:
                break

    # determine how many unique chains exist
    unique_chain = []
    for letter in total_chain:
        if letter not in unique_chain:
            unique_chain.append(letter)
    print(str(len(unique_chain)) + ' chain(s) in total: ' + str(unique_chain))

    # exit if there's only one chain.
    if len(unique_chain) == 1:
        sys.exit()

    # create lists of lists where each sublist contains the data for different chains.
    split_atom_count = []
    split_chain = []
    split_resi_count = []
    split_position = []
    split_atom_type = []
    split_resi_type = []
    chain_end_atom = []
    split_resi_position_every_atom = []

    # inner lists are sublists of each list, each of the sublist represents data about a list
    inner_atom_count = []
    inner_chain = []
    inner_resi_count = []
    inner_position = []
    inner_atom_type = []
    inner_resi_type = []
    inner_resi_position_every_atom = []

    # determine number of atoms in each chain
    chain_counter = 0

    for i in range(len(total_atom_count)):

        if total_chain[i] != unique_chain[chain_counter]:
            split_atom_count.append(inner_atom_count)
            split_chain.append(inner_chain)
            split_resi_count.append(inner_resi_count)
            split_position.append(inner_position)
            split_atom_type.append(inner_atom_type)
            split_resi_type.append(inner_resi_type)
            split_resi_position_every_atom.append(
                inner_resi_position_every_atom)
            inner_atom_count = []
            inner_chain = []
            inner_resi_count = []
            inner_position = []
            inner_atom_type = []
            inner_resi_type = []
            inner_resi_position_every_atom = []
            chain_end_atom.append(len(split_atom_count[chain_counter]))
            chain_counter = chain_counter + 1

        if total_chain[i] == unique_chain[chain_counter]:
            inner_atom_count.append(total_atom_count[i])
            inner_chain.append(total_chain[i])
            inner_resi_count.append(total_resi_count[i])
            inner_position.append(total_position[i])
            inner_atom_type.append(total_atom_type[i])
            inner_resi_type.append(total_resi_type[i])
            inner_resi_position_every_atom.append(
                total_resi_position_every_atom[i])

        if i == (len(total_atom_count) - 1):
            split_atom_count.append(inner_atom_count)
            split_chain.append(inner_chain)
            split_resi_count.append(inner_resi_count)
            split_position.append(inner_position)
            split_atom_type.append(inner_atom_type)
            split_resi_type.append(inner_resi_type)
            split_resi_position_every_atom.append(
                inner_resi_position_every_atom)
            chain_end_atom.append(len(split_atom_count[chain_counter]))

    print('Each of them has ' + str(chain_end_atom) + ' atoms.')

    # determine the interaction between each two chains by using function chain_int()
    # the output is a tuple with 7 list of list including: reaction_chain, reaction_atom, reaction_atom_position,
    # reaction_atom_distance, reaction_resi_count, reaction_resi_type and  reaction_atom_type

    interaction = real_PDB_chain_int(unique_chain, split_position, split_resi_count, split_atom_count,
                                     split_resi_type, split_atom_type, split_resi_position_every_atom)
    reaction_chain = interaction[0]
    reaction_atom = interaction[1]
    reaction_atom_position = interaction[2]
    reaction_atom_distance = interaction[3]
    reaction_resi_count = interaction[4]
    reaction_resi_type = interaction[5]
    reaction_atom_type = interaction[6]
    reaction_resi_position = interaction[7]

    # calculating center of mass (COM) and interaction site

    # COM
    COM = []
    for i in range(len(split_position)):
        sumx = 0
        sumy = 0
        sumz = 0
        for j in range(len(split_position[i])):
            sumx = sumx + split_position[i][j][0]
            sumy = sumy + split_position[i][j][1]
            sumz = sumz + split_position[i][j][2]
        inner_COM = [sumx / len(split_position[i]), sumy /
                     len(split_position[i]), sumz / len(split_position[i])]
        COM.append(inner_COM)

    for i in range(len(COM)):
        print("Center of mass of  " + unique_chain[i] + " is: " +
              "[%.3f, %.3f, %.3f]" % (COM[i][0], COM[i][1], COM[i][2]))

    # int_site
    int_site = []
    two_chain_int_site = []

    for i in range(len(reaction_resi_position)):
        for j in range(0, 2):
            sumx = 0
            sumy = 0
            sumz = 0
            count = 0
            added_position = []
            for k in range(len(reaction_resi_position[i])):
                if reaction_resi_position[i][k][j] not in added_position:
                    sumx = sumx + reaction_resi_position[i][k][j][0]
                    sumy = sumy + reaction_resi_position[i][k][j][1]
                    sumz = sumz + reaction_resi_position[i][k][j][2]
                    added_position.append(reaction_resi_position[i][k][j])
                    count = count + 1
            inner_int_site = [sumx / count, sumy / count, sumz / count]
            two_chain_int_site.append(inner_int_site)
        int_site.append(two_chain_int_site)
        two_chain_int_site = []

    # calculate distance between interaction site.
    int_site_distance = []
    for i in range(len(int_site)):
        distance = math.sqrt((int_site[i][0][0] - int_site[i][1][0]) ** 2 + (int_site[i][0][1] - int_site[i][1][1]) ** 2
                             + (int_site[i][0][2] - int_site[i][1][2]) ** 2)
        int_site_distance.append(distance)

    for i in range(len(int_site)):
        print("Interaction site of " + reaction_chain[i][0] + " & " + reaction_chain[i][1] + " is: "
              + "[%.3f, %.3f, %.3f]" % (int_site[i][0][0],
                                        int_site[i][0][1], int_site[i][0][2]) + " and "
              + "[%.3f, %.3f, %.3f]" % (int_site[i][1][0],
                                        int_site[i][1][1], int_site[i][1][2])
              + " distance between interaction sites is: %.3f nm" % (int_site_distance[i]))

    return reaction_chain, int_site, int_site_distance, unique_chain, COM


