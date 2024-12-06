from collections.abc import Iterator
from copy import deepcopy
from tqdm import tqdm
from aoc import section, load_input
from aoc.grid import Grid
from aoc.utils import Coordinate, Direction, Neighborhood

N, S, E, W = Neighborhood('c4')
TURN = {N: E, E: S, S: W, W: N}
REPR = {N: "^", S: "v", E: ">", W: '<'}
DIR = {v: k for k,v in REPR.items()}

class Loop(Exception): ...

def steps(data: Grid, pos: tuple[int, int], d: Direction):
    dim = abs(d[0])   # direction of the deplacement
    for k in range(*(pos[~dim]-1, -1, -1) if sum(d) < 0 else (pos[~dim]+1, data.shape[~dim], 1)):
        curr_pos = (pos[dim], k) if not dim else (k, pos[dim])
        yield curr_pos, data[curr_pos]


# def forward(grid: Grid[str], start: tuple[int, int], d: Direction) -> None:
#     for curr_pos, e in steps(grid, start, d):
#         if e == "#":
#             previous = Coordinate(curr_pos) - d
#             #grid[previous] = REPR[TURN[d]]
#             return forward(grid, previous, TURN[d])
#         grid[curr_pos] = REPR[d]
#     # reached a border of the grid

# def forward(grid: Grid[str], start: tuple[int, int], d: Direction) -> None:
#     pos = start
#     while True:
#         for curr_pos, e in steps(grid, pos, d):
#             if e == "#":
#                 pos , d = Coordinate(curr_pos) - d, TURN[d]
#                 break
#             else:
#                 grid[curr_pos] = REPR[d]
#         else:
#             return  # reached a border of the grid

def forward(grid: Grid[str], start: tuple[int, int], d: Direction, write=True) -> None:
    pos = start
    seen = set()
    while True:
        #print("here")
        for curr_pos, e in steps(grid, pos, d):
            if (h := (*curr_pos, *d)) in seen:
                raise Loop()
            if e in "#O":
                seen.add(h)
                pos , d = Coordinate(curr_pos) - d, TURN[d]
                break
            elif write:
                grid[curr_pos] = REPR[d]
        else:
            return # reached a border of the grid

def find_loops(grid: Grid[str], start: tuple[int, int], d: Direction) -> Iterator:
    pos = start
    while True:
        for curr_pos, e in steps(grid, pos, d):
            if e == "#":
                pos , d = Coordinate(curr_pos) - d, TURN[d]
                break

            # try putting obstacle
            if not grid.is_valid(obstacle := Coordinate(curr_pos) + d):
                return # reached a border of the grid
            if grid[obstacle] == "#": # natural obstacle, no loop
                continue

            try:
                #temp_grid = deepcopy(grid)
                grid[obstacle] = "O"
                forward(grid, curr_pos, TURN[d], write=False)
            except Loop:
                yield (*obstacle, *d)
            finally:
                grid[obstacle] = "."

            # continue path
            grid[curr_pos] = REPR[d]


@section.p1(sol=4722)
def part_1() -> int:
    """Code for section 1"""
    data = Grid([list(r) for r in load_input()])
    start = next((p for p, e in data.enumerate() if e == "^"))
    forward(data, start, d=N)
    print(str(data).replace(" ", ""))
    return sum(c in REPR.values() for _, c in data.enumerate())

# 1661, 1674, 1623, 1727
# 846 < 1807
@section.p2()
def part_2() -> int:
    """Code for section 2"""
    data = Grid([list(r) for r in load_input()])
    start = next((p for p, e in data.enumerate() if e == "^"))
    return len(set(find_loops(data, start, N)))

if __name__ == "__main__":
    part_1()
    part_2()
