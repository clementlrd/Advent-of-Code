from Graph import Graph
import numpy as np

with open("input/15.txt") as file:
    lignes = list(map(lambda x: x[:-1], file.readlines()))
    for i in range(len(lignes)):
        lignes[i] = list(map(int, lignes[i]))

    vals = np.array(lignes)
    n, m = vals.shape

    def vois(v):
        i, j = v
        vois = []
        if i != 0:
            vois.append((i - 1, j))
        if i != n - 1:
            vois.append((i + 1, j))
        if j != 0:
            vois.append((i, j - 1))
        if j != m - 1:
            vois.append((i, j + 1))
        return vois

    g = Graph(n, m, w=lambda u, v: vals[v], vois=vois)
    g.end = (n - 1, m - 1)
    print("résultat 1 :", g.dist[g.end])

    new_vals = np.array([[0] * 5 * n for _ in range(5 * m)])
    for k in range(5):
        for s in range(5):
            for i in range(n):
                for j in range(m):
                    a = vals[i, j] + k + s
                    new_vals[i + k * n, j + s * m] = a % 10 + a // 10

    def vois2(v):
        i, j = v
        vois = []
        if i != 0:
            vois.append((i - 1, j))
        if i != 5 * n - 1:
            vois.append((i + 1, j))
        if j != 0:
            vois.append((i, j - 1))
        if j != 5 * m - 1:
            vois.append((i, j + 1))
        return vois

    g2 = Graph(5 * n, 5 * m, w=lambda u, v: new_vals[v], vois=vois2)
    g2.end = (5 * n - 1, 5 * m - 1)
    print("résultat 2 :", g2.dist[g2.end])
