from .mid_pt import mid_pt
from .octa_face_COM_coord import octa_face_COM_coord


def octa_face_COM_leg_coord(a: float, b: float, c: float):
    COM_leg = []
    COM_leg.append(octa_face_COM_coord(a, b, c))
    COM_leg.append(mid_pt(a, b))
    COM_leg.append(mid_pt(b, c))
    COM_leg.append(mid_pt(c, a))
    return COM_leg


