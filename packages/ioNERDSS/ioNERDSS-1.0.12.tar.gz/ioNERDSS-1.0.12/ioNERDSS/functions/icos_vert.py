from .icos_vert_write import icos_vert_write


def icos_vert(radius: float, sigma: float):
    icos_vert_write(radius, sigma)
    print('File writing complete!')
    return 0


# -----------------------------------Data Visualization------------------------------

# Analysis tools for 'histogram_complexes_time.dat' file


