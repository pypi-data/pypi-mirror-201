from .icos_vert_COM_leg_gen import icos_vert_COM_leg_gen


def icos_vert_leg_reduce_coor_gen(radius: float, sigma: float):
    COM_leg_list = icos_vert_COM_leg_gen(radius)
    COM_leg_red_list = []
    for elements in COM_leg_list:
        temp_list = []
        temp_list.append(elements[0])
        i = 1
        while i <= 5:
            temp_list.append(icos_vert_leg_reduce(
                elements[0], elements[i], sigma))
            i += 1
        COM_leg_red_list.append(temp_list)
    return COM_leg_red_list


