"""Resolve a daily problem"""  # pylint: disable=invalid-name
from typing import Iterator
from collections import defaultdict

from utils import section, neighborhood
from utils_types import Coordinate


@section(year=2023, day=3, part=1, sol=514969)
def part_1(data: Iterator[str]) -> int:
    """Code for section 1"""
    grid, part_numbers = list(data), list[int]()

    for i, row in enumerate(grid):
        current_number, is_part_number = "", False
        for j, c in enumerate(row):
            if not '0' <= c <= '9':
                if is_part_number and current_number:
                    # we leave a part number, thus we add it in the list
                    part_numbers.append(int(current_number))
                # we make sur that we are not working on a number anymore
                current_number, is_part_number = "", False
                continue  # nothing to see here, we can continue

            # we are in a number. keeping track of it
            current_number += c
            for vi, vj in neighborhood((i, j), mat_size=(len(grid), len(row)), connectivity=8):
                if '0' <= (neighbor := grid[vi][vj]) <= '9' or neighbor == '.':
                    continue    # empty space or number, nothing to see here
                # a special character has been detected, it is a part number
                is_part_number = True

        # make sur to had a number which is at the end of a line
        if is_part_number and current_number:
            part_numbers.append(int(current_number))

    return sum(part_numbers)


@section(year=2023, day=3, part=2, sol=78915902)
def part_2(data: Iterator[str]) -> int:
    """Code for section 2"""
    grid = list(data)
    # keep track of the parts numbers linked to a gear (gears linked)
    part_numbers, gears_linked = list[int](), defaultdict[Coordinate, list[int]](list)

    for i, row in enumerate(grid):
        current_number, is_part_number, gear = "", False, None
        for j, c in enumerate(row):
            if not '0' <= c <= '9':
                if is_part_number and current_number:
                    part_numbers.append(int(current_number))
                    if gear is not None:
                        # we are around a gear, keep track of the part number
                        gears_linked[gear].append(int(current_number))
                current_number, is_part_number, gear = "", False, None
                continue

            current_number += c
            for vi, vj in neighborhood((i, j), mat_size=(len(grid), len(row)), connectivity=8):
                neighbor = grid[vi][vj]
                if neighbor == "*":
                    gear = (vi, vj)   # we found a gear
                if '0' <= neighbor <= '9' or neighbor == '.':
                    continue          # empty space or number
                is_part_number = True

        # make sur to had a number which is at the end of a line
        if is_part_number and current_number:
            part_numbers.append(int(current_number))
            if gear is not None:
                gears_linked[gear].append(int(current_number))

    # gear ratios has two adjacent part numbers
    gear_ratios = filter(lambda x: len(x) == 2, gears_linked.values())
    # gear ratios is a multiplication of the two part numbers
    return sum(x1 * x2 for x1, x2 in gear_ratios)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    part_1()
    part_2()
