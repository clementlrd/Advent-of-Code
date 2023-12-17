"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from queue import PriorityQueue
from utils import lines_of_file, section, grid_map, lmap
from utils_types import Grid, Coordinate

DAY = 17
TEST = False
VERBOSE = False

InputData = Grid[int]

directions = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'v': (1, 0)}
opposite = {'<': '>', '>': '<', '^': 'v', 'v': '^'}

# cost, pos, dir, inertia
SearchNode = tuple[int, Coordinate, str | None, int, str]


def Astar(grid: Grid[int], start: Coordinate = (0, 0)) -> int:
    """Performs A* search on the grid"""
    n, m = len(grid), len(grid[0])
    end = (n - 1, m - 1)
    L: PriorityQueue[SearchNode] = PriorityQueue()       # Fringe
    L.put((grid[start[0]][start[1]], start, None, 0, ""))
    seen: set[tuple[Coordinate, str | None, int]] = set()

    while not L.empty():
        cost, (i, j), d, inertia, acc = L.get()        # Select a state
        if (i, j) == end:   # Return on final state
            print(acc)
            return cost

        if d is not None and ((i, j), d, inertia) in seen:
            continue
        seen.add(((i, j), d, inertia))

        for new_d, (di, dj) in directions.items():
            ni, nj = i + di, j + dj
            if not (0 <= ni < n and 0 <= nj < m):
                continue   # outside grid
            if d is not None and new_d == opposite[d]:
                continue   # don't go back
            new_inertia = 1
            if d is not None and new_d == d:
                if inertia >= 3:
                    continue   # maximum inertia
                new_inertia = inertia + 1
            new_cost = cost + grid[ni][nj]

            if ((ni, nj), new_d, new_inertia) in seen:
                continue   # node already seen with a better cost
            L.put((new_cost, (ni, nj), new_d, new_inertia, acc + new_d))
    raise RuntimeError("No final State found")


def Astar2(grid: Grid[int], start: Coordinate = (0, 0)) -> int:
    """Performs A* search on the grid"""
    n, m = len(grid), len(grid[0])
    L: PriorityQueue[SearchNode] = PriorityQueue()       # Fringe
    L.put((grid[start[0]][start[1]], start, None, 0, ""))
    seen: set[tuple[Coordinate, str | None, int]] = set()

    while not L.empty():
        cost, (i, j), d, inertia, acc = L.get()        # Select a state
        if (i, j) == (n - 5, m - 1):   # Return on final state
            print(acc)
            return cost + sum((grid[ii][m - 1] for ii in range(n - 4, n)))
        if (i, j) == (n - 1, m - 5):   # Return on final state
            print(acc)
            return cost + sum((grid[n - 1][jj] for jj in range(m - 4, m)))

        if d is not None and ((i, j), d, inertia) in seen:
            continue
        seen.add(((i, j), d, inertia))

        for new_d, (di, dj) in directions.items():
            ni, nj = i + di, j + dj
            if not (0 <= ni < n and 0 <= nj < m):
                continue   # outside grid
            if d is not None and new_d == opposite[d]:
                continue   # don't go back
            new_inertia = 1
            if d is not None and new_d != d:
                if inertia < 4:
                    continue
            if d is not None and new_d == d:
                if inertia >= 10:
                    continue   # maximum inertia
                new_inertia = inertia + 1
            new_cost = cost + grid[ni][nj]
            if ((ni, nj), new_d, new_inertia) in seen:
                continue   # node already seen with a better cost
            L.put((new_cost, (ni, nj), new_d, new_inertia, acc + new_d))
    raise RuntimeError("No final State found")


def get_data() -> InputData:
    """Retrieve all the data to begin with."""
    grid = lmap(list, lines_of_file("inputs/17.txt"))  # convert to grid
    grid = grid_map(int, grid)                         # convert grid from str to int
    grid[0][0] = 0                                     # the starting position has no cost
    return grid


@section(day=DAY, part=1)
def part_1(data: InputData) -> int:
    """Code for section 1"""
    return Astar(data)


@section(day=DAY, part=2)
def part_2(data: InputData) -> int:
    """Code for section 2"""
    return Astar2(data)


if __name__ == "__main__":
    part_1(get_data())  # P1: 845
    part_2(get_data())  # P2: 993
