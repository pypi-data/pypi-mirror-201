from .octa_vert_write import octa_vert_write


def octa_vert(radius: float, sigma: float):
    octa_vert_write(radius, sigma)
    print('File writing complete!')
    return 0


