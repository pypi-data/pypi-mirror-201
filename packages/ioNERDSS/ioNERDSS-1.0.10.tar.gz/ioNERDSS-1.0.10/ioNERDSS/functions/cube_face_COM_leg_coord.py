from .mid_pt import mid_pt
from .cube_face_COM_coord import cube_face_COM_coord


def cube_face_COM_leg_coord(a: float, b: float, c: float, d: float):
    COM_leg = []
    COM_leg.append(cube_face_COM_coord(a, b, c, d))
    COM_leg.append(mid_pt(a, b))
    COM_leg.append(mid_pt(b, c))
    COM_leg.append(mid_pt(c, d))
    COM_leg.append(mid_pt(d, a))
    return COM_leg


