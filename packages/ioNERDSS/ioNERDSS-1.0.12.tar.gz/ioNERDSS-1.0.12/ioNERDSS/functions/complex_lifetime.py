import numpy as np
import matplotlib.pyplot as plt
import warnings
from .read_cluster_lifetime import read_cluster_lifetime


def complex_lifetime(FileName: str, FileNum: int, InitialTime: float, FinalTime: float,
                     SpeciesName: str, ShowFig: bool = True, SaveFig: bool = False):
    warnings.filterwarnings('ignore')
    file_name_head = FileName.split('.')[0]
    file_name_tail = FileName.split('.')[1]
    mean_lifetime = []
    for i in range(1, FileNum+1):
        temp_file_name = file_name_head + '_' + str(i) + '.' + file_name_tail
        if FileNum == 1:
            temp_file_name = FileName
        ti_lifetime, tf_lifetime, size_list = read_cluster_lifetime(
            temp_file_name, SpeciesName, InitialTime, FinalTime)
        mean_temp = []
        for i in range(len(tf_lifetime)):
            tf_lifetime[i] = np.delete(
                tf_lifetime[i], range(0, len(ti_lifetime[i])), axis=0)
            mean_temp.append(tf_lifetime[i].mean())
        mean_lifetime.append(mean_temp)
    mean_lifetime_rev = []
    for i in range(len(mean_lifetime[0])):
        temp = []
        for j in range(len(mean_lifetime)):
            temp.append(mean_lifetime[j][i])
        mean_lifetime_rev.append(temp)
    mean = []
    std = []
    for i in mean_lifetime_rev:
        mean.append(np.nanmean(i))
        if FileNum != 1:
            std.append(np.nanstd(i))
    if ShowFig:
        errorbar_color = '#c9e3f6'
        plt.plot(size_list, mean, color='C0')
        if FileNum != 1:
            plt.errorbar(size_list, mean, yerr=std,
                         ecolor=errorbar_color, capsize=2)
        plt.xlabel('Number of ' + str(SpeciesName) + ' in Single Complex')
        plt.ylabel('Lifetime (s)')
        plt.xticks(ticks=size_list)
        plt.title('Lifetime of Complex')
        if SaveFig:
            plt.savefig('complex_lifetime.png', dpi=500)
        plt.show()
    return size_list, mean, 'Nan', std


