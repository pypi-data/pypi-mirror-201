from .dode_vert_leg_reduce_coor_gen import dode_vert_leg_reduce_coor_gen


def dode_vert_input_coord(radius: float, sigma: float):
    coor = dode_vert_leg_reduce_coor_gen(radius, sigma)
    coor_ = np.array(coor[0])
    COM = np.around(coor_[0] - coor_[0], 12)
    lg1 = np.around(coor_[1] - coor_[0], 12)
    lg2 = np.around(coor_[2] - coor_[0], 12)
    lg3 = np.around(coor_[3] - coor_[0], 12)
    n = np.around(coor_[0]/np.linalg.norm(coor_[0]), 12)
    return COM, lg1, lg2, lg3, n


