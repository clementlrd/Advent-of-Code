import re
import helpers


def write_range(t, isRow, row, start, stop):
    for i in range(start, stop + 1):
        if isRow:
            t[row][i] += 1
        else:
            t[i][row] += 1


def write_diagonals(t, q, _x1, _y1, _x2, _y2):
    x1 = min(_x1, _x2)
    x2 = max(_x1, _x2)
    y1 = min(_y1, _y2)
    y2 = max(_y1, _y2)
    if (q == 1):
        for i in range(x2 - x1 + 1):
            t[y1 + i][x1 + i] += 1
    else:
        for i in range(x2 - x1 + 1):
            t[y2 - i][x1 + i] += 1


def count_over_one(t):
    s = 0
    for i in range(len(t)):
        for j in range(len(t[0])):
            if (t[i][j] > 1):
                s += 1
    return s


# x1,y1 -> x2,y2
# y -> rows
# x -> columns
with open("input/5.txt") as file:
    lignes = file.readlines()
    lignes = list(map(lambda x: re.split(r",|->", x), lignes))
    n = 991
    grid = [[0] * n for i in range(n)]
    for i in range(len(lignes)):
        lignes[i] = list(map(int, lignes[i]))
        x1 = lignes[i][0]
        y1 = lignes[i][1]
        x2 = lignes[i][2]
        y2 = lignes[i][3]
        if (x1 == x2):
            write_range(grid, False, x1, min(y1, y2), max(y1, y2))
        elif (y1 == y2):
            write_range(grid, True, y1, min(x1, x2), max(x1, x2))
    print("nombre max dans la grille :", helpers.max_mat(grid))
    print("resultat 1 : ", count_over_one(grid))

    # add diagonals
    cpt = 0
    for i in range(len(lignes)):
        x1 = lignes[i][0]
        y1 = lignes[i][1]
        x2 = lignes[i][2]
        y2 = lignes[i][3]
        if x1 == x2 and y1 == y2:
            grid[y1][x1] += 1
        elif x1 == x2 or y1 == y2:
            pass
        else:
            q = (y2 - y1) / (x2 - x1)
            if q in [1, -1]:
                cpt += 1
                write_diagonals(grid, q, x1, y1, x2, y2)
    print("s'ajoutent", cpt, "diagonales")
    print("résultat 2 :", count_over_one(grid))
