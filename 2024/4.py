from aoc import section, load_input
from aoc.utils import Grid, Coordinate, enumerate_grid, grid_map, print_grid

WORD = "XMAS"
DIRS_DIAGS = [(1, 1) ,(-1, -1), (1, -1), (-1, 1)]
DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0), *DIRS_DIAGS]

def parse(data: list[str]) -> Grid[str]:
    """Parse input into ..."""
    return [list(d) for d in data]

def is_valid(grid, x, y):
    n,m= len(grid), len(grid[0])
    return 0 <= x < n and 0 <= y < m

def is_word(grid, pos, d: tuple, word=WORD) -> bool:
    x, y = pos
    i,j = d
    return all(is_valid(grid, a:=x+k*i, b:=y+k*j) and grid[a][b] == word[k] for k in range(len(word)))

@section.p1(sol=2427)
def part_1() -> int:
    """Code for section 1"""
    grid = parse(load_input())
    return sum(is_word(grid, pos, d)  for pos, c in enumerate_grid(grid) if c=="X" for d in DIRS)

def count_x_mas(grid, pos) -> int:
    (x, y) = pos
    return sum(is_word(grid, (x-di, y-dj), (di, dj), word="MAS") for di, dj in DIRS_DIAGS)

@section.p2(sol=1900)
def part_2() -> int:
    """Code for section 2"""
    grid = parse(load_input())
    return sum(count_x_mas(grid, pos) == 2  for pos, c in enumerate_grid(grid) if c=="A")


if __name__ == "__main__":
    part_1()
    part_2()
