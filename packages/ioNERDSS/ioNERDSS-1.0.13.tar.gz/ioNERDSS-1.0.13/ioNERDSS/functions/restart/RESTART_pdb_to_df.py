def RESTART_pdb_to_df(file_name_pdb):
    df = pd.DataFrame(columns=['Protein_Num', 'Protein_Name'])
    with open(file_name_pdb, 'r') as file:
        index = 0
        for line in file.readlines():
            line = line.split(' ')
            if line[0] == 'ATOM':
                info = []
                for i in line:
                    if i != '':
                        info.append(i)
                df.loc[index, 'Protein_Num'] = int(info[4])
                df.loc[index, 'Protein_Name'] = info[3]
            index += 1
        df = df.dropna()
        df = df.reset_index(drop=True)
    return df


