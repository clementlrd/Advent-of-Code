"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Iterable
from utils import lines_of_file, section

DAY = 0
TEST = True

InputData = Iterable[str]


def get_data() -> InputData:
    """Retrieve all the data to begin with."""
    l = lines_of_file(f"inputs/{DAY if not TEST else 'test'}.txt")
    return l


@section(day=DAY, part=1)
def part_1(data: InputData) -> int:
    """Code for section 1"""
    print(*data, sep="\n")
    return 0


@section(day=DAY, part=2)
def part_2(data: InputData) -> int:
    """Code for section 2"""
    print(*data, sep="\n")
    return 0


if __name__ == "__main__":
    part_1(get_data())  # P1:
    part_2(get_data())  # P2:
