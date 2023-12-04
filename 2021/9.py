from helpers import i_max, print_grid


def expansion(t, grid, i, j, surf):
    if i != 0 and valid(t, grid, i - 1, j, i, j):
        grid[i - 1][j] = 2
        surf[0] += 1
        expansion(t, grid, i - 1, j, surf)
    if i != len(lignes) - 1 and valid(t, grid, i + 1, j, i, j):
        grid[i + 1][j] = 2
        surf[0] += 1
        expansion(t, grid, i + 1, j, surf)
    if j != 0 and valid(t, grid, i, j - 1, i, j):
        grid[i][j - 1] = 2
        surf[0] += 1
        expansion(t, grid, i, j - 1, surf)
    if j != len(lignes[0]) - 1 and valid(t, grid, i, j + 1, i, j):
        grid[i][j + 1] = 2
        surf[0] += 1
        expansion(t, grid, i, j + 1, surf)


def valid(t, grid, i, j, pi, pj):
    return not grid[i][j] and int(t[i][j]) != 9 and int(t[i][j]) > int(t[pi][pj])


def max_3(t: list):
    i_m1 = i_max(t)
    m1 = t[i_m1]
    t.pop(i_m1)
    i_m2 = i_max(t)
    m2 = t[i_m2]
    t.pop(i_m2)
    i_m3 = i_max(t)
    m3 = t[i_m3]
    return m1 * m2 * m3


def print_grid_2(grid):
    new_grid = []
    for i in range(len(grid)):
        new_grid.append("".join(map(str, grid[i])))
    print_grid(new_grid)
    new_grid = list(map(lambda x: x.replace(
        "0", "|").replace("1", "*").replace("2", "."), new_grid))
    print_grid(new_grid)


with open("input/9.txt") as file:
    lignes = list(map(lambda x: x[:-1], file.readlines()))
    low_points = []
    for i in range(len(lignes)):
        for j in range(len(lignes[0])):
            m = 9
            if i != 0:
                m = min(m, int(lignes[i - 1][j]))
            if i != len(lignes) - 1:
                m = min(m, int(lignes[i + 1][j]))
            if j != 0:
                m = min(m, int(lignes[i][j - 1]))
            if j != len(lignes[0]) - 1:
                m = min(m, int(lignes[i][j + 1]))
            if int(lignes[i][j]) < m:
                low_points.append(int(lignes[i][j]))
    print(low_points)
    print("résultat 1 :", sum(low_points) + len(low_points))

    grid = [[0] * len(lignes[0]) for _ in range(len(lignes))]
    bassins = []
    for i in range(len(lignes)):
        for j in range(len(lignes[0])):
            m = 9
            if i != 0:
                m = min(m, int(lignes[i - 1][j]))
            if i != len(lignes) - 1:
                m = min(m, int(lignes[i + 1][j]))
            if j != 0:
                m = min(m, int(lignes[i][j - 1]))
            if j != len(lignes[0]) - 1:
                m = min(m, int(lignes[i][j + 1]))
            if int(lignes[i][j]) < m:
                grid[i][j] = 1
    surfaces = []
    for i in range(len(lignes)):
        for j in range(len(lignes[0])):
            if grid[i][j] == 1:
                surf = [1]
                if i != 0 and valid(lignes, grid, i - 1, j, i, j):
                    grid[i - 1][j] = 2
                    surf[0] += 1
                    expansion(lignes, grid, i - 1, j, surf)
                if i != len(lignes) - 1 and valid(lignes, grid, i + 1, j, i, j):
                    grid[i + 1][j] = 2
                    surf[0] += 1
                    expansion(lignes, grid, i + 1, j, surf)
                if j != 0 and valid(lignes, grid, i, j - 1, i, j):
                    grid[i][j - 1] = 2
                    surf[0] += 1
                    expansion(lignes, grid, i, j - 1, surf)
                if j != len(lignes[0]) - 1 and valid(lignes, grid, i, j + 1, i, j):
                    grid[i][j + 1] = 2
                    surf[0] += 1
                    expansion(lignes, grid, i, j + 1, surf)
                surfaces.append(surf[0])
    print("résultat 2 :", max_3(surfaces[:]))
    print_grid_2(grid)
