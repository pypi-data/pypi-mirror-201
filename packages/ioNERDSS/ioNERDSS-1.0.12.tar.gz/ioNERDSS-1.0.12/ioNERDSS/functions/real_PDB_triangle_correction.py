def real_PDB_triangle_correction(x: float) -> float:
    '''make x in range of [-1, 1], correct precision'''
    if x < -1 and abs(x+1) < 10**-6:
        return -1
    elif x > 1 and abs(x-1) < 10**-6:
        return 1
    elif -1 <= x <= 1:
        return x
    else:
        raise ValueError(f'{x} is out of the range of sin/cos')


