from .tetr_vert_write import tetr_vert_write


def tetr_vert(radius: float, sigma: float):
    tetr_vert_write(radius, sigma)
    print('File writing complete!')
    return 0


