"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Optional, Iterator
from queue import PriorityQueue
from dataclasses import dataclass
from enum import Enum
from utils import lines_of_file, section, grid_map, lmap
from utils_types import Grid, Coordinate

DAY = 17
TEST = False
VERBOSE = False

InputData = Grid[int]


class Direction(Enum):
    """A cardinal direction"""
    N = (-1, 0)
    S = (1, 0)
    E = (0, 1)
    W = (0, -1)


@dataclass
class SearchNode:
    cost: int
    pos: Coordinate
    h: int = 0
    dir: Optional[Direction] = None
    inertia: int = 0
    previous: Optional[SearchNode] = None

    def __lt__(self, node: SearchNode) -> bool:
        return self.cost + self.h <= node.cost + node.h

    def iterate(self) -> Iterator[SearchNode]:
        """Iterate through previous search nodes."""
        current_node = self
        while current_node is not None:
            yield current_node
            current_node = current_node.previous


def Astar(grid: Grid[int], start: Coordinate = (0, 0)) -> SearchNode:
    """Performs A* search on the grid"""
    n, m = len(grid), len(grid[0])
    end = (n - 1, m - 1)
    L: PriorityQueue[SearchNode] = PriorityQueue()       # Fringe
    L.put(SearchNode(
        cost=grid[start[0]][start[1]],
        pos=start,
    ))
    seen: dict[Coordinate, int] = {}
    a = 0
    while not L.empty():
        node = L.get()        # Select a state
        if node.pos == end:   # Return on final state
            return node

        seen[node.pos] = node.cost

        if VERBOSE and a % 10000 == 0:
            print_search(grid, node)
        a += 1

        for d in Direction:
            di, dj = d.value
            i, j = node.pos
            i, j = i + di, j + dj
            if not (0 <= i < n and 0 <= j < m):
                continue  # outside grid
            if node.dir is not None and node.dir.value == (-di, -dj):
                continue   # don't go back
            if node.dir is not None and d.value == node.dir.value and node.inertia >= 3:
                continue   # maximum inertia
            new_cost = node.cost + grid[i][j]
            if (i, j) in seen and seen[(i, j)] <= new_cost:
                continue   # node already seen with a better cost
            inertia = node.inertia if node.dir is not None and node.dir.value == d.value else 0
            L.put(SearchNode(
                cost=new_cost,
                pos=(i, j),
                dir=d,
                inertia=inertia + 1,
                previous=node,
            ))
    raise RuntimeError("No final State found")


def print_search(grid: Grid[int], node: SearchNode) -> None:
    str_grid = grid_map(str, grid)
    for n in node.iterate():
        if n.dir is None:
            continue
        (i, j), d = n.pos, n.dir
        str_grid[i][j] = '^' if d.name == 'N' else 'v' if d.name == 'S' else '<' if d.name == 'W' else '>'

    with open("visualisations/17.txt", 'w', encoding="utf-8") as f:
        for row in map("".join, str_grid):
            f.write(row + '\n')


def get_data() -> InputData:
    """Retrieve all the data to begin with."""
    l = lines_of_file(f"inputs/{DAY if not TEST else 'test'}.txt")
    l = lmap(list, l)
    return grid_map(int, l)


@section(day=DAY, part=1)
def part_1(data: InputData) -> int:
    """Code for section 1"""
    final_node = Astar(data)
    print_search(data, final_node)
    return final_node.cost - data[0][0]


@section(day=DAY, part=2)
def part_2(data: InputData) -> int:
    """Code for section 2"""
    print(*data, sep="\n")
    return 0


if __name__ == "__main__":
    part_1(get_data())  # P1:
    part_2(get_data())  # P2:
