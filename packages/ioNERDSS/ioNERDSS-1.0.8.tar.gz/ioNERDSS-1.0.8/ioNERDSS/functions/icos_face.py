from .icos_face_write import icos_face_write


def icos_face(radius: float, sigma: float):
    icos_face_write(radius, sigma)
    print('File writing complete!')
    return 0


