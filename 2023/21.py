"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from utils import lines_of_file, section, lmap, print_grid, neighborhood
from utils_types import Coordinate, Grid

DAY = 21
TEST = False

InputData = Grid[str]


def get_data() -> InputData:
    """Retrieve all the data to begin with."""
    l = lines_of_file(f"inputs/{DAY if not TEST else 'test'}.txt")
    return lmap(list, l)


def naive_steps(grid: Grid[str], max_depth: int = 64) -> int:
    """Compute all the steps the Elf gardener can make."""
    n, m = len(grid), len(grid[0])
    start = [(i, j) for i, row in enumerate(grid) for j, e in enumerate(row) if e == 'S'][0]
    current_positions = set[Coordinate]((start,))
    for _ in range(max_depth):
        new_positions = set[Coordinate]()
        while len(current_positions) > 0:
            for ni, nj in neighborhood(current_positions.pop(), (n, m), connectivity=4):
                if grid[ni][nj] == '#':
                    continue
                new_positions.add((ni, nj))
        current_positions = new_positions

    for ni, nj in current_positions:
        grid[ni][nj] = 'O'
    print_grid(grid)
    return len(current_positions)


@section(day=DAY, part=1)
def part_1(data: InputData) -> int:
    """Code for section 1"""
    return naive_steps(data)


@section(day=DAY, part=2)
def part_2(data: InputData) -> int:
    """Code for section 2"""
    # max-depth = 26501365
    return 0


if __name__ == "__main__":
    part_1(get_data())  # P1: 3542
    part_2(get_data())  # P2:
