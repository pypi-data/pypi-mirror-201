import pandas as pd
import os
from .multi_hist_to_csv import multi_hist_to_csv


def multi_hist_to_df(FileName: str, SaveCsv: bool = True):
    multi_hist_to_csv(FileName)
    df = pd.read_csv('histogram.csv')
    if not SaveCsv:
        os.remove('histogram.csv')
    return df


