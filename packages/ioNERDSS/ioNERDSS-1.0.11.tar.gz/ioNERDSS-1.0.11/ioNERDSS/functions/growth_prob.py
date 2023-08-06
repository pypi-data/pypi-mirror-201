import numpy as np
import matplotlib.pyplot as plt
import warnings
from .read_transition_matrix import read_transition_matrix


def growth_prob(FileName: str, FileNum: int, InitialTime: float, FinalTime: float,
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
    growth_list_list = []
    tot_list_list = []
    for k in range(len(matrix_list)):
        growth_list = []
        tot_list = []
        i = 0
        while i < len(matrix_list[k][0]):
            j = 0
            growth_sum = 0
            tot_sum = 0
            while j < len(matrix_list[k][i]):
                if i != j:
                    tot_sum += matrix_list[k][j][i]
                    if i < j:
                        growth_sum += matrix_list[k][j][i]
                j += 1
            growth_list.append(growth_sum)
            tot_list.append(tot_sum)
            i += 1
        growth_list_list.append(growth_list)
        tot_list_list.append(tot_list)
    growth_prob = []
    for i in range(len(growth_list_list)):
        growth_prob_temp = []
        for j in range(len(growth_list_list[i])):
            if tot_list_list[i][j] != 0:
                growth_prob_temp.append(
                    growth_list_list[i][j]/tot_list_list[i][j])
            else:
                growth_prob_temp.append(0.0)
        growth_prob.append(growth_prob_temp)
    growth_prob_rev = []
    for i in range(len(growth_prob[0])):
        temp = []
        for j in range(len(growth_prob)):
            temp.append(growth_prob[j][i])
        growth_prob_rev.append(temp)
    mean = []
    std = []
    for i in growth_prob_rev:
        mean.append(np.nanmean(i))
        std.append(np.nanstd(i))
    n_list = list(range(1, 1 + len(matrix_list[0])))
    if ShowFig:
        errorbar_color = '#c9e3f6'
        plt.plot(n_list, mean, color='C0')
        if FileNum != 1:
            plt.errorbar(n_list, mean, yerr=std,
                         ecolor=errorbar_color, capsize=2)
        plt.axhline(y=1/2, c='black', lw=1.0)
        plt.xlabel('Number of ' + str(SpeciesName) + ' in Single Complex')
        plt.ylabel('$P_{growth}$')
        plt.xticks(ticks=n_list)
        plt.yticks((0, 0.25, 0.5, 0.75, 1))
        plt.title('Growth Probability')
        if SaveFig:
            plt.savefig('growth_probability.png', dpi=500)
        plt.show()
    return n_list, mean, 'Nan', std


