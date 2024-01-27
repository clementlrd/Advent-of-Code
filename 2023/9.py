"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Iterator
from dataclasses import dataclass
from itertools import pairwise, starmap
from functools import reduce
from operator import add

from utils import section, lmap


@dataclass(frozen=True, slots=True)
class History:
    """A record of an history entry"""
    values: list[int]

    def forward(self) -> list[list[int]]:
        """Compute all the differences"""
        differences = [self.values]
        while any(differences[-1]):
            # add a new layer of differences
            new_diff = starmap(lambda x, y: y - x, pairwise(differences[-1]))
            differences.append(list(new_diff))
        return differences

    def predict_next(self) -> int:
        """Extrapolate the next value"""
        last_values = (diffs[-1] for diffs in self.forward()[::-1])
        return reduce(add, last_values)

    def predict_before(self) -> int:
        """Extrapolate the first value"""
        first_values = (diffs[0] for diffs in self.forward()[::-1])
        return reduce(lambda pred, v: v - pred, first_values)

    @classmethod
    def from_repr(cls, _repr: str) -> History:
        """Create an History entry from a raw string"""
        return cls(lmap(int, _repr.split(" ")))


@section(year=2023, day=9, part=1, sol=2008960228)
def part_1(data: Iterator[str]) -> int:
    """Code for section 1"""
    histories = map(History.from_repr, data)
    return sum(x.predict_next() for x in histories)


@section(year=2023, day=9, part=2, sol=1097)
def part_2(data: Iterator[str]) -> int:
    """Code for section 2"""
    histories = map(History.from_repr, data)
    return sum(x.predict_before() for x in histories)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    part_1()
    part_2()
