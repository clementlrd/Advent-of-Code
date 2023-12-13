"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Iterable
from utils import lines_of_file, print_answer
from utils import transpose, lmap
from utils_types import Grid

DAY = 13
PART = 1
TEST = False


def is_row_reflection(grid: Grid[str], row: int, smudge: bool = False) -> bool:
    size = min(row, len(grid) - row)
    left, right = grid[row - size:row], grid[row:row + size]

    if not smudge:
        return all(l == r for l, r in zip(left[::-1], right))

    smudge_found = False
    for l, r in zip(left[::-1], right):
        diffs = sum((a != b for a, b in zip(l, r)))
        if diffs == 1:
            # found a smudge
            if smudge_found:
                return False  # there is only one smudge
            smudge_found = True
        if diffs > 1:
            return False
    return smudge_found


def find_row_reflection(grid: Grid[str], smudge: bool = False) -> int:
    """Find the number of row before a reflexion.
    There can be a smudge on mirrors and it has to have on point to correct."""
    for i, row in enumerate(grid):
        if i == 0:
            continue
        diffs = sum((a != b for a, b in zip(row, grid[i - 1])))
        if diffs == 0 or smudge and diffs == 1:
            if is_row_reflection(grid, row=i, smudge=smudge):
                return i
    return 0


def get_data() -> list[Grid[str]]:
    """Retrieve all the data to begin with."""
    l = lines_of_file(f"inputs/{DAY if not TEST else 'test'}.txt")

    scenes: list[Grid[str]] = [[]]
    for row in l:
        if not row:
            scenes.append([])
        else:
            scenes[-1].append(list(row))

    return scenes


def part_1() -> None:
    """Code for section 1"""
    scenes = get_data()
    result = 0
    for scene in scenes:
        i = find_row_reflection(scene)
        j = find_row_reflection(transpose(scene))
        result += j + 100 * i

    print_answer(result, day=DAY, part=1)


def part_2() -> None:
    """Code for section 2"""
    scenes = get_data()
    result = 0
    for scene in scenes:
        i = find_row_reflection(scene, smudge=True)
        j = find_row_reflection(transpose(scene), smudge=True)
        result += j + 100 * i

    print_answer(result, day=DAY, part=2)


if __name__ == "__main__":
    part_1()  # P1:
    part_2()  # P2:
