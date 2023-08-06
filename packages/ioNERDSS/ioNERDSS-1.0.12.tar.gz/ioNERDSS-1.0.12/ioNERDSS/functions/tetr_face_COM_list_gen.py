from .tetr_face_coord import tetr_face_coord
from .tetr_face_COM_coord import tetr_face_COM_coord


def tetr_face_COM_list_gen(radius: float):
    coord = tetr_face_coord(radius)
    COM_list = []
    COM_list.append(tetr_face_COM_coord(coord[0], coord[1], coord[2]))
    COM_list.append(tetr_face_COM_coord(coord[0], coord[2], coord[3]))
    COM_list.append(tetr_face_COM_coord(coord[0], coord[1], coord[3]))
    COM_list.append(tetr_face_COM_coord(coord[1], coord[2], coord[3]))
    return COM_list


