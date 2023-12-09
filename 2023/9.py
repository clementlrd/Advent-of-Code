"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Iterable, Any
from dataclasses import dataclass, field
from itertools import pairwise, starmap
import os
from utils import lines_of_file, lmap

DATA_PATH = "inputs/"
DAY = os.path.basename(__file__).split(".")[0]


@dataclass(slots=True)
class History:
    """A record of an history entry"""
    values: list[int]
    differences: list[list[int]] = field(init=False)

    def __post_init__(self) -> None:
        self.forward()

    def forward(self) -> None:
        """Compute all the differences"""
        self.differences = [self.values]
        while any(self.differences[-1]):
            new_diff = starmap(lambda x, y: y - x, pairwise(self.differences[-1]))
            self.differences.append(list(new_diff))

    def predict_next(self) -> int:
        """Extrapolate the next value"""
        last_values = (diffs[-1] for diffs in self.differences[::-1])
        predicted = 0
        for value in last_values:
            predicted = predicted + value
        return predicted

    def predict_before(self) -> int:
        """Extrapolate the first value"""
        first_values = (diffs[0] for diffs in self.differences[::-1])
        predicted = 0
        for value in first_values:
            predicted = value - predicted
        return predicted

    @staticmethod
    def from_str(string: str) -> History:
        """Create an History entry from a raw string"""
        return History(lmap(int, string.split(" ")))


def get_data() -> Iterable[History]:
    """Retrieve all the data to begin with."""
    l = lines_of_file(f"{DATA_PATH}{DAY}.txt")
    return map(History.from_str, l)


def part_1() -> None:
    """Code for section 1"""
    print_answer(sum(x.predict_next() for x in get_data()), part=1)


def part_2() -> None:
    """Code for section 2"""
    print_answer(sum(x.predict_before() for x in get_data()), part=2)


def print_answer(answer: Any, part: int, print_fn=print) -> None:
    """Shorthand to print answer."""
    print("=" * 50)
    print(f"[DAY {DAY}] Answer to part {part} is:\n\n\t")
    print_fn(answer)
    print("\n", "=" * 50, sep="")


if __name__ == "__main__":
    part_1()  # P1: 2008960228
    part_2()  # P2: 1097
