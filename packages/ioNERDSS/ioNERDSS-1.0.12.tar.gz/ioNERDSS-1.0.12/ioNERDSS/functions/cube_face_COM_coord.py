from .mid_pt import mid_pt


def cube_face_COM_coord(a: float, b: float, c: float, d: float):
    mid_a = mid_pt(a, b)
    mid_b = mid_pt(b, c)
    mid_c = mid_pt(c, d)
    mid_d = mid_pt(d, a)
    COM_a = mid_pt(mid_a, mid_c)
    COM_b = mid_pt(mid_b, mid_d)
    if COM_a == COM_b:
        return COM_a
    else:
        return COM_a


