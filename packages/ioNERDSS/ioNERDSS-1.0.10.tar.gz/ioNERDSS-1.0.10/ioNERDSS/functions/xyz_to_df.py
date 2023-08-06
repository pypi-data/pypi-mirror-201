import pandas as pd
import os
from .xyz_to_csv import xyz_to_csv


def xyz_to_df(FileName: str, LitNum: int, SaveCsv: bool = True):
    xyz_to_csv(FileName, LitNum)
    if LitNum != -1:
        write_file_name = 'trajectory_' + str(LitNum) + '.csv'
    else:
        write_file_name = 'trajectory_full.csv'
    df = pd.read_csv(write_file_name)
    if not SaveCsv:
        os.remove(write_file_name)
    return df


