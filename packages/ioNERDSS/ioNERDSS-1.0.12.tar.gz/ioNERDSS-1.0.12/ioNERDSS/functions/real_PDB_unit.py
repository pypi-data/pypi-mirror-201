import numpy as np


def real_PDB_unit(x: np.ndarray) -> np.ndarray:
    '''Get the unit vector of x\n
    Return 0 if ||x||=0\n
    Return itself if ||x||=1'''
    x_norm = np.linalg.norm(x)
    if abs(x_norm-1) < 10**-6:
        return x
    elif x_norm < 10**-6:
        return np.zeros(3)
    else:
        return x/x_norm


