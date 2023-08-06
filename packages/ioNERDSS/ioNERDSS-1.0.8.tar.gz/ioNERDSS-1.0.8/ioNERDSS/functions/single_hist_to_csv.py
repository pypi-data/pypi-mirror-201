import numpy as np


def single_hist_to_csv(FileName: str):
    name_list = ['Time (s)']
    with open(FileName, 'r') as file:
        for line in file.readlines():
            if line[0:9] != 'Time (s):':
                name = line.split('	')[1].strip(' \n')
                name_num = int(line.split('	')[1].split(' ')[1].strip('.'))
                if name_list != ['Time (s)']:
                    last_num = int(name_list[-1].split(' ')[1].strip('.'))
                else:
                    last_num = 0
                if name not in name_list:
                    if name_num-last_num == 1:
                        name_list.append(name)
                    else:
                        fill = range(last_num+1, name_num)
                        for i in fill:
                            name = str(line.split('	')[1].split(
                                ' ')[0]) + ' ' + str(i) + '.'
                            name_list.append(name)
    file.close()
    with open(FileName, 'r') as read_file, open('histogram.csv', 'w') as write_file:
        head = ''
        for i in name_list:
            head += i
            if i != name_list[-1]:
                head += ','
            else:
                head += '\n'
        write_file.write(head)
        stat = np.zeros(len(name_list))
        for line in read_file.readlines():
            if line[0:9] == 'Time (s):':
                if line != 'Time (s): 0\n':
                    write_line = ''
                    for i in range(len(stat)):
                        write_line += str(stat[i])
                        if i != len(stat)-1:
                            write_line += ','
                        else:
                            write_line += '\n'
                    write_file.write(write_line)
                stat = np.zeros(len(name_list))
                write_line = ''
                info = float(line.split(' ')[-1])
                stat[0] += info
            else:
                name = line.split('	')[-1].strip(' \n')
                num = float(line.split('	')[0])
                index = name_list.index(name)
                stat[index] += num
        for i in range(len(stat)):
            write_line += str(stat[i])
            if i != len(stat)-1:
                write_line += ','
            else:
                write_line += '\n'
        write_file.write(write_line)
    read_file.close()
    write_file.close()
    return 0


