from .icos_face_vert_coord import icos_face_vert_coord
from .icos_face_COM_leg_coord import icos_face_COM_leg_coord


def COM_leg_list_gen(radius: float):
    coord = icos_face_vert_coord(radius)
    COM_leg_list = []
    COM_leg_list.append(icos_face_COM_leg_coord(coord[0], coord[2], coord[8]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[0], coord[8], coord[4]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[0], coord[4], coord[6]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[0], coord[6], coord[10]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[0], coord[10], coord[2]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[3], coord[7], coord[5]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[3], coord[5], coord[9]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[3], coord[9], coord[1]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[3], coord[1], coord[11]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[3], coord[11], coord[7]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[7], coord[2], coord[5]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[2], coord[5], coord[8]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[5], coord[8], coord[9]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[8], coord[9], coord[4]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[9], coord[4], coord[1]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[4], coord[1], coord[6]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[1], coord[6], coord[11]))
    COM_leg_list.append(icos_face_COM_leg_coord(
        coord[6], coord[11], coord[10]))
    COM_leg_list.append(icos_face_COM_leg_coord(
        coord[11], coord[10], coord[7]))
    COM_leg_list.append(icos_face_COM_leg_coord(coord[10], coord[7], coord[2]))
    return COM_leg_list


