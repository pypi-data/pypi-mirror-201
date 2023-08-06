from .dode_face_COM_leg_list_gen import dode_face_COM_leg_list_gen
from .COM_leg_list_gen import COM_leg_list_gen


def dode_face_leg_reduce_coor_gen(radius: float, sigma: float):
    # Generating all the coords of COM and legs when sigma exists
    COM_leg_list = dode_face_COM_leg_list_gen(radius)
    COM_leg_red_list = []
    for elements in COM_leg_list:
        temp_list = []
        temp_list.append(elements[0])
        i = 1
        while i <= 5:
            temp_list.append(dode_face_leg_reduce(
                elements[0], elements[i], sigma))
            i += 1
        COM_leg_red_list.append(temp_list)
    return COM_leg_red_list


