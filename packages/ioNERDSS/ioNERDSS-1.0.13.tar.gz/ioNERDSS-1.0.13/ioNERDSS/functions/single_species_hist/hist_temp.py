from .read_file import read_file


def hist_temp(FileName: str, InitialTime: float, FinalTime: float, SpeciesName: str):
    """???

    Args:
        FileName (str): file location (relative) histogram.dat that will be read
        InitialTime (float): The starting time. Must not be smaller / larger then times in file.
        FinalTime (float): The ending time. Must not be smaller / larger then times in file.
        SpeciesName (str): The name of the species you want to examine. Should be in the .dat file.

    Returns:
        list of lists: ???
        list: a list of means for each ???
    """
    hist = read_file(FileName, SpeciesName)
    plot_count = []
    plot_conv = []
    tot = 0
    for i in hist:
        if InitialTime <= i[0] <= FinalTime:
            tot += 1
            for j in i[2]:
                if j not in plot_conv:
                    plot_conv.append(j)
                    plot_count.append(i[1][i[2].index(j)])
                else:
                    index = plot_conv.index(j)
                    plot_count[index] += i[1][i[2].index(j)]
    plot_count_mean = []
    for i in plot_count:
        plot_count_mean.append(i/tot)
    return plot_conv, plot_count_mean


