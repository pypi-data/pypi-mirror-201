import pandas as pd
import os
from .single_hist_to_csv import single_hist_to_csv


def single_hist_to_df(FileName: str, SaveCsv: bool = True):
    single_hist_to_csv(FileName)
    df = pd.read_csv('histogram.csv')
    if not SaveCsv:
        os.remove('histogram.csv')
    return df


