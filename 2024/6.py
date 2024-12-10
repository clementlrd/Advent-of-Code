from multiprocess.pool import Pool
from copy import deepcopy
from aoc import section, load_input
from aoc.grid import Grid
from aoc.utils import Coordinate, Direction, Neighborhood

N, S, E, W = Neighborhood('c4')
TURN = {N: E, E: S, S: W, W: N}
REPR = {N: "^", S: "v", E: ">", W: '<'}

class Loop(Exception): ...


def forward(grid: Grid[str], start: tuple[int, int], d: Direction, write=True) -> None:
    pos = Coordinate(start)
    seen = set()
    while grid.is_valid(pos + d):
        if (pos + d, d) in seen:
            raise Loop()

        if grid[pos + d] in "#O":
            seen.add((pos + d, d))
            d = TURN[d]
        elif grid[pos + d] in ".<^>v":
            pos += d
        else:
            raise ValueError(grid[pos + d])

        if write:
            grid[pos] = REPR[d]


@section.p1(sol=4722)
def part_1() -> int:
    """Code for section 1"""
    data = Grid([list(r) for r in load_input()])
    start = next((p for p, e in data.enumerate() if e == "^"))
    forward(data, start, d=N)
    print(str(data).replace(" ", ""))
    return sum(c in REPR.values() for _, c in data.enumerate())


@section.p2(sol=1602)
def part_2() -> int:
    """Code for section 2"""
    data = Grid([list(r) for r in load_input()])
    start = next((p for p, e in data.enumerate() if e == "^"))
    path = deepcopy(data)
    forward(path, start, N)

    def is_loop(pos) -> bool:
        try:
            data[pos] = "O"  # try obstacle
            forward(data, start, N, write=False)
        except Loop:
            return True
        finally:
            data[pos] = "."  # revert obstacle
        return False

    path_pos = [p for p, e in path.enumerate() if e in REPR.values() if p != start]
    pool = Pool()  # note: I don't know why it works as I update the same grid for the forward
    return sum(pool.map(is_loop, path_pos))


if __name__ == "__main__":
    part_1()
    part_2()
