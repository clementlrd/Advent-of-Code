from helpers import print_grid

STEP = 999
PRINT = False


def vois(i, j):
    return [(i + k, j + n) for k in [-1, 0, 1] for n in [-1, 0, 1]]


def valid_vois(i, j, n, m):
    v = vois(i, j)
    new_vois = []
    for (k, l) in v:
        if 0 <= k < n and 0 <= l < m and not (k == i and l == j):
            new_vois.append((k, l))
    return new_vois


def blow(t, i, j):
    cpt = 1
    t[i][j] = 0
    for (k, l) in valid_vois(i, j, len(t), len(t[0])):
        if not t[k][l]:
            pass
        elif t[k][l] < 9:
            t[k][l] += 1
        elif t[k][l] >= 9:
            cpt += blow(t, k, l)
    return cpt


with open("input/11.txt") as file:
    lignes = file.readlines()
    grid = [list(map(int, list(lignes[i][:-1]))) for i in range(len(lignes))]
    print_grid(grid)

    cpt = 0
    for k in range(STEP):
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] <= 9:
                    grid[i][j] += 1
        for i in range(len(grid)):
            for j in range(len(grid)):
                if grid[i][j] > 9:
                    cpt += blow(grid, i, j)
        if PRINT:
            print(f"\n--STEP {k+1}--")
            print_grid(grid)
            input()

        zero = True
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                zero = zero and not grid[i][j]
        if zero:
            print()
            print_grid(grid)
            print("résultat 2 :", k + 1)
            break
        if k == 99:
            print("résultat 1 :", cpt)
