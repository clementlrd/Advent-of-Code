"""Resolve a daily problem"""  # pylint: disable=invalid-name
from typing import Iterator
from utils import section, neighborhood

# TODO: refactor


@section(year=2023, day=3, part=1, sol=514969)
def part_1(data: Iterator[str]) -> int:
    """Code for section 1"""
    grid = list(data)
    part_numbers = []

    for i, row in enumerate(grid):
        current_number, is_part_number = "", False
        for j, c in enumerate(row):
            if not '0' <= c <= '9':
                if is_part_number and current_number:
                    # we leave a part number, thus we add it in teh list
                    part_numbers.append(int(current_number))
                # we make sur that we are not working on a number anymore
                current_number, is_part_number = "", False
                continue  # nothing to see here

            # we are in a number. keeping track of it
            current_number += c
            for vi, vj in neighborhood((i, j), mat_size=(len(grid), len(row)), connectivity=8):
                neighbor = grid[vi][vj]
                if '0' <= neighbor <= '9' or neighbor == '.':
                    # empty space or number, nothing to see here
                    continue
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

    part_numbers = []
    # keep track of the parts numbers linked to a gear
    gears_linked = {}

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
                    # we found a gear
                    gear = (vi, vj)
                    gears_linked.setdefault(gear, [])
                if '0' <= neighbor <= '9' or neighbor == '.':
                    # empty space or number
                    continue
                is_part_number = True

        if is_part_number and current_number:
            part_numbers.append(int(current_number))
            if gear is not None:
                gears_linked[gear].append(int(current_number))

    # gear ratios as two adjacent part numbers
    l = filter(lambda x: len(x) == 2, gears_linked.values())
    # gear ration is a multiplication of the two part numbers
    l = map(lambda x: x[0] * x[1], l)
    return sum(l)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    part_1()
    part_2()
