"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Iterable
from utils import lines_of_file, print_answer

DAY = 0
PART = 1
TEST = True


def get_data() -> Iterable[str]:
    """Retrieve all the data to begin with."""
    l = lines_of_file(f"inputs/{DAY if not TEST else 'test'}.txt")
    return l


def part_1() -> None:
    """Code for section 1"""
    l = get_data()

    print_answer(None, day=DAY, part=1)


def part_2() -> None:
    """Code for section 2"""
    l = get_data()

    print_answer(None, day=DAY, part=2)


if __name__ == "__main__":
    part_1()  # P1:
    part_2()  # P2:
