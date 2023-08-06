import numpy as np
import matplotlib.pyplot as plt
from .read_multi_hist import read_multi_hist


def multi_hist(FileName: str, FileNum: int, InitialTime: float, FinalTime: float,
               SpeciesList: list, xAxis: str, BarSize: int = 1, ExcludeSize: int = 0,
               ShowFig: bool = True, SaveFig: bool = False):
    file_name_head = FileName.split('.')[0]
    file_name_tail = FileName.split('.')[1]
    count_list = []
    size_list = []
    for i in range(1, FileNum+1):
        temp_file_name = file_name_head + '_' + str(i) + '.' + file_name_tail
        if FileNum == 1:
            temp_file_name = FileName
        total_size_list = []
        total_count_list = []
        hist_list = read_multi_hist(temp_file_name, SpeciesList=SpeciesList)
        data_count = 0
        for j in range(len(hist_list)):
            if hist_list[j] != []:
                time = hist_list[j][0]
                if InitialTime <= time <= FinalTime:
                    data_count += 1
                    for k in range(len(hist_list[j])):
                        if k != 0:
                            if xAxis == 'tot':
                                total_size = sum(hist_list[j][k][0:-1])
                                if total_size >= ExcludeSize:
                                    if total_size not in total_size_list:
                                        total_size_list.append(total_size)
                                        total_count_list.append(
                                            hist_list[j][k][-1])
                                    else:
                                        index = total_size_list.index(
                                            total_size)
                                        total_count_list[index] += hist_list[j][k][-1]
                            elif xAxis in SpeciesList:
                                name_index = SpeciesList.index(xAxis)
                                total_size = hist_list[j][k][name_index]
                                if total_size >= ExcludeSize:
                                    if total_size not in total_size_list:
                                        total_size_list.append(total_size)
                                        total_count_list.append(
                                            hist_list[j][k][-1])
                                    else:
                                        index = total_size_list.index(
                                            total_size)
                                        total_count_list[index] += hist_list[j][k][-1]
                            else:
                                print('xAxis not in SpeciesList!')
                                return 0
        total_count_list = np.array(total_count_list)/data_count
        if len(total_size_list) != 0:
            total_size_list_sorted = np.arange(1, max(total_size_list)+1, 1)
        else:
            total_size_list_sorted = np.array([])
        total_count_list_sorted = []
        for i in total_size_list_sorted:
            if i in total_size_list:
                index = total_size_list.index(i)
                total_count_list_sorted.append(total_count_list[index])
            else:
                total_count_list_sorted.append(0.0)
        size_list.append(total_size_list_sorted)
        count_list.append(total_count_list_sorted)
    max_size = 0
    for i in size_list:
        if max_size < len(i):
            max_size = len(i)
            n_list = i
    count_list_filled = np.zeros([FileNum, max_size])
    count_list_arr = np.array([])
    for i in range(len(count_list)):
        for j in range(len(count_list[i])):
            count_list_filled[i][j] += count_list[i][j]
    count_list_rev = []
    for i in range(len(count_list_filled[0])):
        temp = []
        for j in range(len(count_list_filled)):
            temp.append(count_list_filled[j][i])
        count_list_rev.append(temp)
    mean = []
    std = []
    for i in count_list_rev:
        mean.append(np.nanmean(i))
        std.append(np.nanstd(i))
    mean_ = []
    std_ = []
    n_list_ = []
    temp_mean = 0
    temp_std = 0
    bar_size_count = 0
    for i in range(len(mean)):
        temp_mean += mean[i]
        temp_std += std[i]
        bar_size_count += 1
        if i+1 == len(mean):
            mean_.append(temp_mean)
            std_.append(temp_std)
            n_list_.append(n_list[i])
        elif bar_size_count >= BarSize:
            mean_.append(temp_mean)
            std_.append(temp_std)
            n_list_.append(n_list[i])
            temp_mean = 0
            temp_std = 0
            bar_size_count = 0
    mean_ = np.array(mean_)
    std_ = np.array(std_)
    n_list_ = np.array(n_list_)
    if ShowFig:
        if FileNum != 1:
            plt.bar(n_list_, mean_, width=BarSize, color='C0',
                    yerr=std_, ecolor='C1', capsize=2)
        else:
            plt.bar(n_list_, mean_, width=BarSize)
        if xAxis == 'tot':
            label_name = 'total monomers'
        else:
            label_name = xAxis
        plt.xlabel('Number of ' + label_name + ' in sigle complex (count)')
        plt.ylabel('Count')
        plt.title('Histogram of Multi-component Assemblies')
        fig_species = xAxis
        if xAxis == 'tot':
            fig_species = 'total_components'
        fig_name = 'histogram_of_' + fig_species
        if SaveFig:
            plt.savefig(fig_name, dpi=500)
        plt.show()
    return n_list_, mean_, 'Nan', std_


