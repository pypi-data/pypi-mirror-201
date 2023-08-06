import math
import numpy as np
import sys
import copy
from .gen.real_PDB_data_check import real_PDB_data_check
from .gen.real_PDB_chain_int import real_PDB_chain_int
from .gen.real_PDB_angles import real_PDB_angles
from .gen.real_PDB_norm_check import real_PDB_norm_check
from .gen.real_PDB_norm_input import real_PDB_norm_input
from .gen.real_PDB_mag import real_PDB_mag


def real_PDB_UI():
    """A user friendly UI to allow for open, minupulating, and then outputting .pdb files.

    Functions:
    
    Open .pdb files:
     - When run, the first thing that will be asked is "Enter pdb file name: []". You must enter the relative / absolute path to the file.
     - Ex: Enter pdb file name: "ioNERDSSPyPi\TestingFunctions\\1si4.pdb" (Note: I have to '\' before 1, so python does not see it as a weird charecter)
    Chaning distance between interaction sites:
     - After the .pdb file in initilized, it will ask "Would you like to chang...", and ask for you to write 'yes' or 'no'
     - If you write yes, keep reading, if you write no, it will just go to the next section
     - Than it will ask 'which distance' you want to change, and ask for an integer between 0-X. 
        - 0: means all distances will be set to the same number you input
        - 1+: That distance will be set to the number inputted. You can find which 'distance' each number refers to by reading and counting down the 
        list of Interaction Sites (which is directly above). 1 = the furthest up.
     - Then enter the new distance.
     - Then the initial message will come up again, and repeats this whol process.
    'Normalizing':
     - It will then ask if you want to see the 'default norm vector to (0,0,1)'. Write 'yes' or 'no' if you do or don't
     - It will then ask if you want each molecule's center of mass to be 0,0,0
     - The UI will then spit out the necessary .mol and .inp files to setup a NERDSS simulation

    If you want to make graphs / new .pdb files, you will need to use the 'seperate' commands instead of the UI.
    """
    # naming explanation:
    # variables with word 'total' in the front indicate that it's a list of data for the whole protein
    # variables with word 'split' in the front indicate that it's a list containing n sub-lists and each sub-list contains
    # data for different chains. (n is the number of chains)

    # indicating number of atoms: if there are 5 atoms, then the list looks like [1,2,3,4,5]
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
    with open(input("Enter pdb file name: "), "r") as filename:
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

    # user can choose to change the interaction site
    new_int_site_distance = copy.deepcopy(int_site_distance)
    new_int_site = copy.deepcopy(int_site)

    while True:
        answer = input(
            "Would you like to change the distance between interaction site (Type 'yes' or 'no'): ")
        if answer == "no":
            print("Calculation is completed.")
            break
        if answer == "yes":
            while True:
                n = int(input("Which distance would you like to change (please enter an integer no greater than %.0f or enter 0 to set all distance to a specific number): " % (
                    len(int_site_distance)))) - 1
                if n in range(-1, len(int_site_distance)):
                    while True:
                        new_distance = float(
                            input("Please enter new distance: "))
                        # decreasing distance & increasing distance
                        if new_distance >= 0:
                            if n == -1:
                                for p in range(0, len(reaction_chain)):
                                    new_int_site_distance[p] = copy.deepcopy(
                                        new_distance)
                                    dir_vec1 = (
                                        int_site[p][0][0] -
                                        int_site[p][1][0], int_site[p][0][1] -
                                        int_site[p][1][1],
                                        int_site[p][0][2] - int_site[p][1][2])
                                    dir_vec2 = (
                                        int_site[p][1][0] -
                                        int_site[p][0][0], int_site[p][1][1] -
                                        int_site[p][0][1],
                                        int_site[p][1][2] - int_site[p][0][2])
                                    unit_dir_vec1 = [dir_vec1[0] / real_PDB_mag(dir_vec1), dir_vec1[1] / real_PDB_mag(dir_vec1),
                                                     dir_vec1[2] / real_PDB_mag(dir_vec1)]
                                    unit_dir_vec2 = [dir_vec2[0] / real_PDB_mag(dir_vec2), dir_vec2[1] / real_PDB_mag(dir_vec2),
                                                     dir_vec2[2] / real_PDB_mag(dir_vec2)]

                                    inner_new_position = []
                                    new_coord1 = []
                                    new_coord2 = []
                                    for i in range(3):
                                        new_coord1.append(
                                            (new_distance - int_site_distance[p]) / 2 * unit_dir_vec1[i] + int_site[p][0][
                                                i])
                                        new_coord2.append(
                                            (new_distance - int_site_distance[p]) / 2 * unit_dir_vec2[i] + int_site[p][1][
                                                i])
                                    inner_new_position.append(new_coord1)
                                    inner_new_position.append(new_coord2)

                                    new_int_site[p] = copy.deepcopy(
                                        inner_new_position)
                                    new_int_site_distance[p] = math.sqrt(
                                        (new_int_site[p][0][0] -
                                         new_int_site[p][1][0]) ** 2
                                        + (new_int_site[p][0][1] -
                                           new_int_site[p][1][1]) ** 2
                                        + (new_int_site[p][0][2] - new_int_site[p][1][2]) ** 2)
                                    print("New interaction site of " + reaction_chain[p][0] + " & " + reaction_chain[p][
                                        1] + " is: "
                                        + "[%.3f, %.3f, %.3f]" % (
                                        new_int_site[p][0][0], new_int_site[p][0][1], new_int_site[p][0][2]) + " and "
                                        + "[%.3f, %.3f, %.3f]" % (
                                        new_int_site[p][1][0], new_int_site[p][1][1], new_int_site[p][1][2])
                                        + " distance between interaction sites is: %.3f" % (new_int_site_distance[p]))
                                break
                            if n >= 0:
                                new_int_site_distance[n] = copy.deepcopy(
                                    new_distance)
                                dir_vec1 = (int_site[n][0][0] - int_site[n][1][0], int_site[n][0]
                                            [1] - int_site[n][1][1], int_site[n][0][2] - int_site[n][1][2])
                                dir_vec2 = (int_site[n][1][0] - int_site[n][0][0], int_site[n][1]
                                            [1] - int_site[n][0][1], int_site[n][1][2] - int_site[n][0][2])
                                unit_dir_vec1 = [
                                    dir_vec1[0] / real_PDB_mag(dir_vec1), dir_vec1[1] / real_PDB_mag(dir_vec1), dir_vec1[2] / real_PDB_mag(dir_vec1)]
                                unit_dir_vec2 = [
                                    dir_vec2[0] / real_PDB_mag(dir_vec2), dir_vec2[1] / real_PDB_mag(dir_vec2), dir_vec2[2] / real_PDB_mag(dir_vec2)]

                                inner_new_position = []
                                new_coord1 = []
                                new_coord2 = []
                                for i in range(3):
                                    new_coord1.append(
                                        (new_distance - int_site_distance[n]) / 2 * unit_dir_vec1[i] + int_site[n][0][i])
                                    new_coord2.append(
                                        (new_distance - int_site_distance[n]) / 2 * unit_dir_vec2[i] + int_site[n][1][i])
                                inner_new_position.append(new_coord1)
                                inner_new_position.append(new_coord2)

                                new_int_site[n] = copy.deepcopy(
                                    inner_new_position)
                                new_int_site_distance[n] = math.sqrt((new_int_site[n][0][0] - new_int_site[n][1][0]) ** 2
                                                                     + (new_int_site[n][0][1] - new_int_site[n][1][1]) ** 2
                                                                     + (new_int_site[n][0][2] - new_int_site[n][1][2]) ** 2)
                                print("New interaction site of " + reaction_chain[n][0] + " & " + reaction_chain[n][1] + " is: "
                                      + "[%.3f, %.3f, %.3f]" % (
                                        new_int_site[n][0][0], new_int_site[n][0][1], new_int_site[n][0][2]) + " and "
                                      + "[%.3f, %.3f, %.3f]" % (
                                    new_int_site[n][1][0], new_int_site[n][1][1], new_int_site[n][1][2])
                                    + " distance between interaction sites is: %.3f" % (new_int_site_distance[n]))
                                break
                        else:
                            print('Invalid number, please try again.')
                            break
                    break
                else:
                    print("Invalid answer, please try again.")
                    break
        else:
            print("Invalid answer, please try again.")

    # ditermine sigma
    # calculating angles
    angle = []
    normal_point_lst1 = []
    normal_point_lst2 = []

    while True:
        answer_norm = str(
            input("Would you like to use the default norm vector (0,0,1)? (Type 'yes' or 'no'): "))
        if answer_norm == 'yes' or answer_norm == 'no':
            break

    # type in norm
    if answer_norm == 'no':
        for i in range(len(reaction_chain)):
            chain1 = 0
            chain2 = 0
            for j in range(len(unique_chain)):
                if reaction_chain[i][0] == unique_chain[j]:
                    chain1 = j
                if reaction_chain[i][1] == unique_chain[j]:
                    chain2 = j
                if reaction_chain[i][0] == unique_chain[chain1] and reaction_chain[i][1] == unique_chain[chain2]:
                    break
            while True:
                normal_point_lst1 = real_PDB_norm_input(normal_point_lst1, str(
                    unique_chain[chain1]), str(unique_chain[chain1]), str(unique_chain[chain2]))
                if real_PDB_norm_check(normal_point_lst1[-1], COM[chain1], new_int_site[i][0]) == False:
                    break
                else:
                    normal_point_lst1.remove(normal_point_lst1[-1])
                    print(
                        'Wrong input, please try again! (Wrong input format or n colinear with COM-to-site vector)')
            while True:
                normal_point_lst2 = real_PDB_norm_input(normal_point_lst2, str(
                    unique_chain[chain2]), str(unique_chain[chain1]), str(unique_chain[chain2]))
                if real_PDB_norm_check(normal_point_lst2[-1], COM[chain2], new_int_site[i][1]) == False:
                    break
                else:
                    normal_point_lst2.remove(normal_point_lst2[-1])
                    print(
                        'Wrong input, please try again! (Wrong input format or n colinear with COM-to-site vector)')
            inner_angle = real_PDB_angles(COM[chain1], COM[chain2], new_int_site[i][0], new_int_site[i][1], np.array(
                COM[chain1]) + np.array(normal_point_lst1[-1]), np.array(COM[chain2]) + np.array(normal_point_lst2[-1]))
            angle.append([inner_angle[0], inner_angle[1], inner_angle[2],
                          inner_angle[3], inner_angle[4], inner_angle[5]])
            print("Angles for chain " +
                  str(unique_chain[chain1]) + " & " + str(unique_chain[chain2]))
            print("Theta1: %.3f, Theta2: %.3f, Phi1: %.3f, Phi2: %.3f, Omega: %.3f" % (
                inner_angle[0], inner_angle[1], inner_angle[2], inner_angle[3], inner_angle[4]))

    # generate norm
    if answer_norm == 'yes':
        for i in range(len(reaction_chain)):
            chain1 = 0
            chain2 = 0
            for j in range(len(unique_chain)):
                if reaction_chain[i][0] == unique_chain[j]:
                    chain1 = j
                if reaction_chain[i][1] == unique_chain[j]:
                    chain2 = j
                if reaction_chain[i][0] == unique_chain[chain1] and reaction_chain[i][1] == unique_chain[chain2]:
                    break
            while True:
                normal_point_lst1.append([0., 0., 1.])
                if real_PDB_norm_check(normal_point_lst1[-1], COM[chain1], new_int_site[i][0]) == False:
                    break
                else:
                    normal_point_lst1.remove(normal_point_lst1[-1])
                    normal_point_lst1.append([0., 1., 0.])

            while True:
                normal_point_lst2.append([0., 0., 1.])
                if real_PDB_norm_check(normal_point_lst2[-1], COM[chain2], new_int_site[i][1]) == False:
                    break
                else:
                    normal_point_lst2.remove(normal_point_lst2[-1])
                    normal_point_lst2.append([0., 1., 0.])

            inner_angle = real_PDB_angles(COM[chain1], COM[chain2], new_int_site[i][0], new_int_site[i][1], np.array(
                COM[chain1]) + np.array(normal_point_lst1[-1]), np.array(COM[chain2]) + np.array(normal_point_lst2[-1]))
            angle.append([inner_angle[0], inner_angle[1], inner_angle[2],
                          inner_angle[3], inner_angle[4], inner_angle[5]])
            print("Angles for chain " +
                  str(unique_chain[chain1]) + " & " + str(unique_chain[chain2]))
            print("Theta1: %.3f, Theta2: %.3f, Phi1: %.3f, Phi2: %.3f, Omega: %.3f" % (
                inner_angle[0], inner_angle[1], inner_angle[2], inner_angle[3], inner_angle[4]))

    # looking for chains possess only 1 inferface.
    reaction_chain_1d = []
    one_site_chain = []
    for i in reaction_chain:
        for j in i:
            reaction_chain_1d.append(j)
    for i in unique_chain:
        if reaction_chain_1d.count(i) == 1:
            one_site_chain.append(i)

    # asking whether to center the COM of every chain to origin.
    while True:
        answer2 = input(
            "Do you want each chain to be centered at center of mass? (Type 'yes' or 'no'): ")
        if answer2 == "yes":
            for i in range(len(unique_chain)):
                for k in range(len(reaction_chain)):
                    for j in range(2):
                        if unique_chain[i] == reaction_chain[k][j]:
                            for l in range(3):
                                new_int_site[k][j][l] = new_int_site[k][j][l] - COM[i][l]
                                # angle[k][j+6][l] = angle[k][j+6][l] - COM[i][l]
                for m in range(3):
                    COM[i][m] = 0.0
            break
        if answer2 == "no":
            break
        else:
            print("Invalid answer, please try again.")

    # writing parameters into a file

    f = open("parm.inp", "w")
    f.write(" # Input file\n\n")
    f.write("start parameters\n")
    f.write("    nItr = 1000000\n")
    f.write("    timestep = 0.1\n\n\n")
    f.write("    timeWrite = 500\n")
    f.write("    trajWrite = 500\n")
    f.write("    pdbWrite = 500\n")
    f.write("    restartWrite = 50000\n")
    f.write("    fromRestart = false\n")
    f.write("end parameters\n\n")
    f.write("start boundaries\n")
    f.write("    WaterBox = [494,494,494] #nm\n")
    f.write("    implicitLipid = false\n")
    f.write("    xBCtype = reflect\n")
    f.write("    yBCtype = reflect\n")
    f.write("    zBCtype = reflect\n")
    f.write("end boundaries\n\n")
    f.write("start molecules\n")
    for i in range(len(unique_chain)):
        f.write("     %s:100\n" % (unique_chain[i]))
    f.write("end molecules\n\n")
    f.write("start reactions\n")
    for i in range(len(reaction_chain)):
        molecule1_lower = reaction_chain[i][0].lower()
        molecule2_lower = reaction_chain[i][1].lower()
        f.write("    #### %s - %s ####\n" %
                (reaction_chain[i][0], reaction_chain[i][1]))
        f.write("    %s(%s) + %s(%s) <-> %s(%s!1).%s(%s!1)\n" % (reaction_chain[i][0], molecule2_lower,
                                                                 reaction_chain[i][1], molecule1_lower,
                                                                 reaction_chain[i][0], molecule2_lower,
                                                                 reaction_chain[i][1], molecule1_lower))
        f.write("    onRate3Dka = 10\n")
        f.write("    offRatekb = 1\n")
        f.write("    sigma = %f\n" % angle[i][5])
        f.write("    norm1 = [%.6f,%.6f,%.6f]\n" % (
            normal_point_lst1[i][0], normal_point_lst1[i][1], normal_point_lst1[i][2]))
        f.write("    norm2 = [%.6f,%.6f,%.6f]\n" % (
            normal_point_lst2[i][0], normal_point_lst2[i][1], normal_point_lst2[i][2]))
        if reaction_chain[i][0] in one_site_chain:
            angle[i][2] = 'nan'
        if reaction_chain[i][1] in one_site_chain:
            angle[i][3] = 'nan'
        f.write("    assocAngles = [" + str(angle[i][0]) + "," + str(angle[i][1]) + "," + str(
            angle[i][2]) + "," + str(angle[i][3]) + "," + str(angle[i][4]) + "\n\n")
    f.write("end reactions")
    f.close()

    for i in range(len(unique_chain)):
        mol_file = str(unique_chain[i]) + '.mol'
        f = open(mol_file, "w")
        f.write("##\n# %s molecule information file\n##\n\n" % unique_chain[i])
        f.write("Name    = %s\n" % unique_chain[i])
        f.write("checkOverlap = true\n\n")
        f.write("# translational diffusion constants\n")
        f.write("D       = [12.0,12.0,12.0]\n\n")
        f.write("# rotational diffusion constants\n")
        f.write("Dr      = [0.5,0.5,0.5]\n\n")
        f.write("# Coordinates, with states below, or\n")
        f.write("COM     %.4f    %.4f    %.4f\n" %
                (COM[i][0], COM[i][1], COM[i][2]))
        reaction_chain_merged = []
        chain_string = []
        bond_counter = 0
        for a in range(len(reaction_chain)):
            for b in range(2):
                reaction_chain_merged.append(reaction_chain[a][b])
        if unique_chain[i] not in reaction_chain_merged:
            break
        if unique_chain[i] in reaction_chain_merged:
            bond_counter = 0
            for m in range(len(reaction_chain)):
                if unique_chain[i] == reaction_chain[m][0]:
                    bond_counter += 1
                    chain_name = str(reaction_chain[m][1])
                    chain_string.append(chain_name.lower())
                    f.write("%s       %.4f    %.4f    %.4f\n" % (chain_name.lower(
                    ), new_int_site[m][0][0], new_int_site[m][0][1], new_int_site[m][0][2]))
                elif unique_chain[i] == reaction_chain[m][1]:
                    bond_counter += 1
                    chain_name = str(reaction_chain[m][0])
                    f.write("%s       %.4f    %.4f    %.4f\n" % (chain_name.lower(
                    ), new_int_site[m][1][0], new_int_site[m][1][1], new_int_site[m][1][2]))
                    chain_string.append(chain_name)
        f.write("\nbonds = %d\n" % bond_counter)
        for j in range(bond_counter):
            f.write("COM %s\n" % chain_string[j])
    return 0

# --------------------------------------Seperated functions (same as above)----------------------------------------


