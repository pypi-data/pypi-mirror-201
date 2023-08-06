import pandas as pd


def PDB_bind_df_gen(dis_df, buffer_ratio):
    bind_df = pd.DataFrame(columns=['Protein_Num_1', 'Protein_Name_1', 'Cite_Name_1',
                           'Protein_Num_2', 'Protein_Name_2', 'Cite_Name_2', 'sigma', 'dis'])
    index = 0
    for i in range(len(dis_df)):
        if dis_df.loc[i, 'dis'] >= dis_df.loc[i, 'sigma']*(1-buffer_ratio):
            if dis_df.loc[i, 'dis'] <= dis_df.loc[i, 'sigma']*(1+buffer_ratio):
                bind_df.loc[index] = dis_df.loc[i]
                index += 1
    return bind_df


