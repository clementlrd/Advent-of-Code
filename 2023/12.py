"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Iterator
from functools import lru_cache
from dataclasses import dataclass
from utils import section, compose


@dataclass
class Record:
    """A record contains data on the condition of the springs,
    in particular the number of consecutive damaged springs."""
    springs: str
    group_sizes: tuple[int, ...]

    @classmethod
    def from_repr(cls, _repr: str) -> Record:
        """Create Record from raw string"""
        springs, group_sizes = _repr.split(" ")
        group_sizes = map(int, group_sizes.split(","))  # convert data to int
        return cls(springs, tuple(group_sizes))         # create record

    def unfold(self, n=5) -> Record:
        """Create a new Record object with a number `n` of unfolding."""
        springs = "?".join([self.springs] * n)  # duplicate n times and insert "?" between
        group_sizes = self.group_sizes * n      # duplicate n times the sizes
        return Record(springs, group_sizes)

    def count(self) -> int:
        """Count all the possible permutations for the unknown springs.
        It uses a recursive method."""

        @lru_cache(maxsize=None)
        def recursive_count(springs: str, group_sizes: tuple[int, ...]) -> int:
            """Recursive function to count the possible permutations
            based on the value of the first element.

            **Important:** It works because it uses caching !
            For a lot of calls, the value has already been calculated previously."""
            if springs == "":
                return len(group_sizes) == 0

            if group_sizes == ():
                return "#" not in springs

            count, e, gsize = 0, springs[0], group_sizes[0]

            if e in ".?":
                count += recursive_count(springs[1:], group_sizes)

            if e in "#?" and len(springs) >= gsize:
                consecutive_springs = "." not in springs[:gsize]
                has_group_size = len(springs) == gsize or springs[gsize] != "#"
                if consecutive_springs and has_group_size:
                    count += recursive_count(springs[gsize + 1:], group_sizes[1:])

            return count
        return recursive_count(self.springs, self.group_sizes)


@section(year=2023, day=12, part=1, sol=7236)
def part_1(data: Iterator[str]) -> int:
    """Code for section 1"""
    records = map(Record.from_repr, data)
    return sum(map(Record.count, records))


@section(year=2023, day=12, part=2, sol=11607695322318)
def part_2(data: Iterator[str]) -> int:
    """Code for section 2"""
    records = map(compose(Record.unfold, Record.from_repr), data)
    return sum(map(Record.count, records))


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    part_1()
    part_2()
