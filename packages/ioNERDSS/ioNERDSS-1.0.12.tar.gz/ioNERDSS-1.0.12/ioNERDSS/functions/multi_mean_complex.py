import numpy as np
import matplotlib.pyplot as plt
from .hist import hist
from .read_multi_hist import read_multi_hist
from .multi_hist import multi_hist


def multi_mean_complex(FileName: str, FileNum: int, InitialTime: float, FinalTime: float,
                       SpeciesList: list, SpeciesName: str, ExcludeSize: int = 0, ShowFig: bool = True, SaveFig: bool = False):

    file_name_head = FileName.split('.')[0]
    file_name_tail = FileName.split('.')[1]
    time_list = []
    size_list = []
    for i in range(1, FileNum+1):
        temp_file_name = file_name_head + '_' + str(i) + '.' + file_name_tail
        if FileNum == 1:
            temp_file_name = FileName
        total_size_list = []
        total_time_list = []
        hist_list = read_multi_hist(temp_file_name, SpeciesList=SpeciesList)
        data_count = 0
        for j in range(len(hist_list)):
            if hist_list[j] != []:
                time = hist_list[j][0]
                if InitialTime <= time <= FinalTime:
                    total_time_list.append(time)
                    temp_sum = 0
                    count = 0
                    for k in range(len(hist_list[j])):
                        if k != 0:
                            if SpeciesName == 'tot':
                                total_size = sum(hist_list[j][k][0:-1])
                            elif SpeciesName in SpeciesList:
                                name_index = SpeciesList.index(SpeciesName)
                                total_size = hist_list[j][k][name_index]
                            else:
                                print('SpeciesName not in SpeciesList!')
                                return 0

                            if total_size >= ExcludeSize:
                                count += hist_list[j][k][-1]
                                temp_sum += total_size * hist_list[j][k][-1]
                    if count != 0:
                        total_size_list.append(temp_sum/count)
                    else:
                        total_size_list.append(0.0)
        size_list.append(total_size_list)
        time_list.append(total_time_list)
    size_list_rev = []
    for i in range(len(size_list[0])):
        temp = []
        for j in range(len(size_list)):
            temp.append(size_list[j][i])
        size_list_rev.append(temp)
    mean = []
    std = []
    for i in size_list_rev:
        mean.append(np.nanmean(i))
        std.append(np.nanstd(i))
    mean = np.array(mean)
    std = np.array(std)
    if ShowFig:
        errorbar_color = '#c9e3f6'
        plt.plot(time_list[0], mean, color='C0')
        if FileNum > 1:
            plt.errorbar(time_list[0], mean, color='C0',
                         yerr=std, ecolor=errorbar_color)
        if SpeciesName == 'tot':
            title_spec = 'Total Species'
        else:
            title_spec = SpeciesName
        plt.title('Maximum Number of ' +
                  str(title_spec) + ' in Single Complex')
        plt.xlabel('Time (s)')
        plt.ylabel('Maximum Number of ' + str(title_spec))
        if SaveFig:
            plt.savefig('multi_max_complex.png', dpi=500)
        plt.show()
    return time_list[0], mean, 'Nan', std


