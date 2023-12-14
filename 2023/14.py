"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
import re
from itertools import pairwise
from collections import Counter
from utils import lines_of_file, print_answer
from utils import lmap, transpose, rotate90
from utils_types import Grid


def tilte_north(grid: Grid[str]) -> Grid[str]:
    """Tilte all the round rocks to the north"""
    grid = transpose(grid)               # easier to work with transpose
    tilted_grid, n = [], len(grid)
    for row in grid:
        # gather square rock indexes
        rock_indexes = [j for j, e in enumerate(row) if e == "#"]
        # create segments to work on
        segments = pairwise([-1] + rock_indexes + [n])
        # keep only non empty segments
        segments = filter(lambda x: x[1] - x[0] > 1, segments)

        new_row = row.copy()
        for j0, j1 in segments:
            r = slice(j0 + 1, j1)                        # range between rocks
            c = Counter(row[r])
            # replace segment with tilted rocks
            new_row[r] = list("O" * c['O'] + "." * c['.'])
        tilted_grid.append(new_row)
    return transpose(tilted_grid)   # revert original transpose


def tilte_cycle(grid: Grid[str]) -> Grid[str]:
    """Tilte all the round rocks in all four directions as a cycle (N, W, S, E)"""
    for _ in range(4):
        grid = rotate90(tilte_north(grid))
    return grid


def total_load(grid: Grid[str]) -> int:
    """Compute total load metric as the sum of the rock distances from bottom."""
    m = len(grid[0])
    return sum(((m - i) * Counter(row)["O"] for i, row in enumerate(grid)))


def get_data() -> Grid[str]:
    """Retrieve all the data to begin with."""
    return lmap(list, lines_of_file("inputs/14.txt"))


def part_1() -> None:
    """Code for section 1"""
    print_answer(total_load(tilte_north(get_data())), day=14, part=1)


def part_2() -> None:
    """Code for section 2"""
    l = get_data()
    remaining_steps = 1_000_000_000

    # use regex to find a repeting sequence at the end
    regex = re.compile(r'(.+ .+) (\1)$')
    # the size of the numbers the regex will be looking at
    regex_window = 100
    loads, cycle = [], -1
    for i in range(remaining_steps):
        l = tilte_cycle(l)
        loads.append(total_load(l))
        if i % 100 == 0:
            # look for a repeting sequence every 100 steps
            match = regex.search(" ".join(map(str, loads[-regex_window:])))
            if match is None:
                continue
            remaining_steps -= i + 1         # update with the number of steps
            cycle = len(match.group(1).split(" ")) // 2  # retrieve cycle size
            break

    # execute remaining steps (cutoff cycles with modulo)
    for _ in range(remaining_steps % cycle):
        l = tilte_cycle(l)

    print_answer(total_load(l), day=14, part=2)


if __name__ == "__main__":
    part_1()  # P1: 105208
    part_2()  # P2: 102943
