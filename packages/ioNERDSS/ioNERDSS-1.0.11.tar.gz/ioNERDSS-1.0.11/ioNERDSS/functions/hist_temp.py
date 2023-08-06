from .read_file import read_file


def hist_temp(FileName: str, InitialTime: float, FinalTime: float, SpeciesName: str):
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


