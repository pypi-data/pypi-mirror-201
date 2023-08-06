import numpy as np
from .real_PDB_angles import real_PDB_angles
from .real_PDB_norm_check import real_PDB_norm_check


def real_PDB_separate_angle(Result: tuple):
    reaction_chain, new_int_site, new_int_site_distance, unique_chain, COM = Result
    angle = []
    normal_point_lst1 = []
    normal_point_lst2 = []
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
    return reaction_chain, new_int_site, new_int_site_distance, unique_chain, COM, angle, normal_point_lst1, normal_point_lst2, one_site_chain


