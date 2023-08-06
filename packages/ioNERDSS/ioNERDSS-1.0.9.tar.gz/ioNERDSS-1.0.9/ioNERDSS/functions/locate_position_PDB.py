from .PDB_pdb_to_df import PDB_pdb_to_df
from .PDB_dis_df_gen import PDB_dis_df_gen
from .PDB_bind_df_gen import PDB_bind_df_gen
from .PDB_find_bond import PDB_find_bond
from .PDB_find_complex import PDB_find_complex
from .PDB_complex_df_gen import PDB_complex_df_gen
from .PDB_find_complex_df import PDB_find_complex_df
from .PDB_new_pdb import PDB_new_pdb
from .PDB_binding_info_df import PDB_binding_info_df


def locate_position_PDB(FileNamePdb, NumList, FileNameInp, BufferRatio=0.01):
    print('Reading files......')
    pdb_df = PDB_pdb_to_df(FileNamePdb, True)
    print('Reading files complete!')
    print('Extracting binding information......')
    binding_info = PDB_binding_info_df(FileNameInp)
    print('Extracting complete!')
    print('Calculating distance......')
    dis_df = PDB_dis_df_gen(pdb_df, binding_info)
    print('Calculation complete!')
    print('Finding bonds......')
    bind_df = PDB_bind_df_gen(dis_df, BufferRatio)
    bond_lst = PDB_find_bond(bind_df)
    print('Finding bonds complete!')
    print('Finding complexes......')
    complex_lst = PDB_find_complex(pdb_df, bond_lst)
    complex_df = PDB_complex_df_gen(pdb_df, complex_lst)
    print('Finding complexes complete!')
    print('Writing new PDB files......')
    protein_remain = PDB_find_complex_df(complex_df, NumList, pdb_df)
    PDB_new_pdb(FileNamePdb, protein_remain)
    print('PDB writing complete!(named as output_file.pdb)')
    return 0


