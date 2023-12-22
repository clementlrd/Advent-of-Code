"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Optional
from queue import Queue
from copy import deepcopy
from utils import lines_of_file, section, lmap, neighborhood, enumerate_grid, print_grid
from utils_types import Coordinate, Grid

VERBOSE = True

InputData = Grid[str]


def get_data() -> InputData:
    """Retrieve all the data to begin with."""
    return lmap(list, lines_of_file("inputs/21.txt"))  # create grid


def bfs_steps(grid: Grid[str], max_depth: int, start: Optional[Coordinate] = None) -> int:
    """Compute all the steps the elf gardener can make from a starting position.
    Default: start is the 'S' tile in the center.

    BFS on a graph: keep only postions whose depth as the same parity than `max_depth`."""
    n, m = len(grid), len(grid[0])
    if start is None:
        start = [p for p, e in enumerate_grid(grid) if e == 'S'][0]

    final_positions = set[Coordinate]()
    queue = Queue[tuple[Coordinate, int]]()  # keep depth
    queue.put((start, 0))
    seen = set[Coordinate]()
    while not queue.empty():
        pos, depth = queue.get()

        if depth > max_depth or pos in seen:
            continue
        seen.add(pos)

        if depth % 2 == max_depth % 2:
            final_positions.add(pos)  # will be a valid position when max_depth is reached

        for ni, nj in neighborhood(pos, (n, m), connectivity=4):
            if grid[ni][nj] == '#' or (ni, nj) in seen:
                continue
            queue.put(((ni, nj), depth + 1))

    if VERBOSE:
        with open('visualisations/21.txt', "w", encoding="utf-8") as f:
            str_grid = deepcopy(grid)
            for ni, nj in final_positions:
                if (ni, nj) != (65, 65):
                    str_grid[ni][nj] = 'O'
            print_grid(str_grid, f, join='')

    return len(final_positions)


@section(day=21, part=1)
def part_1(grid: InputData) -> int:
    """Code for section 1"""
    return bfs_steps(grid, max_depth=64)


@section(day=21, part=2)
def part_2(grid: InputData) -> int:
    """Code for section 2

    I help myself with some coments:
    - [explaination](https://github.com/villuna/aoc23/wiki/A-Geometric-solution-to-advent-of-code-2023,-day-21)
    - [viz](https://raw.githubusercontent.com/democat3457/AdventOfCode/master/2023/resources/day21gridvis.png)

    It was also possible to do it with a polynomial equation,
    but it seemed a little too obscure to me.
    """
    n = (26501365 - 65) // 131

    full_even = bfs_steps(grid, max_depth=130)
    full_odd = bfs_steps(grid, max_depth=131)

    big_odd_corners = {
        'TR': bfs_steps(grid, max_depth=130 + 65, start=(130, 0)),
        'TL': bfs_steps(grid, max_depth=130 + 65, start=(130, 130)),
        'BR': bfs_steps(grid, max_depth=130 + 65, start=(0, 0)),
        'BL': bfs_steps(grid, max_depth=130 + 65, start=(0, 130)),
    }

    small_even_corners = {
        'TR': bfs_steps(grid, max_depth=64, start=(130, 0)),
        'TL': bfs_steps(grid, max_depth=64, start=(130, 130)),
        'BR': bfs_steps(grid, max_depth=64, start=(0, 0)),
        'BL': bfs_steps(grid, max_depth=64, start=(0, 130)),
    }

    mids = {
        'T': bfs_steps(grid, max_depth=131, start=(131, 65)),
        'L': bfs_steps(grid, max_depth=131, start=(65, 131)),
        'R': bfs_steps(grid, max_depth=131, start=(65, -1)),
        'B': bfs_steps(grid, max_depth=131, start=(-1, 65)),
    }

    return n**2 * full_even \
        + (n - 1)**2 * full_odd \
        + (n - 1) * sum(big_odd_corners.values()) \
        + n * sum(small_even_corners.values()) \
        + sum(mids.values())


if __name__ == "__main__":
    part_1(get_data())  # P1: 3542
    VERBOSE = False
    part_2(get_data())  # P2: 593174122420825
