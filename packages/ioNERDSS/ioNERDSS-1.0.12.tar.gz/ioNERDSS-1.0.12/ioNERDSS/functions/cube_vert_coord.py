def cube_vert_coord(radius: float):
    scaler = radius/3**0.5
    v0 = [1, 1, 1]
    v1 = [-1, 1, 1]
    v2 = [1, -1, 1]
    v3 = [1, 1, -1]
    v4 = [-1, -1, 1]
    v5 = [1, -1, -1]
    v6 = [-1, 1, -1]
    v7 = [-1, -1, -1]
    VertCoord = [v0, v1, v2, v3, v4, v5, v6, v7]
    VertCoord_ = []
    for i in VertCoord:
        temp_list = []
        for j in i:
            temp = j*scaler
            temp_list.append(temp)
        VertCoord_.append(temp_list)
    return VertCoord_


