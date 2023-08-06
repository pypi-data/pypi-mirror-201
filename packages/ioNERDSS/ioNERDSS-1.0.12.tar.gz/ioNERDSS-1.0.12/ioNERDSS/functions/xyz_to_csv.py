def xyz_to_csv(FileName: str, LitNum: int):
    if LitNum != -1:
        lit_switch = False
        write_file_name = 'trajectory_' + str(LitNum) + '.csv'
    else:
        lit_switch = True
        write_file_name = 'trajectory_full.csv'
    with open(FileName, 'r') as read_file, open(write_file_name, 'w') as write_file:
        head = 'literation,name,x,y,z\n'
        write_file.write(head)
        for line in read_file.readlines():
            if LitNum != -1:
                if line[0:11] == 'iteration: ':
                    if int(line.split(' ')[1]) == LitNum:
                        lit_switch = True
                    else:
                        lit_switch = False
                    literation = LitNum
            else:
                if line[0:11] == 'iteration: ':
                    literation = int(line.split(' ')[1])

            if lit_switch:
                if len(line.strip(' ').strip('\n').split()) == 4:
                    info = line.strip(' ').strip('\n').split()
                    write_info = str(literation) + ','
                    for i in range(len(info)):
                        write_info += info[i]
                        if i != len(info)-1:
                            write_info += ','
                        else:
                            write_info += '\n'
                    write_file.write(write_info)
    return 0


