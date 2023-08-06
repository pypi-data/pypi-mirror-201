import numpy as np
import matplotlib.pyplot as plt
import warnings
from .hist_temp import hist_temp


def hist_3d_time(FileName: str, FileNum: int, InitialTime: float, FinalTime: float,
                 SpeciesName: str, TimeBins: int, xBarSize: int = 1, ShowFig: bool = True, SaveFig: bool = False):
    warnings.filterwarnings('ignore')
    t_arr = np.arange(InitialTime, FinalTime, (FinalTime-InitialTime)/TimeBins)
    t_arr = np.append(t_arr, FinalTime)
    file_name_head = FileName.split('.')[0]
    file_name_tail = FileName.split('.')[1]
    z_list_tot = []
    x_list_tot = []
    for p in range(1, FileNum+1):
        temp_file_name = file_name_head + '_' + str(p) + '.' + file_name_tail
        if FileNum == 1:
            temp_file_name = FileName
        max_num = 0
        x_lst = []
        z_lst = []
        t_plt = np.zeros(TimeBins)
        i = 0
        for i in range(0, len(t_arr)-1):
            t_plt[i] = (t_arr[i]+t_arr[i+1])/2
            x, z = hist_temp(temp_file_name, t_arr[i], t_arr[i+1], SpeciesName)
            x_lst.append(x)
            z_lst.append(z)
            if max(x) > max_num:
                max_num = max(x)
        z_plt = np.zeros(shape=(max_num, TimeBins))
        k = 0
        for i in x_lst:
            l = 0
            for j in i:
                z_plt[j-1, k] = z_lst[k][l]
                l += 1
            k += 1
        z_plt = z_plt.T
        z_plt_ = []
        for i in range(len(z_plt)):
            z_plt_temp = []
            x_count = 0
            sum_ = 0.0
            for j in range(len(z_plt[i])):
                x_count += 1
                sum_ += z_plt[i][j]
                if j == len(z_plt) - 1:
                    z_plt_temp.append(sum_)
                    x_count = 0
                    sum_ = 0
                elif x_count == xBarSize:
                    z_plt_temp.append(sum_)
                    x_count = 0
                    sum_ = 0
            z_plt_.append(z_plt_temp)
        z_plt_ = np.array(z_plt_)
        x_plt = np.arange(0, max_num, xBarSize)+1
        x_list_tot.append(x_plt)
        z_list_tot.append(list(z_plt_))
    max_x_num = 0
    for i in range(len(x_list_tot)):
        if len(x_list_tot[i]) > max_x_num:
            max_x_num = len(x_list_tot[i])
            n_list = x_list_tot[i]
    for i in range(len(z_list_tot)):
        for j in range(len(z_list_tot[i])):
            if len(z_list_tot[i][j]) < len(n_list):
                for k in range(0, 1 + len(n_list) - len(z_list_tot[i][j])):
                    z_list_tot[i][j] = np.append(z_list_tot[i][j], 0.0)
    count_list_mean = np.zeros([TimeBins, len(n_list)])
    for i in range(len(z_list_tot[0])):
        for j in range(len(z_list_tot[0][0])):
            temp_list = []
            for k in range(len(z_list_tot)):
                temp_list.append(z_list_tot[k][i][j])
            count_list_mean[i][j] += np.mean(temp_list)
    if ShowFig:
        xx, yy = np.meshgrid(n_list, t_plt)
        X, Y = xx.ravel(), yy.ravel()
        Z = np.array(count_list_mean.ravel())
        bottom = np.zeros_like(Z)
        width = xBarSize
        depth = 1/TimeBins
        fig = plt.figure()
        ax = fig.add_subplot(2,2,1,projection="3d")
        ax.bar3d(X, Y, bottom, width, depth, Z, shade=True)
        ax.set_xlabel('Number of ' + SpeciesName + ' in sigle complex')
        ax.set_ylabel('Time (s)')
        ax.set_zlabel('Count')
        if SaveFig:
            plt.savefig('histogram_3D.png', dpi=500)
        plt.show()
    return n_list, t_plt, count_list_mean, 'Nan'


