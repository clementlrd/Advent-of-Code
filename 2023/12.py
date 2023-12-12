"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Iterable, Literal, Self
from more_itertools import distinct_permutations
from utils import lines_of_file, print_answer
from tqdm import tqdm

DAY = 12
TEST = False

SpringCondition = Literal[".", "#", '?']


class ConditionRecord:

    def __init__(self, springs: Iterable[SpringCondition], continuous: Iterable[int]) -> None:
        self.springs = list(springs)
        self.continuous = list(continuous)

    @staticmethod
    def from_str(row: str) -> ConditionRecord:
        """Create Record from raw string"""
        springs, continuous = row.split(" ")
        return ConditionRecord(springs, map(int, continuous.split(",")))

    def unfold(self, n=5) -> Self:
        self.springs *= n
        self.continuous *= n
        return self

    def arrangements(self) -> int:
        missing_conds = [i for i, s in enumerate(self.springs) if s == "?"]
        n_missing_damaged = sum(self.continuous) - sum(s == "#" for s in self.springs)
        n_missing_operational = len(missing_conds) - n_missing_damaged

        n_arrangements = 0
        for seq in distinct_permutations("." * n_missing_operational + "#" * n_missing_damaged):
            new_spring = self.springs.copy()
            for i, e in zip(missing_conds, seq):
                new_spring[i] = e

            # group damaged springs
            damaged_group = []
            for i, e in enumerate(new_spring):
                if e == "#":
                    if i == 0 or new_spring[i - 1] == ".":
                        damaged_group.append(1)
                    else:
                        damaged_group[-1] += 1

            # compare to record
            if tuple(damaged_group) == tuple(self.continuous):
                n_arrangements += 1
        return n_arrangements


def get_data() -> Iterable[ConditionRecord]:
    """Retrieve all the data to begin with."""
    l = lines_of_file(f"inputs/{DAY if not TEST else 'test'}.txt")
    return map(ConditionRecord.from_str, l)


def part_1() -> None:
    """Code for section 1"""
    l = get_data()
    arrangements = sum(r.arrangements() for r in l)

    print_answer(arrangements, day=DAY, part=1)


def part_2() -> None:
    """Code for section 2"""
    l = get_data()
    # arrangements = sum(r.unfold().arrangements() for r in l)
    arrangements = 0
    for r in tqdm(list(l)):
        arrangements += r.unfold().arrangements()

    print_answer(arrangements, day=DAY, part=2)


if __name__ == "__main__":
    part_1()  # P1: 7236
    part_2()  # P2:
