import numpy as np
from coreframe import CoreFrame

def from_csv(path, dtimes_col):
    '''
    Returns the CoreFrame generated from the .csv file.

        Parameters:
            path (string): Path to .csv file
            dtimes_col (int): Index of column with datetime values

        Returns:
            CoreFrame generated from the .csv file in the path
    '''
    data = np.genfromtxt('data.csv', delimiter=',', dtype=None, encoding="utf8" )
    dtimes = data[1:, dtimes_col].astype(np.datetime64)
    np.delete(data, dtimes_col, axis = 1)
    col_names = data[0, :]
    data = data[1:, :].astype(float)
    return CoreFrame(data, dtimes, col_names=col_names)
