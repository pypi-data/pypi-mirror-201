def PDB_find_complex(pdb_df, bond_lst):
    complex_lst = []
    for i in range(1, 1+pdb_df['Protein_Num'].max()):
        complex_temp = [i]
        j = 0
        while j < len(bond_lst):
            if bond_lst[j][0] in complex_temp and bond_lst[j][1] not in complex_temp:
                complex_temp.append(bond_lst[j][1])
                j = 0
            elif bond_lst[j][1] in complex_temp and bond_lst[j][0] not in complex_temp:
                complex_temp.append(bond_lst[j][0])
                j = 0
            else:
                j += 1
        complex_lst.append(complex_temp)
    for i in complex_lst:
        i.sort()
    complex_lst_ = []
    for i in complex_lst:
        if i not in complex_lst_:
            complex_lst_.append(i)
    return complex_lst_


