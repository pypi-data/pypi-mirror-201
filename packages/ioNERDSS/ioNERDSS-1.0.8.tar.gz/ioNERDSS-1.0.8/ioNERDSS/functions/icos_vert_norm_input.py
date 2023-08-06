import math


def icos_vert_norm_input(scaler: float, dis_: float):
    c1 = math.cos(2*math.pi/5)
    c2 = math.cos(math.pi/5)
    s1 = math.sin(2*math.pi/5)
    s2 = math.sin(4*math.pi/5)
    v0 = scaler*np.array([0, 1])
    v1 = scaler*np.array([-s1, c1])
    v2 = scaler*np.array([-s2, -c2])
    v3 = scaler*np.array([s2, -c2])
    v4 = scaler*np.array([s1, c1])
    lg1 = np.array([v0[0], v0[1], -dis_])
    lg2 = np.array([v1[0], v1[1], -dis_])
    lg3 = np.array([v2[0], v2[1], -dis_])
    lg4 = np.array([v3[0], v3[1], -dis_])
    lg5 = np.array([v4[0], v4[1], -dis_])
    COM = np.array([0, 0, 0])
    n = np.array([0, 0, 1])
    return COM, lg1, lg2, lg3, lg4, lg5, n


