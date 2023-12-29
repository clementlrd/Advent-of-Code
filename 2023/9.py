"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Iterator
from dataclasses import dataclass, field
from itertools import pairwise, starmap
from utils import section, lmap


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
        # TODO: use predict next with reversed order
        first_values = (diffs[0] for diffs in self.differences[::-1])
        predicted = 0
        for value in first_values:
            predicted = value - predicted
        return predicted

    @staticmethod
    def from_str(string: str) -> History:
        """Create an History entry from a raw string"""
        return History(lmap(int, string.split(" ")))


@section(year=2023, day=9, part=1, sol=2008960228)
def part_1(data: Iterator[str]) -> int:
    """Code for section 1"""
    histories = map(History.from_str, data)
    return sum(x.predict_next() for x in histories)


@section(year=2023, day=9, part=2, sol=1097)
def part_2(data: Iterator[str]) -> int:
    """Code for section 2"""
    histories = map(History.from_str, data)
    return sum(x.predict_before() for x in histories)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    part_1()
    part_2()
