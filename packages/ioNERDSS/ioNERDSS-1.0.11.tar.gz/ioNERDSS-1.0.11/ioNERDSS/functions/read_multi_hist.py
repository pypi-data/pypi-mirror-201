import numpy as np


def read_multi_hist(FileName: str, SpeciesList: list):
    SpeciesList = np.array(SpeciesList)
    hist_list = []
    time_temp = []
    with open(FileName, 'r') as file:
        for line in file.readlines():
            if line[0:10] == 'Time (s): ':
                if float(line.split(' ')[-1].strip('\n')) != 0:
                    hist_list.append(time_temp)
                time_temp = []
                time_temp.append(float(line.split(' ')[-1].strip('\n')))
            else:
                complex_temp = np.zeros(len(SpeciesList) + 1)
                count = int(line.split('	')[0])
                info = line.strip('. \n').split('	')[1].split('. ')
                for i in range(len(info)):
                    name = str(info[i].split(': ')[0])
                    num = int(info[i].split(': ')[1])
                    index = np.where(SpeciesList == name)[0][0]
                    complex_temp[index] += num
                complex_temp[-1] += count
                time_temp.append(complex_temp)
        hist_list.append(time_temp)
    return hist_list


