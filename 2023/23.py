"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from dataclasses import dataclass
from itertools import starmap
from queue import LifoQueue

from utils import lines_of_file, section, find_element, enumerate_grid, lmap
from utils_types import Grid, Coordinate

DAY = 23
TEST = False


directions = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'v': (1, 0)}
opposite = {'<': '>', '>': '<', '^': 'v', 'v': '^'}


@dataclass
class PathEdge:
    start: Coordinate
    end: Coordinate
    length: int


class PathGraph:
    def __init__(self, grid: Grid[str], slopes=True) -> None:
        dirs = ''.join(directions.keys())
        # find start and end positions
        sj = find_element(grid[0], lambda c: c == '.')[0]
        ej = find_element(grid[-1], lambda c: c == '.')[0]
        self.start, self.end = (0, sj), (len(grid) - 1, ej)

        # create edge graph
        self.edges = dict[Coordinate, list[PathEdge]]()
        self.edges[self.start] = [follow_path(grid, self.start, 'v')]
        for (i, j), c in enumerate_grid(grid):
            starts = starmap(lambda k, l: grid[i + k][j + l] in '#' + dirs, directions.values())
            if c != '.' or not all(starts):
                continue
            for d, (di, dj) in directions.items():
                ni, nj = i + di, j + dj
                if not (0 <= ni < len(grid) and 0 <= nj < len(grid[0])):
                    continue  # outside

                if grid[ni][nj] == d or not slopes and grid[ni][nj] == opposite[d]:  # starting path
                    path = follow_path(grid, (i, j), d)
                    self.edges.setdefault((i, j), []).append(path)

        # create verticies list
        self.V = list(set(p for es in self.edges.values() for e in es for p in (e.start, e.end)))
        self.pos_to_ind = {p: i for i, p in enumerate(self.V)}

    def dfs(self) -> int:
        max_depth, seen = 0, [False] * len(self.V)

        def dfs_recursive(v: Coordinate, d: int):
            nonlocal max_depth
            i = self.pos_to_ind[v]

            if seen[i]:
                return
            seen[i] = True

            if v == self.end:
                max_depth = max(max_depth, d)
            if v in self.edges:
                for e in self.edges[v]:
                    dfs_recursive(e.end, d + e.length)

            seen[i] = False

        dfs_recursive(self.start, 0)
        return max_depth

    def longest_path(self) -> int | float:
        """Not used anymore, but worked for part 1"""
        stack = LifoQueue[Coordinate]()
        visited = set()
        dist = [-float('inf')] * len(self.V)

        def topological_sort(v: Coordinate) -> None:
            visited.add(v)
            if v in self.edges:
                for e in self.edges[v]:
                    if e.end not in visited:
                        topological_sort(e.end)

            stack.put(v)

        for v in self.V:
            if v not in visited:
                topological_sort(v)

        start_id = self.pos_to_ind[self.start]
        dist[start_id] = 0

        while not stack.empty():
            v = stack.get()
            in_id = self.pos_to_ind[v]
            if dist[in_id] != float('inf') and v in self.edges:
                for edge in self.edges[v]:
                    out_id = self.pos_to_ind[edge.end]
                    if dist[out_id] < dist[in_id] + edge.length:
                        dist[out_id] = dist[in_id] + edge.length

        return dist[self.pos_to_ind[self.end]]


def follow_path(grid: Grid[str], start: Coordinate, dir: str) -> PathEdge:
    i, j, di, dj = *start, *directions[dir]
    i, j = i + di, j + dj
    path = set[Coordinate]((start, (i, j)))

    def step(_pos: Coordinate) -> Coordinate:
        _i, _j = _pos
        for di, dj in directions.values():
            ni, nj = _i + di, _j + dj
            if grid[ni][nj] != '#' and (ni, nj) not in path:
                return ni, nj
        raise RuntimeError("Cannot step anymore in position", _pos)

    while True:
        if i in (0, len(grid) - 1):
            return PathEdge(start, (i, j), len(path))
        i, j = step((i, j))
        path.add((i, j))
        if grid[i][j] in directions:
            return PathEdge(start, step((i, j)), len(path))


InputData = Grid[str]


def get_data() -> InputData:
    """Retrieve all the data to begin with."""
    return lmap(list, lines_of_file("inputs/23.txt"))  # create grid


@section(day=DAY, part=1)
def part_1(data: InputData) -> int:
    """Code for section 1"""
    return PathGraph(data).dfs()


@section(day=DAY, part=2)
def part_2(data: InputData) -> int:
    """Code for section 2"""
    return PathGraph(data, slopes=False).dfs()


if __name__ == "__main__":
    part_1(get_data())  # P1: 2254 (j'en ai un en trop qqpart)
    part_2(get_data())  # P2: 6394 (tj le même ecart)
