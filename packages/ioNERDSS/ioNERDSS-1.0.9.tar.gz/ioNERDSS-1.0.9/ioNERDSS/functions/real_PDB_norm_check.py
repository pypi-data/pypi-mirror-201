import numpy as np


def real_PDB_norm_check(norm, COM, site, buffer_ratio=1e-3):
    '''
    norm is a 3D vector
    COM is a point
    site is a point
    False: continue norm calculation
    True: requesting redo input
    '''
    for i in norm:
        if type(i) != float:
            return True
    for i in COM:
        if type(i) != float:
            return True
    for i in site:
        if type(i) != float:
            return True
    if len(norm) != 3 or len(COM) != 3 or len(site) != 3:
        return True
    if norm == [0, 0, 0]:
        return True
    norm = np.array(norm)
    COM = np.array(COM)
    site = np.array(site)
    vec1 = norm
    vec2 = site - COM
    zero_pos_1 = []
    zero_pos_2 = []
    for i in range(len(vec1)):
        if vec1[i] == 0:
            zero_pos_1.append(i)
    for i in range(len(vec2)):
        if vec2[i] == 0:
            zero_pos_2.append(i)
    if len(zero_pos_1) == 1 and len(zero_pos_2) == 1 and zero_pos_1 == zero_pos_2:
        pool = [0, 1, 2]
        pool.remove(zero_pos_1[0])
        ratio = vec1[pool[0]]/vec2[pool[0]]
        if vec1[pool[1]]/vec2[pool[1]] >= ratio*(1-buffer_ratio) and vec1[pool[1]]/vec2[pool[1]] <= ratio*(1+buffer_ratio):
            return True
        else:
            return False
    elif len(zero_pos_1) == 1 and len(zero_pos_2) == 1 and zero_pos_1 != zero_pos_2:
        return False
    elif len(zero_pos_1) == 2 and len(zero_pos_2) == 2 and zero_pos_1 == zero_pos_2:
        return True
    elif len(zero_pos_1) == 2 and len(zero_pos_2) == 2 and zero_pos_1 != zero_pos_2:
        return False
    elif len(zero_pos_1) != len(zero_pos_2):
        return False
    else:
        ratio = vec1[0]/vec2[0]
        if ratio >= 0:
            if vec1[1]/vec2[1] >= ratio*(1-buffer_ratio) and vec1[1]/vec2[1] <= ratio*(1+buffer_ratio):
                if vec1[2]/vec2[2] >= ratio*(1-buffer_ratio) and vec1[2]/vec2[2] <= ratio*(1+buffer_ratio):
                    return True
                else:
                    return False
            else:
                return False
        if ratio < 0:
            if vec1[1]/vec2[1] >= ratio*(1+buffer_ratio) and vec1[1]/vec2[1] <= ratio*(1-buffer_ratio):
                if vec1[2]/vec2[2] >= ratio*(1+buffer_ratio) and vec1[2]/vec2[2] <= ratio*(1-buffer_ratio):
                    return True
                else:
                    return False
            else:
                return False


