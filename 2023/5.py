"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Iterator
from dataclasses import dataclass, field
from queue import LifoQueue
from functools import reduce
from itertools import chain
from more_itertools import batched
from utils import section, lmap


@dataclass
class Range:
    """A range object, contains a begin and an end"""
    start: int
    end: int

    @staticmethod
    def from_step(start: int, steps: int) -> Range:
        """Create a range object using steps instead of the end"""
        return Range(start=start, end=start + steps - 1)


@dataclass
class MapRange:
    """It is an object that can map a source value into a destination value
    if it is inside the range."""
    src: int
    dest: int
    steps: int

    def __contains__(self, src: int) -> bool:
        """Check if the src is inside the range"""
        return self.src <= src <= self.src + self.steps - 1

    def apply(self, src: int) -> int:
        """Transform the src into the corresponding destination (apply)"""
        if src not in self:
            raise ValueError
        return self.dest + src - self.src


@dataclass
class Map:
    """An object representing a Map.
    It is composed of multiples ranges that map a source to a destination."""
    ranges: list[MapRange] = field(init=False, default_factory=list)

    @property
    def empty(self) -> bool:
        """Check whether the map object is empty"""
        return len(self.ranges) == 0

    def map(self, src: int) -> int:
        """Map a source to a destination.
        Return the source if there is no corresponding ranges."""
        for r in self.ranges:
            if src in r:
                return r.apply(src)
        return src

    def map_range(self, src: Range) -> Iterator[Range]:
        """Transform a whole Range object of source into its corresponding
        Range object of destination. A unique Range of source can create
        multiple range objects in the destination."""
        queue = LifoQueue()
        queue.put(src)
        while not queue.empty():
            curr: Range = queue.get()
            for r in self.ranges:
                if curr.start in r and curr.end not in r:
                    # only the start of the current range is inside the MapRange
                    start, end = curr.start, r.src + r.steps - 1
                    yield Range(start=r.apply(start), end=r.apply(end))
                    queue.put(Range(start=end + 1, end=curr.end))

                elif curr.start not in r and curr.end in r:
                    # only the end of the current range is inside the MapRange
                    start, end = r.src, curr.end
                    yield Range(start=r.apply(start), end=r.apply(end))
                    queue.put(Range(start=curr.start, end=start - 1))

                elif curr.start in r and curr.end in r:
                    # the range is totally include in the MapRange
                    yield Range(start=r.apply(curr.start), end=r.apply(curr.end))

                elif curr.start <= r.src and r.src + r.steps - 1 <= curr.end:
                    # the MapRange is totally include in the range.
                    if curr.start != r.src:
                        queue.put(Range(start=curr.start, end=r.src - 1))
                    if r.src + r.steps - 1 != curr.end:
                        queue.put(Range(start=r.src + r.steps, end=curr.end))
                    yield Range(start=r.dest, end=r.dest + r.steps - 1)

                else:
                    # the range has nothing to do with this MapRange
                    continue

                break
            else:
                # no update made, the range is not in the Map
                yield curr


def generate_maps(data: Iterator[str]) -> Iterator[Map]:
    """Generate map objects from data."""
    curr = Map()
    for row in data:
        if "map:" in row:
            # the row starts a new map, yield the previous one
            if not curr.empty:
                yield curr
            curr = Map()
        elif row:
            # the row describe a range: we retrieve de data
            dest, src, steps = map(int, row.split(' '))
            # we add the map range to the last map
            curr.ranges.append(
                MapRange(dest=dest, src=src, steps=steps)
            )
    yield curr


@section(year=2023, day=5, part=1, sol=382895070)
def part_1(data: Iterator[str]) -> int:
    """Code for section 1"""
    seeds = lmap(int, next(data).split(": ")[1].split(" "))
    maps = generate_maps(data)

    # TODO: use reduce
    values = seeds
    for m in maps:
        values = map(m.map, values)

    return min(values)


@section(year=2023, day=5, part=2, sol=17729182)
def part_2(data: Iterator[str]) -> int:
    """Code for section 2"""
    seeds = lmap(int, next(data).split(": ")[1].split(" "))
    maps = generate_maps(data)

    ranges = (
        Range.from_step(start=start, steps=length)
        for start, length in batched(seeds, 2)  # type: ignore
    )

    for m in maps:
        ranges = map(m.map_range, ranges)
        ranges = reduce(chain, ranges)

    return min(x.start for x in ranges)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    part_1()
    part_2()
