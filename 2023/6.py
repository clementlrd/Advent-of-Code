"""Resolve a daily problem"""  # pylint: disable=invalid-name
from typing import Iterable, Any
from dataclasses import dataclass
import os
import math
from numpy.polynomial import Polynomial
from utils import lines_of_file, lfilter, lmap

DATA_PATH = "inputs/"
DAY = os.path.basename(__file__).split(".")[0]


@dataclass
class Boat:
    """A boat with a loading time button."""
    loading_time: int

    @property
    def speed(self) -> int:
        """The speed of the boat, correspond to `loading_time/1 mm.ms-1`"""
        return self.loading_time

    def distance(self, time_limit: int) -> int:
        """Return the maximum distance (mm) for an amount of time (ms)"""
        return self.speed * (time_limit - self.loading_time)


@dataclass
class Race:
    """A race simulator to beat a record."""
    time_limit: int
    record: int

    def nbr_beat_record_naive(self) -> int:
        """The number of race that beat the record. naive version."""
        return sum(
            Boat(loading_time=t).distance(self.time_limit) > self.record
            for t in range(0, self.time_limit - 1)
        )

    def nbr_beat_record(self) -> int:
        """The number of race that beat the record"""
        t1, t2 = self.time_range_to_beat_record()
        return t2 - t1 + 1

    def time_range_to_beat_record(self) -> tuple[int, int]:
        """Loading time that beat the record is solution of a polynomial equation.
        More precisely, the loading time as to been between the roots of the polynomial."""
        p = Polynomial([-self.record, self.time_limit, -1])
        r1, r2 = p.roots()
        return (math.ceil(r1), math.floor(r2))


def get_data() -> Iterable[list[str]]:
    """Retrieve all the data to begin with."""
    l = lines_of_file(f"{DATA_PATH}{DAY}.txt")
    l = map(lambda x: lfilter(None, x.split(' ')[1:]), l)
    return l


def part_1() -> None:
    """Code for section 1"""
    l = map(lambda x: lmap(int, x), get_data())  # convert data to int

    total = 1
    for time_limit, record in zip(*l):
        r = Race(time_limit=time_limit, record=record)
        total *= r.nbr_beat_record()

    print_answer(total, part=1)


def part_2() -> None:
    """Code for section 2"""
    l = map(''.join, get_data())    # data needs in fact to be concatenated
    max_time, record = map(int, l)  # convert to int
    race = Race(max_time, record)   # create the race

    print_answer(race.nbr_beat_record(), part=2)


def print_answer(answer: Any, part, print_fn=print) -> None:
    """Shorthand to print answer."""
    print("=" * 50)
    print(f"[DAY {DAY}] Answer to part {part} is:\n\n\t")
    print_fn(answer)
    print("\n", "=" * 50, sep="")


if __name__ == "__main__":
    part_1()  # P1: 840336
    part_2()  # P2: 41382569
