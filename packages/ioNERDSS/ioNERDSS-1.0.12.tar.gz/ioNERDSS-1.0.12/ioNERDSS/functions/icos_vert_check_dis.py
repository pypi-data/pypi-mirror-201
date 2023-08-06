from .distance import distance


def icos_vert_check_dis(cen: float, COM: float, lg1: float, lg2: float, lg3: float, lg4: float, lg5: float):
    dis1 = round(distance(cen, lg1), 8)
    dis2 = round(distance(cen, lg2), 8)
    dis3 = round(distance(cen, lg3), 8)
    dis4 = round(distance(cen, lg4), 8)
    dis5 = round(distance(cen, lg5), 8)
    dis_ = round(distance(COM, cen), 8)
    if dis1 == dis2 and dis1 == dis3 and dis1 == dis4 and dis1 == dis5:
        return dis1, dis_
    else:
        return dis1, dis_


