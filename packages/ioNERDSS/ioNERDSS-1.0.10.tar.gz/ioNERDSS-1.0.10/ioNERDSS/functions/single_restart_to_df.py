from .PDB_pdb_to_df import PDB_pdb_to_df
from .RESTART_read_restart import RESTART_read_restart


def single_restart_to_df(FileNamePdb, ComplexSizeList, FileNameRestart='restart.dat', SerialNum=0):
    if SerialNum == -1:
        return 0, -1
    complex_list = RESTART_read_restart(FileNameRestart)
    index = 0
    protein_remain = []
    for i in range(len(ComplexSizeList)):
        for j in range(len(complex_list)):
            if len(complex_list[j]) == ComplexSizeList[i]:
                index += 1
                if SerialNum == index-1:
                    protein_remain = complex_list[j]
                    SerialNum += 1
                    complex_pdb_df = PDB_pdb_to_df(FileNamePdb, False)
                    complex_pdb_df = complex_pdb_df[complex_pdb_df['Cite_Name'] == 'COM']
                    complex_pdb_df = complex_pdb_df[complex_pdb_df['Protein_Num'].isin(
                        protein_remain)]
                    if 0 in complex_pdb_df.index:
                        complex_pdb_df = complex_pdb_df.drop(0)
                    return complex_pdb_df, SerialNum
    print('Cannot find more desired size of comolex!')
    return 0, -1


# Code written by Yian and modified bu Hugh
