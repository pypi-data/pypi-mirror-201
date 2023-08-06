from .cube_face_vert_coord import cube_face_vert_coord
from .cube_face_COM_coord import cube_face_COM_coord


def cube_face_COM_list_gen(radius: float):
    coord = cube_face_vert_coord(radius)
    COM_list = []
    COM_list.append(cube_face_COM_coord(
        coord[0], coord[3], coord[5], coord[2]))
    COM_list.append(cube_face_COM_coord(
        coord[0], coord[3], coord[6], coord[1]))
    COM_list.append(cube_face_COM_coord(
        coord[0], coord[1], coord[4], coord[2]))
    COM_list.append(cube_face_COM_coord(
        coord[7], coord[4], coord[1], coord[6]))
    COM_list.append(cube_face_COM_coord(
        coord[7], coord[4], coord[2], coord[5]))
    COM_list.append(cube_face_COM_coord(
        coord[7], coord[6], coord[3], coord[5]))
    return COM_list


