from .dode_face_write import dode_face_write


def dode_face(radius: float, sigma: float):
    dode_face_write(radius, sigma)
    print('File writing complete!')
    return 0


