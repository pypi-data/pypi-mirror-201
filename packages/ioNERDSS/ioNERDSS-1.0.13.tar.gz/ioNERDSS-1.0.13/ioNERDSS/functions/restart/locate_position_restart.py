from .RESTART_read_restart import RESTART_read_restart
from .RESTART_pdb_to_df import RESTART_pdb_to_df
from .RESTART_complex_df_gen import RESTART_complex_df_gen
from .RESTART_find_complex_df import RESTART_find_complex_df
from .RESTART_new_pdb import RESTART_new_pdb


def locate_position_restart(FileNamePdb, NumList, FileNameRestart='restart.dat'):
    print('Reading restart.dat......')
    complex_lst = RESTART_read_restart(FileNameRestart)
    print('Reading files complete!')
    print('Reading PDB files......')
    pdb_df = RESTART_pdb_to_df(FileNamePdb)
    print('Reading files complete!')
    print('Finding complexes......')
    complex_df = RESTART_complex_df_gen(pdb_df, complex_lst)
    print('Finding complexes complete!')
    print('Writing new PDB files......')
    protein_remain = RESTART_find_complex_df(complex_df, NumList, pdb_df)
    RESTART_new_pdb(FileNamePdb, protein_remain)
    print('PDB writing complete!(named as output_file.pdb)')
    return 0


