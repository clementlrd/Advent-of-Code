from utils import lmap, find, crange, neighbourhood, print_matrix
import numpy as np
from functools import reduce

part = 2


class Graph:
    def __init__(self, mat) -> None:
        self.matrix = np.array(mat)
        self.size = self.matrix.shape
        for x in crange(self.size):
            if self.matrix[x] == -1:
                self.start = x
            elif self.matrix[x] == ord('z') - ord('a') + 1:
                self.end = x
        self.dist = np.infty * np.ones(self.size)
        self.dist[self.start] = 0
        self.visited = np.zeros(self.size, dtype=bool)
        self.visited[self.start] = True

    def _minDistance(self):
        min = np.infty
        min_index = self.start
        for x in crange(self.size):
            if self.dist[x] < min and not self.visited[x]:
                min = self.dist[x]
                min_index = x
        return min_index

    def dijkstra(self):
        while not reduce(lambda acc, x: acc and x, self.visited.flatten()):
            u = self._minDistance()
            self.visited[u] = True

            for x in neighbourhood(u, self.size):
                if (not self.visited[x] and self.matrix[x] - self.matrix[u] <= 1 and self.dist[x] > self.dist[u] + 1):
                    if (part == 1):
                        self.dist[x] = self.dist[u] + 1
                    else:
                        self.dist[x] = self.dist[u] if self.matrix[x] == 0 else self.dist[u] + 1


with open("inputs/12.txt", "r") as file:
    heightmap = lmap(lambda x: lmap(lambda y: ord(
        y) - ord('a') if y not in ['E', 'S'] else {'S': -1, 'E': ord('z') - ord('a') + 1}[y], x[:-1]), file.readlines())
    graph = Graph(heightmap)
    graph.dijkstra()
    # -- part 1 --
    print(f"partie {part} :", graph.dist[graph.end])
