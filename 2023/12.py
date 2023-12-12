"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Iterable
from functools import lru_cache
from dataclasses import dataclass
from utils import lines_of_file, print_answer


@dataclass
class Record:
    """A record contains data on the condition of the springs,
    in particular the number of consecutive damaged springs."""
    springs: str
    group_sizes: tuple[int, ...]

    @staticmethod
    def from_str(row: str) -> Record:
        """Create Record from raw string"""
        springs, group_sizes = row.split(" ")
        group_sizes = map(int, group_sizes.split(","))  # convert data to int
        return Record(springs, tuple(group_sizes))      # create record

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


def get_data() -> Iterable[Record]:
    """Retrieve all the data to begin with."""
    return map(Record.from_str, lines_of_file("inputs/12.txt"))


def part_1() -> None:
    """Code for section 1"""
    l = get_data()
    arrangements = sum(map(Record.count, l))

    print_answer(arrangements, day=12, part=1)


def part_2() -> None:
    """Code for section 2"""
    l = map(Record.unfold, get_data())
    arrangements = sum(map(Record.count, l))

    print_answer(arrangements, day=12, part=2)


if __name__ == "__main__":
    part_1()  # P1: 7236
    part_2()  # P2: 11607695322318
