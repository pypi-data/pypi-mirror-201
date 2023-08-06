from .tetr_vert_COM_leg_gen import tetr_vert_COM_leg_gen


def tetr_vert_leg_reduce_coor_gen(radius: float, sigma: float):
    # Generating all the coords of COM and legs when sigma exists
    COM_leg_list = tetr_vert_COM_leg_gen(radius)
    COM_leg_red_list = []
    for elements in COM_leg_list:
        temp_list = []
        temp_list.append(elements[0])
        i = 1
        while i <= 3:
            temp_list.append(tetr_vert_leg_reduce(
                elements[0], elements[i], sigma))
            i += 1
        COM_leg_red_list.append(temp_list)
    return COM_leg_red_list


