from .distance import distance
from .dode_vert_input_coord import dode_vert_input_coord


def dode_vert_norm_input(radius: float, sigma: float):
    COM, lg1, lg2, lg3, n = dode_vert_input_coord(radius, sigma)
    length = distance(lg1, lg2)
    dis1 = ((-length/2)**2+(-((length/2)*(3**0.5))/3)**2)**0.5
    dis2 = distance(COM, lg1)
    height = (dis2**2-dis1**2)**0.5
    lg1_ = np.array([-length/2, -((length/2)*(3**0.5))/3, -height])
    lg2_ = np.array([length/2, -((length/2)*(3**0.5))/3, -height])
    lg3_ = np.array([0, ((length/2)*(3**0.5))/3*2, -height])
    COM_ = np.array([0, 0, 0])
    n_ = np.array([0, 0, 1])
    return COM_, lg1_, lg2_, lg3_, n_


