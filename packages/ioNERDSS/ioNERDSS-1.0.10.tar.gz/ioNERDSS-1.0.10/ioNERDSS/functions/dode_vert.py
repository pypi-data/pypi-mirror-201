from .dode_vert_write import dode_vert_write


def dode_vert(radius: float, sigma: float):
    dode_vert_write(radius, sigma)
    print('File writing complete!')
    return 0


