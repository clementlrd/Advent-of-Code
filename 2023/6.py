"""Resolve a daily problem"""  # pylint: disable=invalid-name
from typing import Iterator
from dataclasses import dataclass
import math
from numpy.polynomial import Polynomial
from utils import section


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


@section(year=2023, day=6, part=1, sol=840336)
def part_1(data: Iterator[str]) -> int:
    """Code for section 1"""
    # retrieve data and remove trailing whitespaces
    times = filter(None, next(data).split(' ')[1:])
    distances = filter(None, next(data).split(' ')[1:])

    total = 1
    for time_limit, record in zip(times, distances):
        r = Race(time_limit=int(time_limit), record=int(record))
        total *= r.nbr_beat_record()

    return total


@section(year=2023, day=6, part=2, sol=41382569)
def part_2(data: Iterator[str]) -> int:
    """Code for section 2"""
    # data needs in fact to be concatenated
    max_time = ''.join(next(data).split(' ')[1:])
    record = ''.join(next(data).split(' ')[1:])
    race = Race(int(max_time), int(record))   # create the race

    return race.nbr_beat_record()


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    part_1()
    part_2()
