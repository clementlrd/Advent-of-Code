"""Resolve a daily problem"""  # pylint: disable=invalid-name
from typing import Iterable, Callable, Optional, Any
# pylint: disable-next=unused-import
from dataclasses import dataclass, field
import os
import __main__
# import numpy as np
from utils import lines_of_file, lfilter, lmap
from functools import reduce

DATA_PATH = "inputs/"
DAY = os.path.basename(__file__).split(".")[0]
PART = 2
TEST = False


@dataclass
class Boat:
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
    time_limit: int
    record: int

    def nbr_beat_record(self) -> int:
        return sum(
            Boat(loading_time=t).distance(self.time_limit) > self.record
            for t in range(0, self.time_limit - 1)
        )


def get_data() -> Iterable[list[int]]:
    """Retrieve all the data to begin with."""
    l = lines_of_file(f"{DATA_PATH}{DAY if not TEST else 'test'}.txt")
    l = map(lambda x: lfilter(None, x.split(' ')[1:]), l)
    l = map(lambda x: lmap(int, x), l)
    return list(l)


def part_1() -> None:
    """Code for section 1"""
    max_time, record = get_data()
    races = map(lambda x: Race(x[0], x[1]), zip(max_time, record))
    l = map(lambda x: x.nbr_beat_record(), races)

    print_answer(reduce(lambda x, y: x * y, l))


def part_2() -> None:
    """Code for section 2"""
    max_time, record = get_data()
    max_time = int(reduce(lambda x, y: x + y, map(str, max_time)))
    record = int(reduce(lambda x, y: x + y, map(str, record)))
    race = Race(max_time, record)

    print_answer(race.nbr_beat_record())


def main(fn: Optional[Callable[[], None]] = None) -> None:
    """Main process"""
    if fn is not None:
        return fn()
    ex = vars(__main__)[f"part_{PART}"]
    return ex()


def print_answer(answer: Any, part=PART, print_fn=print) -> None:
    """Shorthand to print answer."""
    print("=" * 50)
    print(f"[DAY {DAY}] Answer to part {part} is:\n\n\t")
    print_fn(answer)
    print("\n", "=" * 50, sep="")


if __name__ == "__main__":
    main()
