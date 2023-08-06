import math
import numpy as np


def fitSphere(x, y, z):
    A = np.zeros((len(x), 4))
    A[:, 0] = 2*x
    A[:, 1] = 2*y
    A[:, 2] = 2*z
    A[:, 3] = 1
    f = np.zeros((len(x), 1))
    f[:, 0] = x*x+y*y+z*z
    C, residules, rank, singval = np.linalg.lstsq(A, f)
    t = (C[0]*C[0])+(C[1]*C[1])+(C[2]*C[2])+C[3]
    radius = math.sqrt(t)
    return radius, C[0], C[1], C[2]


