import numpy as np
import matplotlib.pyplot as plt
import warnings
from .read_cluster_lifetime import read_cluster_lifetime


def complex_lifetime(FileName: str, FileNum: int, InitialTime: float, FinalTime: float,
                     SpeciesName: str, ShowFig: bool = True, SaveFig: bool = False):
    """
    This line plot indicates the lifetime for different sizes of complexes. The x-axis is the size of complexes, and the y-axis is the corresponding lifetime in unit of second. If multiple input files are given, the output plot will be the average value of all files and an error bar will also be included.

    Args:
        FileName (str): The path to the '.dat' file, which is usually named as 'transition_matrix_time.dat', representing the histogram data to be analyzed.
        FileNum (int): The number of the total input file. If multiple files are provided, their names should obey the naming rule listed below.
        InitialTime (float): The initial time that users desire to examine. The acceptable range should not be smaller than the starting time or exceed the ending time of simulation.
        FinalTime (float): The final time that users desire to examine. The acceptable range should not be smaller than the value of InitialTime or exceed the ending time of simulation.
        SpeciesName (str): The name of species that users want to examine, which should also be identical with the name written in the input (.inp and .mol) files.
        ShowFig (bool, optional): If True, the plot will be shown; if False, the plot will not be shown. No matter the plot is shown or not, the returns will remain the same. Defaults to True.
        SaveFig (bool, optional): If True, the plot will be saved as a '.png' file in the current directory; if False, the figure will not be saved. Defaults to False.

    Returns:
        A tuple containing the following:
        - np.ndarray: an array of the size of complexes
        - np.ndarray: an array of the dissociate probabilities when complexes dissociate into smaller complexes
        - np.ndarray: an array of the dissociate probabilities when complexes dissociate into larger complexes

    Notes:
        - If multiple input files are given, the output plot will be the average value of all files and an error bar will also be included.
        - For the dissociate reaction, only the complexes of smaller size dissociating from the original one is counted as dissociate event asymmetrically.
        - For example, if a heptamer dissociates into a tetramer and a trimer, then this event is counted only once, which is heptamer dissociates to trimer.
        - If a single file is provided, the input file should be named as its original name ('transition_matrix_time.dat').
        - If multiple files are provided, the name of the input file should also include serial number as 'transition_matrix_time_X.dat' where X = 1,2,3,4,5...
    """
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


