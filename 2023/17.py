"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Callable, Iterator
from queue import PriorityQueue
from utils import section, grid_map, lmap
from utils_types import Grid, Coordinate

directions = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'v': (1, 0)}
opposite = {'<': '>', '>': '<', '^': 'v', 'v': '^'}


def neighbors(grid: Grid[int], node: Node) -> Iterator[Node]:
    """Compute neighbors of a node: the new position and """
    (i, j), dirs = node
    for new_d, (di, dj) in directions.items():
        ni, nj = i + di, j + dj
        if not (0 <= ni < len(grid) and 0 <= nj < len(grid[0])):
            continue   # outside grid

        if dirs and new_d == dirs[-1]:
            new_dirs = dirs + new_d
        else:
            new_dirs = new_d

        yield ((ni, nj), new_dirs)


Node = tuple[Coordinate, str]  # coordinate / direction with inertia
SearchNode = tuple[int, *Node, str]  # cost / node / path


def uniformCostSearch(
    grid: Grid[int],
    is_terminal: Callable[[Node], bool],
    is_valid: Callable[[Node, Node], bool],
    start: Coordinate = (0, 0)
) -> tuple[int, Coordinate, str, str]:
    """Performs uniform cost search on the grid to find the path with lower cost."""
    L = PriorityQueue[SearchNode]()
    L.put((0, start, '', ''))
    seen = set[Node]()

    while not L.empty():
        cost, pos, direction, path = L.get()  # select a state
        node: Node = pos, direction

        if is_terminal(node):          # Return on final state
            return cost, pos, direction, path

        if node in seen:
            continue
        seen.add(node)

        for new_node in neighbors(grid, node):
            if is_valid(node, new_node) and new_node not in seen:
                (i, j), dirs = new_node
                L.put((cost + grid[i][j], (i, j), dirs, path + dirs[-1]))
    raise RuntimeError("No final State found")


@section(year=2023, day=17, part=1, sol=845)
def part_1(data: Iterator[str]) -> int:
    """Code for section 1"""
    grid = lmap(list, data)     # convert to grid
    grid = grid_map(int, grid)  # convert grid from str to int

    def is_terminal(node: Node) -> bool:
        return node[0] == (len(grid) - 1, len(grid[0]) - 1)

    def is_valid(node: Node, new_node: Node) -> bool:
        (_, dirs), (_, new_dirs) = node, new_node
        # don't go back and maximum inertia
        return not dirs or new_dirs[-1] != opposite[dirs[-1]] and len(new_dirs) <= 3

    return uniformCostSearch(grid, is_terminal, is_valid)[0]


@section(year=2023, day=17, part=2, sol=993)
def part_2(data: Iterator[str]) -> int:
    """Code for section 2"""
    grid = lmap(list, data)     # convert to grid
    grid = grid_map(int, grid)  # convert grid from str to int

    def is_terminal(node: Node) -> bool:
        pos, dirs, n, m = *node, len(grid), len(grid[0])
        fstate1 = pos == (n - 5, m - 1) and ('v' not in dirs or len(dirs) <= 6)
        fstate2 = pos == (n - 1, m - 5) and ('>' not in dirs or len(dirs) <= 6)
        return fstate1 or fstate2

    def is_valid(node: Node, new_node: Node) -> bool:
        (_, dirs), (_, new_dirs) = node, new_node
        # don't go back and maximum inertia
        not_go_back = not dirs or new_dirs[-1] != opposite[dirs[-1]]
        min_inertia = len(dirs) >= 4 or dirs in new_dirs
        max_inertia = len(new_dirs) <= 10
        return not dirs or not_go_back and min_inertia and max_inertia

    n, m = len(grid), len(grid[0])
    cost, pos, _, _ = uniformCostSearch(grid, is_terminal, is_valid)

    if pos == (n - 5, m - 1):
        return cost + sum(grid[i][m - 1] for i in range(n - 4, n))
    if pos == (n - 1, m - 5):
        return cost + sum(grid[n - 1][j] for j in range(m - 4, m))
    raise ValueError('Wrong end state', pos, cost)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    part_1()
    part_2()
