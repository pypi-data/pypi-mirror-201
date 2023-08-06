from .cube_vert_coord import cube_vert_coord


def cube_vert_COM_leg_gen(radius: float):
    coord = cube_vert_coord(radius)
    COM_leg_list = []
    COM_leg_list.append(cube_vert_COM_leg(
        coord[0], coord[1], coord[2], coord[3]))
    COM_leg_list.append(cube_vert_COM_leg(
        coord[1], coord[0], coord[4], coord[6]))
    COM_leg_list.append(cube_vert_COM_leg(
        coord[2], coord[0], coord[4], coord[5]))
    COM_leg_list.append(cube_vert_COM_leg(
        coord[3], coord[0], coord[5], coord[6]))
    COM_leg_list.append(cube_vert_COM_leg(
        coord[4], coord[1], coord[2], coord[7]))
    COM_leg_list.append(cube_vert_COM_leg(
        coord[5], coord[2], coord[3], coord[7]))
    COM_leg_list.append(cube_vert_COM_leg(
        coord[6], coord[1], coord[3], coord[7]))
    COM_leg_list.append(cube_vert_COM_leg(
        coord[7], coord[4], coord[5], coord[6]))
    return COM_leg_list


