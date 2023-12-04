import numpy as np


def print_grid(t):
    n, m = t.shape
    for i in range(n):
        print(" ".join(list(map(lambda x: "#" if x else ".", t[i]))))


def count(grid):
    cpt = 0
    for x in grid:
        for e in x:
            cpt += e
    print("résultat 1 :", cpt)


with open("input/13.txt") as file:
    lignes = list(map(lambda x: x[:-1], file))
    vals = []
    fold = []
    sep = False
    for i in range(len(lignes)):
        if not sep and not lignes[i]:
            sep = True
            continue
        if sep:
            fold.append(lignes[i])
        else:
            vals.append(lignes[i])
    vals = np.array(list(map(lambda x: list(map(int, x.split(','))), vals)))
    grid = np.zeros((vals[:, 1].max() + 1, vals[:, 0].max() + 1), dtype=int)
    for i in range(vals.shape[0]):
        x, y = vals[i]
        grid[y, x] = 1

    for k in range(len(fold)):
        fold[k] = fold[k].split("fold along ")[1]
        pos = int(fold[k][2:])
        if fold[k][0] == 'x':
            n, m = grid.shape
            new_grid = np.zeros((n, pos), dtype=int)
            for i in range(n):
                for j in range(pos):
                    new_grid[i, j] = grid[i, j]
                for j in range(pos + 1, m):
                    new_grid[i, pos - j] += grid[i, j]
        elif fold[k][0] == 'y':
            n, m = grid.shape
            new_grid = np.zeros((pos, m), dtype=int)
            for i in range(pos):
                new_grid[i] = grid[i]
            for i in range(pos + 1, n):
                new_grid[pos - i] += grid[i]
        grid = new_grid
    print_grid(grid)
    count(grid)
