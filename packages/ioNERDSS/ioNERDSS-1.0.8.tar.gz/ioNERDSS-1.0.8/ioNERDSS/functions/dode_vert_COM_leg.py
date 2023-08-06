import numpy as np
from .mid_pt import mid_pt


def dode_vert_COM_leg(COM: float, a: float, b: float, c: float):
    lega = mid_pt(COM, a)
    legb = mid_pt(COM, b)
    legc = mid_pt(COM, c)
    return [np.around(COM, 10), np.around(lega, 10), np.around(legb, 10), np.around(legc, 10)]


