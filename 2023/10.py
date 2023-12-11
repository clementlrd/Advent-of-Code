"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Callable, Optional, Any, Iterator, TypeVar
from dataclasses import dataclass, field
from queue import Queue
import os
from more_itertools import flatten
from utils import lines_of_file, lmap, neighborhood

DATA_PATH = "inputs/"
DAY = os.path.basename(__file__).split(".")[0]
VERBOSE = True


@dataclass
class Tile:
    """Represents the sides of the pipe in a Tile"""
    N: bool = False
    S: bool = False
    W: bool = False
    E: bool = False
    start: bool = False

    @staticmethod
    def from_char(char: str) -> Tile:
        """Create a Tile from its char representation"""
        if char == '|':
            return Tile(N=True, S=True)
        if char == '-':
            return Tile(E=True, W=True)
        if char == 'L':
            return Tile(N=True, E=True)
        if char == 'J':
            return Tile(N=True, W=True)
        if char == '7':
            return Tile(W=True, S=True)
        if char == 'F':
            return Tile(E=True, S=True)
        if char == 'S':
            return Tile(start=True, N=True, S=True, W=True, E=True)
        if char == '.':
            return Tile()
        raise ValueError


@dataclass
class PipeNode:
    """Represents a Pipe on the grid. Know its neighbors."""
    pos: tuple[int, int]
    tile: Tile
    connected_pipes: list[tuple[int, int]] = field(init=False, default_factory=list)
    depth: Optional[int] = field(init=False, default=None)

    def _add_neighbor(self, pos: tuple[int, int]) -> None:
        self.connected_pipes.append(pos)

    def connect(self, grid: Grid[PipeNode]) -> None:
        """Connect the pipe node to its neighbors"""
        n, m = len(grid), len(grid[0])
        (i, j), tile = self.pos, self.tile
        for (ni, nj) in neighborhood(self.pos, (n, m), connectivity=4):
            next_tile = grid[ni][nj].tile

            upper = i - ni == 1 and tile.N and next_tile.S
            under = ni - i == 1 and tile.S and next_tile.N
            left = j - nj == 1 and tile.W and next_tile.E
            right = nj - j == 1 and tile.E and next_tile.W

            if upper or under or left or right:
                # add to neigbors only if they are connected
                self._add_neighbor((ni, nj))


def enumerate_grid(grid: list[list[Any]]) -> Iterator[tuple[tuple[int, int], Any]]:
    """Enumerate over a grid, yield an element along with its position"""
    for i, row in enumerate(grid):
        for j, e in enumerate(row):
            yield (i, j), e


T = TypeVar('T')
S = TypeVar('S')
Grid = list[list[T]]


def grid_map(fn: Callable[[tuple[int, int], T], S], grid: Grid[T]) -> Grid[S]:
    """Map a function over a grid. The function needs to take the position and the element as input.
    It returns a new grid."""
    return [[fn((i, j), e) for j, e in enumerate(row)] for i, row in enumerate(grid)]


def find_start_node(grid: Grid[PipeNode]) -> tuple[int, int]:
    """Return the coordinates of the start position"""
    for (i, j), e in enumerate_grid(grid):
        if e.tile.start:
            return (i, j)
    raise ValueError("There is no starting point in the grid")


def BFS(start_node, grid: Grid[PipeNode]) -> None:
    """BFS to find the node with the greatest depth"""
    start_node.depth = 0
    fringe: Queue[PipeNode] = Queue()
    fringe.put(start_node)
    while not fringe.empty():
        s = fringe.get()
        for i, j in s.connected_pipes:
            if i == s.pos[0] and j == s.pos[1]:
                continue
            n = grid[i][j]
            if s.depth is None:
                raise ValueError("Depth of a previously seen node is None")
            if n.depth is None:
                n.depth = s.depth + 1
                fringe.put(n)


def paint_BFS(grid: Grid[PipeNode]) -> Grid[str]:
    """BFS to find the node with the greatest depth"""
    n, m = len(grid), len(grid[0])
    edge_grid = [['.'] * (m + 1) for _ in range(n + 1)]
    edge_grid[0][0] = "0"
    fringe: Queue[tuple[int, int]] = Queue()
    fringe.put((0, 0))
    seen = set()
    while not fringe.empty():
        i, j = fringe.get()
        if (i, j) in seen:
            raise ValueError("Already seen", (i, j))
        if edge_grid[i][j] != "0":
            raise ValueError("weird point in frindge", (i, j))
        seen.add((i, j))
        for ni, nj in neighborhood((i, j), (n + 1, m + 1), connectivity=4):
            if edge_grid[ni][nj] == '0':
                continue
            if ni in (0, n) or nj in (0, m):  # on the edge of the grid
                edge_grid[ni][nj] = "0"
                fringe.put((ni, nj))
                continue
            # check if there is no pipe to cross
            if i - ni == 1:   # top
                pipeW, pipeE = grid[i - 1][j - 1], grid[i - 1][j]
                pipeW = pipeW.depth is not None and pipeW.tile.E
                pipeE = pipeE.depth is not None and pipeE.tile.W
                if pipeE and pipeW:  # there is a pipe
                    continue
            if ni - i == 1:   # bottom
                pipeW, pipeE = grid[i][j - 1], grid[i][j]
                pipeW = pipeW.depth is not None and pipeW.tile.E
                pipeE = pipeE.depth is not None and pipeE.tile.W
                if pipeE and pipeW:  # there is a pipe
                    continue
            if j - nj == 1:   # left
                pipeN, pipeS = grid[i - 1][j - 1], grid[i][j - 1]
                pipeS = pipeS.depth is not None and pipeS.tile.N
                pipeN = pipeN.depth is not None and pipeN.tile.S
                if pipeS and pipeN:  # there is a pipe
                    continue
            if nj - j == 1:   # right
                pipeN, pipeS = grid[i - 1][j], grid[i][j]
                pipeS = pipeS.depth is not None and pipeS.tile.N
                pipeN = pipeN.depth is not None and pipeN.tile.S
                if pipeS and pipeN:  # there is a pipe
                    continue
            edge_grid[ni][nj] = "0"
            fringe.put((ni, nj))
    return edge_grid


def get_data() -> list[list[Tile]]:
    """Retrieve all the data to begin with."""
    l = lines_of_file(f"{DATA_PATH}{DAY}.txt")
    return lmap(lambda row: lmap(Tile.from_char, row), l)


def part_1() -> None:
    """Code for section 1"""
    grid = grid_map(PipeNode, get_data())
    grid_map(lambda pos, e: e.connect(grid), grid)
    si, sj = find_start_node(grid)
    BFS(grid[si][sj], grid)

    max_depth = max(flatten(grid), key=lambda x: -1 if x.depth is None else x.depth).depth

    print_answer(max_depth, part=1)


def part_2() -> None:
    """Code for section 2"""
    grid = grid_map(PipeNode, get_data())
    grid_map(lambda pos, e: e.connect(grid), grid)
    si, sj = find_start_node(grid)
    BFS(grid[si][sj], grid)  # mark depth
    painted_grid = paint_BFS(grid)
    path_grid = grid_map(lambda pos, e: '.' if e.depth is None else "*", grid)

    for (i, j), e in enumerate_grid(path_grid):
        if e == "*":
            continue
        if all(painted_grid[i + ni][j + nj] == "." for ni, nj in ((0, 0), (0, 1), (1, 0), (1, 1))):
            path_grid[i][j] = 'I'
        if all(painted_grid[i + ni][j + nj] == "0" for ni, nj in ((0, 0), (0, 1), (1, 0), (1, 1))):
            path_grid[i][j] = '0'

    if VERBOSE:
        with open(f"{DATA_PATH}{DAY}.plot.txt", 'w', encoding="utf-8") as f:
            f.write('\n')
            # print painted graph
            for row in painted_grid:
                f.write("".join(row) + "\n")
            f.write('\n')
            # print painted graph
            for row in path_grid:
                f.write("".join(row) + "\n")

    interior_points = sum(e == 'I' for e in flatten(path_grid))
    print_answer(interior_points, part=2)


def print_answer(answer: Any, part, print_fn=print) -> None:
    """Shorthand to print answer."""
    print("=" * 50)
    print(f"[DAY {DAY}] Answer to part {part} is:\n\n\t")
    print_fn(answer)
    print("\n", "=" * 50, sep="")


if __name__ == "__main__":
    part_1()  # P1: 6757
    part_2()  # P2: 523
