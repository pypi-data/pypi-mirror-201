from .octa_face_write import octa_face_write


def octa_face(radius: float, sigma: float):
    octa_face_write(radius, sigma)
    print('File writing complete!')
    return 0


