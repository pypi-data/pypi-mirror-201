from .cube_face_write import cube_face_write


def cube_face(radius: float, sigma: float):
    cube_face_write(radius, sigma)
    print('File writing complete!')
    return 0


