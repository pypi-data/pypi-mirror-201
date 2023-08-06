from .octa_vert_leg_reduce_coor_gen import octa_vert_leg_reduce_coor_gen


def octa_vert_input_coord(radius: float, sigma: float):
    coor = octa_vert_leg_reduce_coor_gen(radius, sigma)
    coor_ = np.array(coor[4])
    COM = np.around(coor_[0] - coor_[0], 8)
    lg1 = np.around(coor_[1] - coor_[0], 8)
    lg2 = np.around(coor_[2] - coor_[0], 8)
    lg3 = np.around(coor_[3] - coor_[0], 8)
    lg4 = np.around(coor_[4] - coor_[0], 8)
    n = np.around(coor_[0]/np.linalg.norm(coor_[0]), 8)
    return COM, lg1, lg2, lg3, lg4, n


