def rotations():
    axes = [[0, 1, 2], [0, 2, 1], [1, 2, 0], [2, 1, 0], [2, 0, 1], [1, 0, 2]]
    signes = [-1, 1]
    for i, axe in enumerate(axes):
        for sign_x in signes:
            for sign_y in signes:
                # using signature
                yield (axe, [sign_x, sign_y, sign_x * sign_y * (-1)**i])


def change_coord(coord, rot, t=[0, 0, 0]):
    axes, signes = rot
    return [coord[axes[i]] * signes[i] - t[i] for i in range(3)]


def compare(j, scanner, new_configs):
    if len(new_configs) == 0:
        raise "No new configs"
    m = 0
    for k, ref_scanner in new_configs:
        # for every rotation, for every translation, compare to a new_configs scanner
        for rot in rotations():
            for coord in scanner:
                translation = change_coord(
                    coord, rot, ref_scanner[0])
                cpt = 0
                for coord_2 in scanner:
                    if change_coord(coord_2, rot, translation) in ref_scanner:
                        cpt += 1
                m = max(m, cpt)
                if cpt >= 12:
                    for i in range(len(scanner)):
                        scanner[i] = change_coord(
                            scanner[i], rot, translation)
                    print("match scanner", j, "with", k)
                    print("used the following rotation :", rot)
                    return scanner
    print("max match for scanner", j, ":", m)


with open("input/test.txt") as file:
    """
    for rot in rotations():
        print([("" if rot[1][i] == 1 else "-") + ("x" if rot[0][i] ==
              0 else "y" if rot[0][i] == 1 else "z") for i in range(3)])
    """
    lignes = list(map(lambda x: x[:-1], file.readlines()))
    scanners = [[]]
    cpt = 0
    # formatting
    # scanner shape : nbr scanners * nbr balises * dimensions (3)
    for k in range(len(lignes)):
        if lignes[k] == "":
            scanners.append([])
            cpt += 1
            continue
        if "---" in lignes[k]:
            continue
        scanners[cpt].append(lignes[k])
    for i in range(len(scanners)):
        scanners[i] = list(map(lambda x: x.split(','), scanners[i]))
        for j in range(len(scanners[i])):
            scanners[i][j] = list(map(int, scanners[i][j]))
    print("formatted")

    # add config 0 (relative to)
    config = []
    new_configs = [(0, scanners[0])]
    other_config = [(1 + i, sc) for (i, sc) in enumerate(scanners[1:])]

    while len(other_config) > 0:
        new = []
        other = []
        for k, scanner in other_config:
            sc = compare(k, scanner, new_configs)
            if sc is None:
                other.append((k, scanner))
            else:
                new.append((k, sc))
        config.extend(new_configs)
        new_configs = new
        other_config = other

    beacons = set()
    for scanner in config:
        for coord in scanner:
            beacons.add(coord)
    print("résultat 1 :", len(beacons))
