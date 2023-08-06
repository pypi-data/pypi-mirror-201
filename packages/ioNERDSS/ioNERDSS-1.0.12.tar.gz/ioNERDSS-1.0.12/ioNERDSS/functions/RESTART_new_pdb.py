def RESTART_new_pdb(file_name_pdb, protein_remain):
    with open(file_name_pdb, 'r') as file:
        write_lst = []
        for line in file.readlines():
            line_ = line.split(' ')
            if line_[0] == 'TITLE':
                write_lst.append(line)
            elif line_[0] == 'CRYST1':
                write_lst.append(line)
            elif line_[0] == 'ATOM':
                info = []
                for i in line_:
                    i.strip('\n')
                    if i != '':
                        info.append(i)
                info[9] = info[9].strip('\n')
                if int(info[4]) in protein_remain:
                    write_lst.append(line)
    with open('output_file.pdb', 'w') as file_:
        file_.seek(0)
        file_.truncate()
        for i in write_lst:
            file_.writelines(i)
    return 0


