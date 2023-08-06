from .cube_face_leg_reduce_coord_gen import cube_face_leg_reduce_coord_gen


def cube_face_input_coord(radius: float, sigma: float):
    coor = cube_face_leg_reduce_coord_gen(radius, sigma)
    coor_ = np.array(coor[0])
    COM = np.around(coor_[0] - coor_[0], 7)
    lg1 = coor_[1] - coor_[0]
    lg2 = coor_[2] - coor_[0]
    lg3 = coor_[3] - coor_[0]
    lg4 = coor_[4] - coor_[0]
    n = -coor_[0]
    return [COM, lg1, lg2, lg3, lg4, n]


