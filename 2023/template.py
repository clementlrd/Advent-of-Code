"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Iterable
from utils import section

DAY = 0
TEST = True
VERBOSE = True


@section(year=2023, day=DAY, part=1, test=TEST)
def part_1(data: Iterable[str]) -> int:
    """Code for section 1"""
    if VERBOSE:
        print(*data, sep="\n")
    return 0


@section(year=2023, day=DAY, part=2, test=TEST)
def part_2(data: Iterable[str]) -> int:
    """Code for section 2"""
    if VERBOSE:
        print(*data, sep="\n")
    return 0


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    part_1()
    part_2()
