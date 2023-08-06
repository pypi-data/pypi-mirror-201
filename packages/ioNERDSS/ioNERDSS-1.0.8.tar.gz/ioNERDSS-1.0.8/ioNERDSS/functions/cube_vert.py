from .cube_vert_write import cube_vert_write


def cube_vert(radius: float, sigma: float):
    cube_vert_write(radius, sigma)
    print('File writing complete!')
    return 0


