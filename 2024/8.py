from collections import defaultdict
from itertools import combinations

from aoc import section, load_input
from aoc.grid import Grid
from aoc.utils import Coordinate

def parse(data: list[str]):
    """Parse input into ..."""
    ...

@section.p1()
def part_1() -> int:
    """Code for section 1"""
    data = Grid.from_strings(load_input())
    antenas: dict[str, list[Coordinate]] = defaultdict(list)
    for pos, c in data.enumerate():
        if c != ".":
            antenas[c].append(Coordinate(pos))
    for c, positions in antenas.items():
        for a, b in combinations(positions, 2):
            d = (a - b)
            for p in ((a + d), (b - d)):
                if data.is_valid(p):
                    data[p] = "#"
    return sum( c == "#" for _, c in data.enumerate() )

@section.p2()
def part_2() -> int:
    """Code for section 2"""
    data = Grid.from_strings(load_input())
    antenas: dict[str, list[Coordinate]] = defaultdict(list)
    for pos, c in data.enumerate():
        if c != ".":
            antenas[c].append(Coordinate(pos))
    for c, positions in antenas.items():
        for a, b in combinations(positions, 2):
            d = (a - b)
            k = 0
            while data.is_valid(p := a + k * d):
                data[p] = "#"
                k += 1
            k = 0
            while data.is_valid(p := b - k * d):
                data[p] = "#"
                k += 1
            
    print(data)
    return sum( c == "#" for _, c in data.enumerate() )


if __name__ == "__main__":
    part_1()
    part_2()
