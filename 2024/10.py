from collections.abc import Iterator
from aoc import section, load_input
from aoc.grid import Grid
from aoc.utils import Neighborhood, Coordinate

def follow_path(grid: Grid[int], start: Coordinate) -> list[Coordinate]:
    """Returns all the coordinates of the peaks reached from the start, by a smooth, continuous increment.
    Warning: There can be duplicates if there is multiple paths."""
    assert grid[start] == 0

    def step(p: Coordinate) -> Iterator[Coordinate] :
        if grid[p] == 9:
            return iter((p,))
        return (q for d in Neighborhood('c4') if grid.is_valid(p + d) and grid[p + d] == grid[p] + 1 for q in step(p + d))

    return list(step(start))

@section.p1(sol=531)
def part_1() -> int:
    """Code for section 1"""
    grid = Grid.from_strings(load_input()).map(int)
    return sum(len(set(follow_path(grid, Coordinate(p)))) for p, e in grid.enumerate() if e == 0)


@section.p2(sol=1210)
def part_2() -> int:
    """Code for section 2"""
    grid = Grid.from_strings(load_input()).map(int)
    return sum(len(follow_path(grid, Coordinate(p))) for p, e in grid.enumerate() if e == 0)


if __name__ == "__main__":
    part_1()
    part_2()
