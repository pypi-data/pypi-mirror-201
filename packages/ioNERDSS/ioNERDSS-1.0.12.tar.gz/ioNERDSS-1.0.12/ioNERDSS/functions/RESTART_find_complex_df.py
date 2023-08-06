def RESTART_find_complex_df(complex_df, num_lst, pdb_df):
    protein_name = []
    for i in range(len(pdb_df)):
        if pdb_df.loc[i, 'Protein_Name'] not in protein_name:
            protein_name.append(pdb_df.loc[i, 'Protein_Name'])
    complex_df['Num_List'] = ''
    for i in range(complex_df.shape[0]):
        lst = []
        for j in range(complex_df.shape[1]-2):
            lst.append(complex_df.iloc[i, j])
        complex_df.loc[i, 'Num_List'] = str(lst)
    num_lst_str = str(num_lst)
    protein_remain = []
    for i in range(complex_df.shape[0]):
        if complex_df.loc[i, 'Num_List'] == num_lst_str:
            string = complex_df.loc[i, 'Protein_Num']
            string = string.strip('[').strip(']').split(',')
            for i in string:
                protein_remain.append(int(i))
    return protein_remain


