import math
import copy
from .real_PDB_mag import real_PDB_mag


def real_PDB_separate_sigma(Result: tuple, ChangeSigma: bool = False, SiteList: list = [], NewSigma: list = []):

    reaction_chain, int_site, int_site_distance, unique_chain, COM = Result
    # user can choose to change the interaction site
    new_int_site_distance = copy.deepcopy(int_site_distance)
    new_int_site = copy.deepcopy(int_site)
    if ChangeSigma:
        for i in range(len(SiteList)):
            n = SiteList[i] - 1
            new_distance = NewSigma[i]
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
                        # print("New interaction site of " + reaction_chain[p][0] + " & " + reaction_chain[p][
                        #     1] + " is: "
                        #     + "[%.3f, %.3f, %.3f]" % (
                        #     new_int_site[p][0][0], new_int_site[p][0][1], new_int_site[p][0][2]) + " and "
                        #     + "[%.3f, %.3f, %.3f]" % (
                        #     new_int_site[p][1][0], new_int_site[p][1][1], new_int_site[p][1][2])
                        #     + " distance between interaction sites is: %.3f" % (new_int_site_distance[p]))
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

                    new_int_site[n] = copy.deepcopy(inner_new_position)
                    new_int_site_distance[n] = math.sqrt((new_int_site[n][0][0] - new_int_site[n][1][0]) ** 2
                                                         + (new_int_site[n][0][1] - new_int_site[n][1][1]) ** 2
                                                         + (new_int_site[n][0][2] - new_int_site[n][1][2]) ** 2)
                    # print("New interaction site of " + reaction_chain[n][0] + " & " + reaction_chain[n][1] + " is: "
                    #     + "[%.3f, %.3f, %.3f]" % (
                    #         new_int_site[n][0][0], new_int_site[n][0][1], new_int_site[n][0][2]) + " and "
                    #     + "[%.3f, %.3f, %.3f]" % (
                    #     new_int_site[n][1][0], new_int_site[n][1][1], new_int_site[n][1][2])
                    #     + " distance between interaction sites is: %.3f" % (new_int_site_distance[n]) + ' nm')

        for i in range(len(new_int_site)):
            print("New interaction site of " + reaction_chain[i][0] + " & " + reaction_chain[i][1] + " is: "
                  + "[%.3f, %.3f, %.3f]" % (new_int_site[i][0][0],
                                            new_int_site[i][0][1], new_int_site[i][0][2]) + " and "
                  + "[%.3f, %.3f, %.3f]" % (new_int_site[i][1][0],
                                            new_int_site[i][1][1], new_int_site[i][1][2])
                  + " distance between new interaction sites is: %.3f nm" % (new_int_site_distance[i]))

        return reaction_chain, new_int_site, new_int_site_distance, unique_chain, COM

    else:
        return Result


