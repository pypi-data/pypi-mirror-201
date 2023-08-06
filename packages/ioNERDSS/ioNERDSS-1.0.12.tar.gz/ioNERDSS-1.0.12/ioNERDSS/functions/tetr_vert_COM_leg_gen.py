from .tetr_vert_coord import tetr_vert_coord


def tetr_vert_COM_leg_gen(radius: float):
    coord = tetr_vert_coord(radius)
    COM_leg_list = []
    COM_leg_list.append(tetr_vert_COM_leg(
        coord[0], coord[1], coord[2], coord[3]))
    COM_leg_list.append(tetr_vert_COM_leg(
        coord[1], coord[2], coord[3], coord[0]))
    COM_leg_list.append(tetr_vert_COM_leg(
        coord[2], coord[3], coord[0], coord[1]))
    COM_leg_list.append(tetr_vert_COM_leg(
        coord[3], coord[0], coord[1], coord[2]))
    return COM_leg_list


