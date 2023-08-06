import numpy as np
from .mid_pt import mid_pt


def octa_vert_COM_leg(COM: float, a: float, b: float, c: float, d: float):
    lega = mid_pt(COM, a)
    legb = mid_pt(COM, b)
    legc = mid_pt(COM, c)
    legd = mid_pt(COM, d)
    return [np.around(COM, 10), np.around(lega, 10), np.around(legb, 10), np.around(legc, 10), np.around(legd, 10)]


