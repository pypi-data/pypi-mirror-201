from .octa_face_vert_coord import octa_face_vert_coord
from .octa_face_COM_leg_coord import octa_face_COM_leg_coord


def octa_face_COM_leg_list_gen(radius: float):
    coord = octa_face_vert_coord(radius)
    COM_leg_list = []

    COM_leg_list.append(octa_face_COM_leg_coord(coord[0], coord[2], coord[4]))
    COM_leg_list.append(octa_face_COM_leg_coord(coord[0], coord[3], coord[4]))
    COM_leg_list.append(octa_face_COM_leg_coord(coord[0], coord[3], coord[5]))
    COM_leg_list.append(octa_face_COM_leg_coord(coord[0], coord[2], coord[5]))
    COM_leg_list.append(octa_face_COM_leg_coord(coord[1], coord[2], coord[4]))
    COM_leg_list.append(octa_face_COM_leg_coord(coord[1], coord[3], coord[4]))
    COM_leg_list.append(octa_face_COM_leg_coord(coord[1], coord[3], coord[5]))
    COM_leg_list.append(octa_face_COM_leg_coord(coord[1], coord[2], coord[5]))
    return COM_leg_list


