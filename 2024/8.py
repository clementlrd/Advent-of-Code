from collections import defaultdict
from itertools import combinations

from aoc import section, load_input
from aoc.grid import Grid
from aoc.utils import Coordinate

def get_antenas(grid: Grid[str]) -> dict[str, list[Coordinate]]:
    antennas = defaultdict(list)
    for pos, c in grid.enumerate():
        if c != ".":
            antennas[c].append(Coordinate(pos))
    return antennas

def antenna_pairs(antennas):
    return ((a, b) for positions in antennas.values() for a, b in combinations(positions, 2))


@section.p1(sol=348)
def part_1() -> int:
    """Code for section 1"""
    data = Grid.from_strings(load_input())
    antennas = get_antenas(data)
    for a, b in antenna_pairs(antennas):
        d = (a - b)
        for p in ((a + d), (b - d)):
            if data.is_valid(p):
                data[p] = "#"
    return sum( c == "#" for c in data )


@section.p2(sol=1221)
def part_2() -> int:
    """Code for section 2"""
    data = Grid.from_strings(load_input())
    antennas = get_antenas(data)
    for a, b in antenna_pairs(antennas):
        for fn in (lambda d: a + d, lambda d: b - d):
            k = 0
            while data.is_valid(p := fn(k * (a - b))):
                data[p] = "#"
                k += 1
    return sum( c == "#" for c in data )


if __name__ == "__main__":
    part_1()
    part_2()
