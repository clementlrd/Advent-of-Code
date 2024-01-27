"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Iterator
from dataclasses import dataclass
from queue import LifoQueue
from collections import defaultdict

from utils import section, enumerate_grid, lmap
from utils_types import Grid, Coordinate


directions = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'v': (1, 0)}
opposite = {'<': '>', '>': '<', '^': 'v', 'v': '^'}


@dataclass(frozen=True, slots=True)
class PathEdge:
    """Represents a path between two crossroads as an edge of a graph
    whose weight is the length of the path."""
    start: Coordinate
    end: Coordinate
    length: int


class PathGraph:
    """Represents the forest as a directed graph where verticies are the coordinates
    of the crossroadsand edges (PathEdge) are the length of these path."""

    def __init__(self, grid: Grid[str], slopes=True) -> None:
        # find start and end positions
        self.start = (0, grid[0].index('.'))
        self.end = (len(grid) - 1, grid[-1].index('.'))

        # create edge graph
        self.edges = defaultdict[Coordinate, list[PathEdge]](list)
        self.edges[self.start] = [follow_path(grid, self.start, 'v')]
        for (i, j), c in enumerate_grid(grid):
            if c != '.':
                continue  # a crossroad is necessary on a path
            for k, l in directions.values():
                if grid[i + k][j + l] not in '#<^v>':
                    break  # a crossroad has only slopes or walls next to it
            else:
                # we found a crossroad, compute path
                for d, (di, dj) in directions.items():
                    if not (0 <= (ni := i + di) < len(grid) and 0 <= (nj := j + dj) < len(grid[0])):
                        continue  # outside the grid

                    if grid[ni][nj] == d or not slopes and grid[ni][nj] == opposite[d]:
                        path = follow_path(grid, (i, j), d)
                        self.edges[(i, j)].append(path)

        # create a list of vertex
        self.V = list(set(p for es in self.edges.values() for e in es for p in (e.start, e.end)))
        self.pos_to_ind = {p: i for i, p in enumerate(self.V)}

    def dfs(self) -> int:
        """Use a recursive DFS to find the maximal depth on the grid."""
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
        """Not used anymore, but worked for part 1."""
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
                    if dist[out_id] < (d := dist[in_id] + edge.length):
                        dist[out_id] = d

        return dist[self.pos_to_ind[self.end]]


def follow_path(grid: Grid[str], start: Coordinate, direction: str) -> PathEdge:
    """Follow a path until the next crossroad. It returns a PathEdge object."""
    # make first step to init the path
    i, j, di, dj = *start, *directions[direction]
    i, j = i + di, j + dj
    path = set[Coordinate]((start, (i, j)))

    def step(_pos: Coordinate) -> Coordinate:
        """Make one step further on the path. It returns the next position."""
        _i, _j = _pos
        for di, dj in directions.values():
            if grid[ni := _i + di][nj := _j + dj] != '#' and (ni, nj) not in path:
                return ni, nj
        raise RuntimeError("Cannot step anymore in position", _pos)

    while True:
        if i in (0, len(grid) - 1):  # has reached an end of the grid
            return PathEdge(start, (i, j), len(path) - 1)

        i, j = step((i, j))
        path.add((i, j))

        if grid[i][j] in directions:  # has reached a crossroad
            return PathEdge(start, step((i, j)), len(path))


@section(year=2023, day=23, part=1, sol=2254)
def part_1(data: Iterator[str]) -> int:
    """Code for section 1"""
    grid = lmap(list, data)
    return PathGraph(grid).dfs()


@section(year=2023, day=23, part=2, sol=6394)
def part_2(data: Iterator[str]) -> int:
    """Code for section 2"""
    grid = lmap(list, data)
    return PathGraph(grid, slopes=False).dfs()


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    part_1()
    part_2()
