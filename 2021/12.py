from helpers import print_grid
import numpy as np


def explore(caves, cave_connections, i, path):
    if caves[i] == "end":
        # print(path + ["end"])
        return 1
    cpt = 0
    for j in range(len(caves)):
        if (cave_connections[i, j] == 2 or (cave_connections[i, j] == 1 and caves[j] not in path)):
            cpt += explore(caves, cave_connections, j, path + [caves[j]])
    return cpt


def explore2(caves, cave_connections, i, path):
    if caves[i] == "end":
        # print(path)
        return 1
    cpt = 0
    for j in range(len(caves)):
        b = cave_connections[i, j] == 1
        if ((cave_connections[i, j] == 2 or b) and caves[j] != "start"):
            if (b and caves[j] in path and path[0]):
                continue
            new_path = path + [caves[j]]
            if (b and caves[j] in path and not path[0]):
                new_path[0] = True
            cpt += explore2(caves, cave_connections, j, new_path)
    return cpt


with open("input/12.txt") as file:
    lignes = list(map(lambda x: x[:-1].split("-"), file.readlines()))
    n = len(lignes)
    # print_grid(lignes)
    caves = []
    for i in range(n):
        for j in range(2):
            if lignes[i][j] not in caves:
                caves.append(lignes[i][j])
    m = len(caves)
    cave_connections = np.zeros((m, m), dtype=int)
    for k in range(n):
        i = caves.index(lignes[k][0])
        j = caves.index(lignes[k][1])
        cave_connections[j, i] = 2 if caves[i].upper() == caves[i] else 1
        cave_connections[i, j] = 2 if caves[j].upper() == caves[j] else 1
    print_grid(cave_connections)
    print(caves)
    cpt = explore(caves, cave_connections, caves.index("start"), ["start"])
    print("résultat 1 :", cpt)
    cpt = explore2(caves, cave_connections,
                   caves.index("start"), [False, "start"])
    print("résultat 2 :", cpt)
