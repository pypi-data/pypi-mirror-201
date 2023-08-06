from .COM_leg_list_gen import COM_leg_list_gen
from .octa_face_COM_leg_list_gen import octa_face_COM_leg_list_gen


def octa_face_leg_reduce_coord_gen(radius: float, sigma: float):
    COM_leg_list = octa_face_COM_leg_list_gen(radius)
    COM_leg_red_list = []
    for elements in COM_leg_list:
        temp_list = []
        temp_list.append(elements[0])
        i = 1
        while i <= 3:
            temp_list.append(octa_face_leg_reduce(
                elements[0], elements[i], sigma))
            i += 1
        COM_leg_red_list.append(temp_list)
    return COM_leg_red_list


