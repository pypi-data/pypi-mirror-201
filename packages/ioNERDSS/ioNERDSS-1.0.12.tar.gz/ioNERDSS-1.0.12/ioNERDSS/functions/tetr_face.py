from .tetr_face_write import tetr_face_write


def tetr_face(radius: float, sigma: float):
    tetr_face_write(radius, sigma)
    print('File writing complete!')
    return 0


