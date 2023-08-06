def PDB_find_bond(bind_df):
    bond_lst = []
    for i in range(len(bind_df)):
        bond_lst.append([int(bind_df.loc[i, 'Protein_Num_1']),
                        int(bind_df.loc[i, 'Protein_Num_2'])])
    for i in bond_lst:
        i.sort()
    bond_lst_ = []
    for i in bond_lst:
        if i not in bond_lst_:
            bond_lst_.append(i)
    return bond_lst_


