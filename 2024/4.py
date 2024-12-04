from aoc import section, load_input
from aoc.grid import Grid
from aoc.utils import Coordinate, Direction, Neighborhood


def is_word(grid: Grid, pos: Coordinate, d: Direction, word="XMAS") -> bool:
    return all(grid.is_valid(p := pos + k*d) and grid[p] == l for k, l in enumerate(word))


@section.p1(sol=2427)
def part_1() -> int:
    """Code for section 1"""
    grid = Grid([list(r) for r in load_input()])
    return sum(is_word(grid, Coordinate(pos), d)  for pos, c in grid.enumerate() if c=="X" for d in Neighborhood())


@section.p2(sol=1900)
def part_2() -> int:
    """Code for section 2"""
    grid = Grid([list(r) for r in load_input()])

    def count_x_mas(pos: Coordinate) -> int:
        return sum(is_word(grid, pos - d, d, word="MAS") for d in Neighborhood("cross"))
    
    return sum(count_x_mas(Coordinate(pos)) == 2  for pos, c in grid.enumerate() if c == "A")


if __name__ == "__main__":
    part_1()
    part_2()
