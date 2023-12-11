"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Iterable
from queue import Queue
from enum import Enum
import sys
from more_itertools import flatten
from utils import lines_of_file, print_answer
from utils import grid_map, enumerate_grid, lmap
from utils_types import Grid, Coordinate

VERBOSE = True
sys.setrecursionlimit(100_000)


class Direction(Enum):
    """A cardinal direction"""
    N = (-1, 0)
    S = (1, 0)
    E = (0, 1)
    W = (0, -1)


class Tile:
    """Represents the sides of the pipe in a Tile"""
    convertion_table = {
        '|': {'char': '║', 'dirs': (Direction.N, Direction.S)},
        '-': {'char': '═', 'dirs': (Direction.E, Direction.W)},
        'L': {'char': '╚', 'dirs': (Direction.N, Direction.E)},
        'J': {'char': '╝', 'dirs': (Direction.N, Direction.W)},
        '7': {'char': '╗', 'dirs': (Direction.W, Direction.S)},
        'F': {'char': '╔', 'dirs': (Direction.E, Direction.S)},
        "S": {'char': '¤', 'dirs': Direction},
        ".": {'char': '.', 'dirs': ()},
    }

    def __init__(self, dirs: Iterable[Direction], char='.') -> None:
        self.N, self.S, self.E, self.W = False, False, False, False
        for d in dirs:
            setattr(self, d.name, True)
        self.char = char

    def is_connected_to(self, tile: Tile, d: Direction) -> bool:
        """Return True if the tile is connected to the other tile in a given direction."""
        di, dj = d.value
        return getattr(self, d.name) and getattr(tile, Direction((-di, -dj)).name)

    @staticmethod
    def from_char(char: str) -> Tile:
        """Create a Tile from its char representation"""
        return Tile(**Tile.convertion_table[char])


class PipeNode:
    """Represents a Pipe on the grid.
    It knows its neighbors after the `connect` function is called."""

    def __init__(self, pos: Coordinate, tile: Tile) -> None:
        self.pos, self.tile = pos, tile
        self.connected_pipes: list[Coordinate] = []
        self.depth = -1

    def connect(self, grid: Grid[PipeNode]) -> None:
        """Connect the pipe node to its neighbors"""
        n, m = len(grid), len(grid[0])
        for d in Direction:
            (i, j), (di, dj) = self.pos, d.value
            if not 0 <= i + di < n or not 0 <= j + dj < m:
                continue
            next_tile = grid[i + di][j + dj].tile
            if self.tile.is_connected_to(next_tile, d):
                # add to neigbors only if they are connected
                self.connected_pipes.append((i + di, j + dj))

    def __lt__(self, pipe: PipeNode) -> bool:
        return self.depth < pipe.depth


class PipeMaze:
    """Represents the grid of pipes"""

    def __init__(self, tiles: Grid[Tile]) -> None:
        self.grid = grid_map(PipeNode, tiles, pos=True)
        grid_map(lambda e: e.connect(self.grid), self.grid)

    @property
    def start(self) -> PipeNode:
        """Return the coordinates of the start position"""
        for _, e in enumerate_grid(self.grid):
            if e.tile.char == '¤':
                return e
        raise ValueError("There is no starting point in the grid")

    def find_path(self) -> None:
        """Create a path using BFS.
        It registers the depth of a pipe from the starting point."""
        self.start.depth = 0
        fringe: Queue[PipeNode] = Queue()
        fringe.put(self.start)
        while not fringe.empty():
            s = fringe.get()
            for i, j in s.connected_pipes:
                n = self.grid[i][j]
                if s.depth < 0:
                    raise ValueError("Depth of a previously seen node is None")
                if n.depth < 0:
                    n.depth = s.depth + 1
                    fringe.put(n)


class EdgeGraph:
    """Represents the edges of the maze where every pipe is inside a box."""

    def __init__(self, maze: PipeMaze) -> None:
        n, m = len(maze.grid), len(maze.grid[0])
        self.grid = [['.'] * (m + 1) for _ in range(n + 1)]
        self.maze = maze

    def cross_pipe(self, pos: Coordinate, d: Direction) -> bool:
        """Returns True if the coordinate obtained with a given direction
        cross a pipe from the maze."""
        (i, j) = pos
        lookup: dict[str, tuple[Coordinate, Coordinate, Direction]] = {
            'N': ((i - 1, j - 1), (i - 1, j), Direction.E),
            'S': ((i, j - 1), (i, j), Direction.E),
            'E': ((i - 1, j), (i, j), Direction.S),
            'W': ((i - 1, j - 1), (i, j - 1), Direction.S)
        }
        (i1, j1), (i2, j2), d = lookup[d.name]
        pipe1, pipe2 = self.maze.grid[i1][j1], self.maze.grid[i2][j2]
        are_connected = pipe1.tile.is_connected_to(pipe2.tile, d)
        on_main_path = pipe1.depth >= 0 and pipe2.depth >= 0
        return on_main_path and are_connected

    def flood_fill(self, x: Coordinate, color: str) -> None:
        """Fill a grid from a starting position using `flood_fill` algorithm."""
        (i, j), n, m = x, len(self.grid), len(self.grid[0])
        if self.grid[i][j] != '.':
            return

        self.grid[i][j] = color
        for d in Direction:
            di, dj = d.value
            ni, nj = i + di, j + dj
            if not 0 <= ni < n or not 0 <= nj < m:
                continue
            on_edge = ni in (0, n - 1) or nj in (0, m - 1)
            if on_edge or not self.cross_pipe((i, j), d):
                self.flood_fill((ni, nj), color=color)


def get_data() -> Grid[Tile]:
    """Retrieve all the data to begin with."""
    l = lines_of_file("inputs/10.txt")
    l = lmap(list, l)                   # convert to grid
    return grid_map(Tile.from_char, l)  # convert to Tiles


def part_1() -> None:
    """Code for section 1"""
    maze = PipeMaze(get_data())
    maze.find_path()
    max_depth = max(flatten(maze.grid)).depth

    print_answer(max_depth, day=10, part=1)


def part_2() -> None:
    """Code for section 2"""
    maze = PipeMaze(get_data())
    maze.find_path()
    edges = EdgeGraph(maze)
    edges.flood_fill((0, 0), color="0")

    path_grid = grid_map(lambda e: e.tile.char if e.depth >= 0 else ".", maze.grid)
    for (i, j), e in enumerate_grid(path_grid):
        if e != '.':
            continue
        # we are not on the path, we can color the current point
        # A point can be colored if the four points on the corners (edge grid) are the same color
        corners = ((0, 0), (0, 1), (1, 0), (1, 1))
        if all(edges.grid[i + ni][j + nj] == "." for ni, nj in corners):
            path_grid[i][j] = '~'    # we are inside the loop
        if all(edges.grid[i + ni][j + nj] == "0" for ni, nj in corners):
            path_grid[i][j] = ' '    # we are outside the loop

    if VERBOSE:
        with open("visualisations/10.txt", 'w', encoding="utf-8") as f:
            f.write('\n')  # print painted graph
            for row in path_grid:
                f.write("".join(row) + "\n")

    interior_points = sum(e == '~' for e in flatten(path_grid))
    print_answer(interior_points, day=10, part=2)


if __name__ == "__main__":
    part_1()  # P1: 6757
    part_2()  # P2: 523
