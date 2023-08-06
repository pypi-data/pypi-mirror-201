def traj_track(FileName: str, SiteNum: int, MolIndex: list):
    array = []
    for i in range(len(MolIndex)):
        array.append([])
    with open(FileName, 'r') as file:
        for line in file.readlines():
            if line[0:11] == 'iteration: ':
                index = 0
            if len(line.strip(' ').strip('\n').split()) == 4:
                if (index//SiteNum)+1 in MolIndex and index % SiteNum == 0:
                    info = line.strip(' ').strip('\n').split()
                    x = float(info[1])
                    y = float(info[2])
                    z = float(info[3])
                    coord = [x, y, z]
                    list_index = MolIndex.index((index//SiteNum)+1)
                    array[list_index].append(coord)
                index += 1
    return array


# -------------------------------------Gag (Sphere) Regularization Index Calculation---------------------------------------

# ref: https://jekel.me/2015/Least-Squares-Sphere-Fit/
