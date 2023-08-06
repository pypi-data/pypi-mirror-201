import numpy as np
import matplotlib.pyplot as plt
from .read_file import read_file


def max_complex(FileName: str, FileNum: int, InitialTime: float, FinalTime: float,
                SpeciesName: str, ShowFig: bool = True, SaveFig: bool = False):
    file_name_head = FileName.split('.')[0]
    file_name_tail = FileName.split('.')[1]
    time_list = []
    size_list = []
    for k in range(1, FileNum+1):
        temp_file_name = file_name_head + '_' + str(k) + '.' + file_name_tail
        if FileNum == 1:
            temp_file_name = FileName
        total_size_list = []
        total_time_list = []
        hist = read_file(temp_file_name, SpeciesName)
        for i in hist:
            if InitialTime <= i[0] <= FinalTime:
                total_time_list.append(i[0])
                total_size_list.append(max(i[2]))
        time_list.append(total_time_list)
        size_list.append(total_size_list)
    size_list_rev = []
    for i in range(len(size_list[0])):
        temp = []
        for j in range(len(size_list)):
            temp.append(size_list[j][i])
        size_list_rev.append(temp)
    mean = []
    std = []
    for i in range(len(size_list_rev)):
        mean.append(np.mean(size_list_rev[i]))
        if FileNum > 1:
            std.append(np.std(size_list_rev[i]))
    if ShowFig:
        errorbar_color = '#c9e3f6'
        plt.plot(time_list[0], mean, color='C0')
        if FileNum > 1:
            plt.errorbar(time_list[0], mean, color='C0',
                         yerr=std, ecolor=errorbar_color)
        plt.title('Maximum Number of ' +
                  str(SpeciesName) + ' in Single Complex')
        plt.xlabel('Time (s)')
        plt.ylabel('Maximum Number of ' + str(SpeciesName))
        if SaveFig:
            plt.savefig('max_complex.png', dpi=500)
        plt.show()
    return time_list[0], mean, 'Nan', std


