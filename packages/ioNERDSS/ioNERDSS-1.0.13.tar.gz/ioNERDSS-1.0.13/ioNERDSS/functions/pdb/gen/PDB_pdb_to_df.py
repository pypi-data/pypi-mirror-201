def PDB_pdb_to_df(file_name, drop_COM):
    df = pd.DataFrame(columns=['Protein_Num', 'Protein_Name',
                      'Cite_Name', 'x_coord', 'y_coord', 'z_coord'])
    with open(file_name, 'r') as file:
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
                df.loc[index, 'Cite_Name'] = info[2]
                df.loc[index, 'x_coord'] = float(info[5])
                df.loc[index, 'y_coord'] = float(info[6])
                df.loc[index, 'z_coord'] = float(info[7])
            index += 1
        df = df.dropna()
        if drop_COM:
            df = df.drop(index=df[(df.Cite_Name == 'COM')].index.tolist())
        df = df.reset_index(drop=True)
    return df


