def octa_face_vert_coord(radius: float):
    scaler = radius
    v0 = [1, 0, 0]
    v1 = [-1, 0, 0]
    v2 = [0, 1, 0]
    v3 = [0, -1, 0]
    v4 = [0, 0, 1]
    v5 = [0, 0, -1]
    VertCoord = [v0, v1, v2, v3, v4, v5]
    VertCoord_ = []
    for i in VertCoord:
        temp_list = []
        for j in i:
            temp = j*scaler
            temp_list.append(temp)
        VertCoord_.append(temp_list)
    return VertCoord_


