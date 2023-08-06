import math
import numpy as np
from .real_PDB_unit import real_PDB_unit
from .real_PDB_triangle_correction import real_PDB_triangle_correction


def real_PDB_calculate_phi(v: np.ndarray, n: np.ndarray, sigma: np.ndarray) -> float:

    # calculate phi
    t1 = real_PDB_unit(np.cross(v, sigma))
    t2 = real_PDB_unit(np.cross(v, n))
    phi = math.acos(real_PDB_triangle_correction(np.dot(t1, t2)))

    # determine the sign of phi (+/-)
    v_uni = real_PDB_unit(v)
    n_proj = n - v_uni * np.dot(v_uni, n)
    sigma_proj = sigma - v_uni * np.dot(v_uni, sigma)
    phi_dir = real_PDB_unit(np.cross(sigma_proj, n_proj))

    if np.dot(v_uni, phi_dir) > 0:
        phi = -phi
    else:
        phi = phi

    return phi


# This function will calculate five necessary angles: theta_one, theta_two, phi_one, phi_two and omega
# Input variables: four coordinates indicating COM and interaction site of two chains
# First created by Yian Qian
# Modified by Mankun Sang on 04/13/2022
#   1) unit of zero vector and length-one vector
#   2) error messages when v // n
#   3) test scripts
# Modified by Yian Qian & Mankun Sang on 04/16/2022
#   0) correct omega calculation when n // sigma
#   1) generalize the sign determination of phi and omega
#   2) created a function for phi cacluation
