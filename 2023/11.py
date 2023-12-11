"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from itertools import combinations, starmap
from utils import lines_of_file, print_answer
from utils import lmap, manhattan_distance, enumerate_grid, enumerate_cols
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


def get_data() -> Grid[str]:
    """Retrieve all the data to begin with."""
    return lmap(list, lines_of_file("inputs/11.txt"))


def part_1() -> None:
    """Code for section 1"""
    total_distances = Space(get_data()).all_distances()
    print_answer(total_distances, day=11, part=1)


def part_2() -> None:
    """Code for section 2"""
    total_distances = Space(get_data(), factor=1000000).all_distances()
    print_answer(total_distances, day=11, part=2)


if __name__ == "__main__":
    part_1()  # P1: 9545480
    part_2()  # P2: 406725732046
