"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Iterator
from itertools import chain

from utils import transpose, section
from utils_types import Grid


def is_row_reflection(grid: Grid[str], row: int, smudge: bool = False) -> bool:
    """Whether the row is a reflection for the grid or not,
    where the given row is the first row of the reflection of the right part"""
    size = min(row, len(grid) - row)
    # left is in reverse order to compute similarities
    left = chain.from_iterable(grid[row - size:row][::-1])
    right = chain.from_iterable(grid[row:row + size])
    diffs = sum(l != r for l, r in zip(left, right))
    return diffs == int(smudge)


def find_row_reflection(grid: Grid[str], smudge: bool = False) -> int:
    """Find the number of row before a reflexion.
    There can be a smudge on mirrors and it has to have on point to correct."""
    for i, row in enumerate(grid):
        if i == 0:
            continue
        # find two contiguous and rows
        diffs = sum(a != b for a, b in zip(row, grid[i - 1]))
        if diffs == 0 or smudge and diffs == 1:
            if is_row_reflection(grid, row=i, smudge=smudge):
                return i
    return 0


def build_scenes(data: Iterator[str]) -> list[Grid[str]]:
    """Retrieve all the data to begin with."""
    scenes: list[Grid[str]] = [[]]
    for row in data:
        if not row:
            scenes.append([])
        else:
            scenes[-1].append(list(row))

    return scenes


@section(year=2023, day=13, part=1, sol=27300)
def part_1(data: Iterator[str]) -> int:
    """Code for section 1"""
    scenes, result = build_scenes(data), 0
    for scene in scenes:
        i = find_row_reflection(scene)
        j = find_row_reflection(transpose(scene))
        result += j + 100 * i

    return result


@section(year=2023, day=13, part=2, sol=29276)
def part_2(data: Iterator[str]) -> int:
    """Code for section 2"""
    scenes, result = build_scenes(data), 0
    for scene in scenes:
        i = find_row_reflection(scene, smudge=True)
        j = find_row_reflection(transpose(scene), smudge=True)
        result += j + 100 * i

    return result


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    part_1()
    part_2()
