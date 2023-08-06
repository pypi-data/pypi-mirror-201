import pandas as pd
import os
from .single_hist_to_csv import single_hist_to_csv


def single_hist_to_df(FileName: str, SaveCsv: bool = True):
    """Creates a pandas dataframe from a histogram.dat (single-species)

    Args:
        FileName (str): Path to the histogram.dat file
        SaveCsv (bool, optional): If a .csv file is saved as well. Defaults to True.

    Returns:
       pandas.df: Each row is a different time stamp (all times listed in column A). Each column is a different size of complex molecule (all sizes listed in row 1). Each box 
        is the number of that complex molecule at that time stamp.
    """
    single_hist_to_csv(FileName)
    df = pd.read_csv('histogram.csv')
    if not SaveCsv:
        os.remove('histogram.csv')
    return df


