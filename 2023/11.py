"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Iterator
from itertools import combinations, starmap
from utils import section, lmap, manhattan_distance, enumerate_grid, enumerate_cols
from utils_types import Grid, Coordinate


class Space:
    """Represents a chunck of space, with its galaxies and its expansion factor"""

    def __init__(self, grid: Grid[str], factor=2) -> None:
        self.factor = factor
        self.galaxies = {pos for pos, e in enumerate_grid(grid) if e == "#"}
        self.empty_rows = [i for i, row in enumerate(grid) if "#" not in row]
        self.empty_cols = [j for j, col in enumerate_cols(grid) if "#" not in col]

    def distance(self, g1: Coordinate, g2: Coordinate) -> int:
        """Compute distances inside the space,
        taking into account expansion factor between galaxies."""
        (i0, i1), (j0, j1) = lmap(sorted, zip(g1, g2))
        empty_row_between = sum((i0 < i < i1 for i in self.empty_rows))
        empty_col_between = sum((j0 < j < j1 for j in self.empty_cols))

        distance = manhattan_distance(g1, g2)
        # correct distance due to space expansion
        distance += (self.factor - 1) * (empty_col_between + empty_row_between)
        return distance

    def all_distances(self) -> int:
        """Compute all the distances between gaalxies"""
        distances = starmap(self.distance, combinations(self.galaxies, 2))
        return sum(distances)


@section(year=2023, day=11, part=1, sol=9545480)
def part_1(data: Iterator[str]) -> int:
    """Code for section 1"""
    grid = lmap(list, data)
    return Space(grid).all_distances()


@section(year=2023, day=11, part=2, sol=406725732046)
def part_2(data: Iterator[str]) -> int:
    """Code for section 2"""
    grid = lmap(list, data)
    return Space(grid, factor=1000000).all_distances()


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    part_1()
    part_2()
