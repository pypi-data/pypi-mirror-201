import numpy as np
import matplotlib.pyplot as plt
from .read_multi_hist import read_multi_hist


def multi_hist_stacked(FileName: str, FileNum: int, InitialTime: float, FinalTime: float,
                       SpeciesList: list, xAxis: str, DivideSpecies: str, DivideSize: int,
                       BarSize: int = 1, ExcludeSize: int = 0, ShowFig: bool = True, SaveFig: bool = False):
    file_name_head = FileName.split('.')[0]
    file_name_tail = FileName.split('.')[1]
    above_list = []
    equal_list = []
    below_list = []
    size_list = []
    for i in range(1, FileNum+1):
        temp_file_name = file_name_head + '_' + str(i) + '.' + file_name_tail
        if FileNum == 1:
            temp_file_name = FileName
        total_size_list = []
        total_above_list = []
        total_equal_list = []
        total_below_list = []
        hist_list = read_multi_hist(temp_file_name, SpeciesList)
        data_count = 0
        for j in range(len(hist_list)):
            if hist_list[j] != []:
                time = hist_list[j][0]
                if InitialTime <= time <= FinalTime:
                    data_count += 1
                    for k in range(len(hist_list[j])):
                        if k != 0:
                            if xAxis == 'tot' and DivideSpecies in SpeciesList:
                                total_size = sum(hist_list[j][k][0:-1])
                                divide_index = SpeciesList.index(DivideSpecies)
                                divide_spe_size = hist_list[j][k][divide_index]
                                if total_size >= ExcludeSize:
                                    if total_size not in total_size_list:
                                        total_size_list.append(total_size)
                                        if divide_spe_size > DivideSize:
                                            total_above_list.append(
                                                hist_list[j][k][-1])
                                            total_equal_list.append(0.0)
                                            total_below_list.append(0.0)
                                        elif divide_spe_size == DivideSize:
                                            total_equal_list.append(
                                                hist_list[j][k][-1])
                                            total_above_list.append(0.0)
                                            total_below_list.append(0.0)
                                        else:
                                            total_below_list.append(
                                                hist_list[j][k][-1])
                                            total_above_list.append(0.0)
                                            total_equal_list.append(0.0)
                                    else:
                                        if divide_spe_size > DivideSize:
                                            index = total_size_list.index(
                                                total_size)
                                            total_above_list[index] += hist_list[j][k][-1]
                                        elif divide_spe_size == DivideSize:
                                            index = total_size_list.index(
                                                total_size)
                                            total_equal_list[index] += hist_list[j][k][-1]
                                        else:
                                            index = total_size_list.index(
                                                total_size)
                                            total_below_list[index] += hist_list[j][k][-1]
                            elif xAxis in SpeciesList and DivideSpecies in SpeciesList:
                                name_index = SpeciesList.index(xAxis)
                                total_size = hist_list[j][k][name_index]
                                divide_index = SpeciesList.index(DivideSpecies)
                                divide_spe_size = hist_list[j][k][divide_index]
                                if total_size >= ExcludeSize:
                                    if total_size not in total_size_list:
                                        total_size_list.append(total_size)
                                        if divide_spe_size > DivideSize:
                                            total_above_list.append(
                                                hist_list[j][k][-1])
                                            total_equal_list.append(0.0)
                                            total_below_list.append(0.0)
                                        elif divide_spe_size == DivideSize:
                                            total_equal_list.append(
                                                hist_list[j][k][-1])
                                            total_above_list.append(0.0)
                                            total_below_list.append(0.0)
                                        else:
                                            total_below_list.append(
                                                hist_list[j][k][-1])
                                            total_above_list.append(0.0)
                                            total_equal_list.append(0.0)
                                    else:
                                        if divide_spe_size > DivideSize:
                                            index = total_size_list.index(
                                                total_size)
                                            total_above_list[index] += hist_list[j][k][-1]
                                        elif divide_spe_size == DivideSize:
                                            index = total_size_list.index(
                                                total_size)
                                            total_equal_list[index] += hist_list[j][k][-1]
                                        else:
                                            index = total_size_list.index(
                                                total_size)
                                            total_below_list[index] += hist_list[j][k][-1]
                            else:
                                print('xAxis or DivideSpecies not in SpeciesList!')
                                return 0
        total_above_list = np.array(total_above_list)/data_count
        total_equal_list = np.array(total_equal_list)/data_count
        total_below_list = np.array(total_below_list)/data_count
        if len(total_size_list) != 0:
            total_size_list_sorted = np.arange(1, max(total_size_list)+1, 1)
        else:
            total_size_list_sorted = np.array([])
        total_above_list_sorted = []
        for i in total_size_list_sorted:
            if i in total_size_list:
                index = total_size_list.index(i)
                total_above_list_sorted.append(total_above_list[index])
            else:
                total_above_list_sorted.append(0.0)
        total_equal_list_sorted = []
        for i in total_size_list_sorted:
            if i in total_size_list:
                index = total_size_list.index(i)
                total_equal_list_sorted.append(total_equal_list[index])
            else:
                total_equal_list_sorted.append(0.0)
        total_below_list_sorted = []
        for i in total_size_list_sorted:
            if i in total_size_list:
                index = total_size_list.index(i)
                total_below_list_sorted.append(total_below_list[index])
            else:
                total_below_list_sorted.append(0.0)
        size_list.append(total_size_list_sorted)
        above_list.append(total_above_list_sorted)
        equal_list.append(total_equal_list_sorted)
        below_list.append(total_below_list_sorted)
    max_size = 0
    for i in size_list:
        if max_size < len(i):
            max_size = len(i)
            n_list = i
    above_list_filled = np.zeros([FileNum, max_size])
    above_list_arr = np.array([])
    for i in range(len(above_list)):
        for j in range(len(above_list[i])):
            above_list_filled[i][j] += above_list[i][j]
    equal_list_filled = np.zeros([FileNum, max_size])
    equal_list_arr = np.array([])
    for i in range(len(equal_list)):
        for j in range(len(equal_list[i])):
            equal_list_filled[i][j] += equal_list[i][j]
    below_list_filled = np.zeros([FileNum, max_size])
    below_list_arr = np.array([])
    for i in range(len(below_list)):
        for j in range(len(below_list[i])):
            below_list_filled[i][j] += below_list[i][j]
    above_list_rev = []
    for i in range(len(above_list_filled[0])):
        temp = []
        for j in range(len(above_list_filled)):
            temp.append(above_list_filled[j][i])
        above_list_rev.append(temp)
    equal_list_rev = []
    for i in range(len(equal_list_filled[0])):
        temp = []
        for j in range(len(equal_list_filled)):
            temp.append(equal_list_filled[j][i])
        equal_list_rev.append(temp)
    below_list_rev = []
    for i in range(len(below_list_filled[0])):
        temp = []
        for j in range(len(below_list_filled)):
            temp.append(below_list_filled[j][i])
        below_list_rev.append(temp)
    mean_above = []
    std_above = []
    mean_equal = []
    std_equal = []
    mean_below = []
    std_below = []
    for i in above_list_rev:
        mean_above.append(np.nanmean(i))
        std_above.append(np.nanstd(i))
    for i in equal_list_rev:
        mean_equal.append(np.nanmean(i))
        std_equal.append(np.nanstd(i))
    for i in below_list_rev:
        mean_below.append(np.nanmean(i))
        std_below.append(np.nanstd(i))
    mean_above_ = []
    mean_equal_ = []
    mean_below_ = []
    std_above_ = []
    std_equal_ = []
    std_below_ = []
    n_list_ = []
    temp_mean_above = 0
    temp_mean_equal = 0
    temp_mean_below = 0
    temp_std_above = 0
    temp_std_equal = 0
    temp_std_below = 0
    bar_size_count = 0
    for i in range(len(mean_above)):
        temp_mean_above += mean_above[i]
        temp_mean_equal += mean_equal[i]
        temp_mean_below += mean_below[i]
        temp_std_above += std_above[i]
        temp_std_equal += std_equal[i]
        temp_std_below += std_below[i]
        bar_size_count += 1
        if i+1 == len(mean_above):
            mean_above_.append(temp_mean_above)
            mean_equal_.append(temp_mean_equal)
            mean_below_.append(temp_mean_below)
            std_above_.append(temp_std_above)
            std_equal_.append(temp_std_equal)
            std_below_.append(temp_std_below)
            n_list_.append(n_list[i])
        elif bar_size_count >= BarSize:
            mean_above_.append(temp_mean_above)
            mean_equal_.append(temp_mean_equal)
            mean_below_.append(temp_mean_below)
            std_above_.append(temp_std_above)
            std_equal_.append(temp_std_equal)
            std_below_.append(temp_std_below)
            n_list_.append(n_list[i])
            temp_mean_above = 0
            temp_mean_equal = 0
            temp_mean_below = 0
            temp_std_above = 0
            temp_std_equal = 0
            temp_std_below = 0
            bar_size_count = 0
    mean_above_ = np.array(mean_above_)
    mean_equal_ = np.array(mean_equal_)
    mean_below_ = np.array(mean_below_)
    std_above_ = np.array(std_above_)
    std_equal_ = np.array(std_equal_)
    std_below_ = np.array(std_below_)
    n_list_ = np.array(n_list_)
    if ShowFig:
        if DivideSize != 0:
            below_label = DivideSpecies + '<' + str(DivideSize)
            equal_label = DivideSpecies + '=' + str(DivideSize)
            above_label = DivideSpecies + '>' + str(DivideSize)
        else:
            above_label = 'With ' + DivideSpecies
            equal_label = 'Without ' + DivideSpecies
        if FileNum != 1:
            if DivideSize != 0:
                plt.bar(n_list_, mean_below_, width=BarSize, color='C0',
                        yerr=std_below_, label=below_label, ecolor='C3', capsize=2)
            plt.bar(n_list_, mean_equal_, width=BarSize, color='C1', yerr=std_equal_,
                    bottom=mean_below_, label=equal_label, ecolor='C3', capsize=2)
            plt.bar(n_list_, mean_above_, width=BarSize, color='C2', yerr=std_above_,
                    bottom=mean_below_+mean_equal_, label=above_label, ecolor='C3', capsize=2)
        else:
            if DivideSize != 0:
                plt.bar(n_list_, mean_below_, width=BarSize,
                        color='C0', label=below_label, capsize=2)
            plt.bar(n_list_, mean_equal_, width=BarSize, color='C1',
                    bottom=mean_below_, label=equal_label, capsize=2)
            plt.bar(n_list_, mean_above_, width=BarSize, color='C2',
                    bottom=mean_below_+mean_equal_, label=above_label, capsize=2)
        if xAxis == 'tot':
            x_label_name = 'total monomers'
        else:
            x_label_name = xAxis
        plt.xlabel('Number of ' + x_label_name + ' in sigle complex')
        plt.ylabel('Count')
        plt.legend()
        plt.title('Histogram of Multi-component Assemblies')
        fig_name = 'stacked_histogram_of_' + xAxis + '_divided_by_' + DivideSpecies
        if SaveFig:
            plt.savefig(fig_name, dpi=500)
        plt.show()
    return n_list_, [mean_below_, mean_equal_, mean_above_], 'Nan', [std_below_, std_equal_, std_above_]


