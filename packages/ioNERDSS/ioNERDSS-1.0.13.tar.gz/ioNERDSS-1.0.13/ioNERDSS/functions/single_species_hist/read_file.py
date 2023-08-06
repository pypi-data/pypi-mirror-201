def read_file(FileName: str, SpeciesName: str):
    """Will take in a histogram.dat (single-species) and turn it into a list of lists

    Args:
        FileName (str): Path to the histogram.dat file
        SpeciesName (str): The name of the specific species you want to examine. Should be in the .dat file.

    Returns:
        list of lists: Has many lists, where each sub-list is a new time stamp that includes time at index 0, and all other (???) info after 
    """
    hist = []
    hist_temp = []
    hist_conv = []
    hist_count = []
    with open(FileName, 'r') as file:
        for line in file.readlines():
            if line[0:4] == 'Time':
                if hist_count != [] and hist_conv != []:
                    hist_temp.append(hist_count)
                    hist_temp.append(hist_conv)
                    hist.append(hist_temp)
                hist_count = []
                hist_conv = []
                hist_temp = []
                hist_temp.append(float(line.strip('Time (s): ')))
            else:
                string = '	' + str(SpeciesName) + ': '
                line = line.strip('. \n').split(string)
                if len(line) != 2:
                    print('Wrong species name!')
                    return 0
                else:
                    hist_count.append(int(line[0]))
                    hist_conv.append(int(line[1]))
            if len(hist_temp) == 0:
                hist_temp.append(hist_count)
                hist_temp.append(hist_conv)
                hist.append(hist_temp)
    hist_temp.append(hist_count)
    hist_temp.append(hist_conv)
    hist.append(hist_temp)
    return hist


