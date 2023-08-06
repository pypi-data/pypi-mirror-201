from .dode_face_leg_reduce_coor_gen import dode_face_leg_reduce_coor_gen


def dode_face_input_coord(radius: float, sigma: float):
    coor = dode_face_leg_reduce_coor_gen(radius, sigma)
    coor_ = np.array(coor[0])
    COM = coor_[0] - coor_[0]
    lg1 = coor_[1] - coor_[0]
    lg2 = coor_[2] - coor_[0]
    lg3 = coor_[3] - coor_[0]
    lg4 = coor_[4] - coor_[0]
    lg5 = coor_[5] - coor_[0]
    n = -coor_[0]
    return COM, lg1, lg2, lg3, lg4, lg5, n


