from .RESTART_read_restart import RESTART_read_restart
from .RESTART_new_pdb import RESTART_new_pdb


def single_locate_position_restart(FileNamePdb, ComplexSize, FileNameRestart='restart.dat'):
    print('Reading restart.dat...')
    complex_lst = RESTART_read_restart(FileNameRestart)
    print('Reading files complete!')
    protein_remain = []
    for i in complex_lst:
        if len(i) == ComplexSize:
            protein_remain.append(i)
    protein_remain_flat = []
    for i in protein_remain:
        for j in i:
            protein_remain_flat.append(j)
    RESTART_new_pdb(FileNamePdb, protein_remain_flat)
    print('PDB writing complete!(named as output_file.pdb)')
    return 0


# ---------------------------Reading Real PDB File and Generating NERDSS inputs-----------------------------------
# function for checking format of data in readlines
