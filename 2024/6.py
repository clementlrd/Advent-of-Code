from collections.abc import Iterator
from copy import deepcopy
from aoc import section, load_input
from aoc.grid import Grid
from aoc.utils import Coordinate, Direction, Neighborhood

N, S, E, W = Neighborhood('c4')
TURN = {N: E, E: S, S: W, W: N}
REPR = {N: "^", S: "v", E: ">", W: '<'}

class Loop(Exception): ...

def steps(data: Grid, pos: tuple[int, int], d: Direction):
    dim = abs(d[0])   # direction of the deplacement
    for k in range(*(pos[~dim]-1, -1, -1) if sum(d) < 0 else (pos[~dim]+1, data.shape[~dim], 1)):
        curr_pos = (pos[dim], k) if not dim else (k, pos[dim])
        yield curr_pos, data[curr_pos]


def forward(grid: Grid[str], start: tuple[int, int], d: Direction) -> None:
    for curr_pos, e in steps(grid, start, d):
        if e == "#":
            previous = Coordinate(curr_pos) - d
            grid[previous] = REPR[TURN[d]]
            #x,y = curr_pos
            #print(grid.subgrid((x-2, y-2), (x+3, y+3)))
            return forward(grid, previous, TURN[d])
        if grid[curr_pos] == REPR[d]:
            raise Loop()
        if grid[curr_pos] == REPR[TURN[d]] and grid[Coordinate(curr_pos) + d] in "#O":
            raise Loop()
        #if grid[curr_pos] == REPR[-d] and grid[Coordinate(curr_pos) + d] in "#O" and grid[Coordinate(curr_pos) + TURN[d]] in "#O" and grid[Coordinate(curr_pos) - TURN[d]] == REPR[TURN[d]]:
        if grid[curr_pos] == REPR[-d] and grid[Coordinate(curr_pos) + d] in "#O" and ( grid[Coordinate(curr_pos) + TURN[d]] in "#O" or  grid[Coordinate(curr_pos) - TURN[d]] in "#O"):
            raise Loop()
        grid[curr_pos] = REPR[d]
    # reached a border of the grid

def find_loops(grid: Grid[str], start: tuple[int, int], d: Direction) -> Iterator[tuple[int, int]]:
    for curr_pos, e in steps(grid, start, d):
        assert e != "O"
        if e == "#":
            yield from find_loops(grid, Coordinate(curr_pos) - d, TURN[d])
            return
        # try putting an obstacle, do we create a loop ?
        obstacle = Coordinate(curr_pos) + d
        if not grid.is_valid(obstacle):
            return # reached a border of the grid
        if grid[obstacle] != "#": # make sur there is no natural obstacle
            try:
                if grid[curr_pos] == REPR[TURN[d]]:
                    raise Loop() # already been there 
                temp_grid = deepcopy(grid)
                temp_grid[curr_pos] = REPR[TURN[d]]
                temp_grid[obstacle] = "O"
                forward(temp_grid, curr_pos, TURN[d])
            except (Loop, RecursionError):
                yield obstacle

        if grid[curr_pos] == REPR[TURN[d]] and grid[Coordinate(curr_pos) + d] == "#":
            raise Loop()

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

# 1661, 1674
# 846 < 1807
@section.p2()
def part_2() -> int:
    """Code for section 2"""
    data = Grid([list(r) for r in load_input()])
    start = next((p for p, e in data.enumerate() if e == "^"))
    a = len(set(find_loops(data, start, N)))
    print(str(data).replace(" ", ""))
    return a

if __name__ == "__main__":
    part_1()
    part_2()
