import math


def real_PDB_mag(x):
    return math.sqrt(sum(i ** 2 for i in x))


