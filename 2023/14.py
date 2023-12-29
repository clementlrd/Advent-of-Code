"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Iterator
import re
from itertools import pairwise, starmap
from collections import Counter
from utils import section
from utils import lmap, transpose, rotate90, compose
from utils_types import Grid


def tilt_north(grid: Grid[str]) -> Grid[str]:
    """Tilte all the round rocks to the north"""
    grid = transpose(grid)        # easier to work with transpose
    tilted_grid, n = [], len(grid)
    for row in grid:
        # gather square rock indexes
        rock_indexes = [j for j, e in enumerate(row) if e == "#"]
        # create segments to work on
        segments = pairwise([-1] + rock_indexes + [n])
        # keep only non empty segments
        segments = filter(lambda x: x[1] - x[0] > 2, segments)

        new_row = row.copy()
        for j0, j1 in segments:
            r = slice(j0 + 1, j1)           # range between rocks
            c = Counter(row[r])
            # replace segment with tilted rocks
            new_row[r] = list("O" * c['O'] + "." * c['.'])
        tilted_grid.append(new_row)
    return transpose(tilted_grid)     # revert original transpose


def tilt_cycle(grid: Grid[str]) -> Grid[str]:
    """Tilte all the round rocks in all four directions as a cycle (N, W, S, E)"""
    return compose(rotate90, tilt_north, repeat=4)(grid)


def total_load(grid: Grid[str]) -> int:
    """Compute total load metric as the sum of the rock distances from bottom."""
    def row_load(i, row) -> int:
        # distance from bottom times the number of round rocks
        return (len(grid[0]) - i) * Counter(row)["O"]

    return sum(starmap(row_load, enumerate(grid)))


@section(year=2023, day=14, part=1, sol=105208)
def part_1(data: Iterator[str]) -> int:
    """Code for section 1"""
    grid = lmap(list, data)
    return compose(total_load, tilt_north)(grid)


@section(year=2023, day=14, part=2, sol=102943)
def part_2(data: Iterator[str]) -> int:
    """Code for section 2"""
    grid = lmap(list, data)
    remaining_steps = 1_000_000_000

    # use regex to find a repeting sequence at the end
    regex = re.compile(r'(.+ .+) (\1)$')
    # the size of the numbers the regex will be looking at
    regex_window = 100
    loads, cycle = [], -1
    for i in range(remaining_steps):
        grid = tilt_cycle(grid)
        loads.append(total_load(grid))
        if i % 100 == 0:
            # look for a repeting sequence every 100 steps
            match = regex.search(" ".join(map(str, loads[-regex_window:])))
            if match is None:
                continue
            remaining_steps -= i + 1         # update with the number of steps
            cycle = len(match.group(1).split(" ")) // 2  # retrieve cycle size
            break

    # execute remaining steps (cutoff cycles with modulo)
    ex_remaining_cycles = compose(tilt_cycle, repeat=remaining_steps % cycle)

    return compose(total_load, ex_remaining_cycles)(grid)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    part_1()
    part_2()
