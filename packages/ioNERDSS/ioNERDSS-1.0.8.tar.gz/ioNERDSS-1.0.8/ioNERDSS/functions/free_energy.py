import math
import numpy as np
import matplotlib.pyplot as plt
import warnings
from .read_transition_matrix import read_transition_matrix


def free_energy(FileName: str, FileNum: int, InitialTime: float, FinalTime: float,
                SpeciesName: str, ShowFig: bool = True, SaveFig: bool = False):
    warnings.filterwarnings('ignore')
    matrix_list = []
    file_name_head = FileName.split('.')[0]
    file_name_tail = FileName.split('.')[1]
    for i in range(1, FileNum+1):
        temp_file_name = file_name_head + '_' + str(i) + '.' + file_name_tail
        if FileNum == 1:
            temp_file_name = FileName
        ti_matrix, tf_matrix = read_transition_matrix(
            temp_file_name, SpeciesName, InitialTime, FinalTime)
        matrix = tf_matrix - ti_matrix
        matrix_list.append(matrix)
    sum_list_list = []
    for k in range(len(matrix_list)):
        sum_list = np.zeros(len(matrix))
        i = 0
        while i < len(matrix_list[k]):
            j = 0
            while j < len(matrix_list[k][i]):
                if i == j:
                    sum_list[i] += matrix_list[k][i][j]
                elif i > j:
                    if i % 2 == 0:
                        if j <= (i-1)/2:
                            sum_list[i] += matrix_list[k][i][j]
                    else:
                        if j <= i/2:
                            if (i-1)/2 == j:
                                sum_list[i] += matrix_list[k][i][j]/2
                            else:
                                sum_list[i] += matrix_list[k][i][j]
                else:
                    if j % 2 != 0:
                        if i <= j/2:
                            if (j-1)/2 == i:
                                sum_list[i] += matrix_list[k][i][j]/2
                            else:
                                sum_list[i] += matrix_list[k][i][j]
                        else:
                            sum_list[i] += matrix_list[k][i][j]
                    else:
                        sum_list[i] += matrix_list[k][i][j]
                j += 1
            i += 1
        sum_list_list.append(sum_list)
    energy_list_list = []
    for i in range(len(sum_list_list)):
        sum_arr = np.array(sum_list_list[i])
        sum_arr = sum_arr/sum_arr.sum()
        energy_list = np.asarray([])
        for i in sum_arr:
            if i > 0:
                energy_list = np.append(energy_list, -math.log(i))
            else:
                energy_list = np.append(energy_list, np.nan)
        energy_list_list.append(energy_list)
    n_list = list(range(1, 1 + len(matrix_list[0])))
    energy_list_list_rev = []
    for i in range(len(energy_list_list[0])):
        temp = []
        for j in range(len(energy_list_list)):
            temp.append(energy_list_list[j][i])
        energy_list_list_rev.append(temp)
    mean_energy_list = np.array([])
    std_energy_list = np.array([])
    for i in energy_list_list_rev:
        mean_energy_list = np.append(mean_energy_list, np.nanmean(i))
        if FileNum != 1:
            std_energy_list = np.append(std_energy_list, np.nanstd(i))
    if ShowFig:
        errorbar_color = '#c9e3f6'
        plt.plot(n_list, mean_energy_list, 'C0')
        if FileNum != 1:
            plt.errorbar(n_list, mean_energy_list, yerr=std_energy_list,
                         ecolor=errorbar_color, capsize=2)
        plt.title('Free Energy')
        plt.xlabel('Number of ' + str(SpeciesName) + ' in Single Complex')
        plt.ylabel('-ln(p(N)) ($k_B$T)')
        plt.xticks(ticks=n_list)
        if SaveFig:
            plt.savefig('free_energy.png', dpi=500)
        plt.show()
    return n_list, mean_energy_list, 'Nan', std_energy_list


