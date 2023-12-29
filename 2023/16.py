"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import TypeVar, Iterator
from dataclasses import dataclass
from itertools import repeat, chain
from copy import deepcopy
from enum import Enum
from queue import LifoQueue
from utils import section, lmap, grid_map
from utils_types import Grid, Coordinate


class Direction(Enum):
    """A cardinal direction"""
    N = 1j
    S = -1j
    E = 1 + 0j
    W = -1 + 0j


@dataclass
class Tile:
    """Represents a basic Tile that can be energized upon the passage of a beam."""
    repr: str
    energized: bool = False

    @classmethod
    def from_repr(cls, c: str) -> Tile | Mirror | Splitter:
        """Create from string representation of the Tile."""
        return Mirror(c) if c in '/\\' else Splitter(c) if c in '|-' else cls(c)


class Mirror(Tile):
    """A special Tile that can reflect a ray in another direction."""
    lface_seen: bool = False
    rface_seen: bool = False

    def reflect_beam(self, direction: Direction) -> Direction:
        """Send a beam in another direction as a mirror will do."""
        d = direction.value
        if self.repr == '\\':
            self.rface_seen |= direction in (Direction.W, Direction.S)
            self.lface_seen |= direction in (Direction.E, Direction.N)
            if not d.imag:  # horizontal
                return Direction(d * 1j)  # rotate anticlockwize
            return Direction(d * -1j)     # rotate clockwize
        if self.repr == '/':
            self.rface_seen |= direction in (Direction.W, Direction.N)
            self.lface_seen |= direction in (Direction.E, Direction.S)
            if not d.real:  # vertical
                return Direction(d * 1j)  # rotate anticlockwize
            return Direction(d * -1j)     # rotate clockwize
        raise ValueError(f'{self.repr} is not a Mirror')

    def already_reflect(self, direction: Direction) -> bool:
        """Whether the mirror has already reflected a ray in these directions."""
        if self.repr == '\\':
            if direction in (Direction.W, Direction.S):
                return self.rface_seen
            if direction in (Direction.E, Direction.N):
                return self.lface_seen
        if self.repr == '/':
            if direction in (Direction.E, Direction.S):
                return self.lface_seen
            if direction in (Direction.W, Direction.N):
                return self.rface_seen
        raise ValueError(f'{self.repr} is not a Mirror')


class Splitter(Tile):
    """A special Tile that can split a ray into two other directions."""
    split: bool = False
    pass_through: bool = False

    def reflect_beam(self, direction: Direction) -> tuple[Direction, ...]:
        """Split the beam according to the splitter functionning."""
        d = direction.value
        if self.repr == "|" and not d.imag:  # horizontal
            self.split = True
            return (Direction.N, Direction.S)
        if self.repr == '-' and not d.real:  # vertical
            self.split = True
            return (Direction.E, Direction.W)
        self.pass_through = True
        return (direction, )

    def already_reflect(self, direction: Direction) -> bool:
        """Whether the splitter has already reflected a ray in these directions."""
        if self.repr == '|' and not direction.value.imag:
            return self.split
        if self.repr == '-' and not direction.value.real:
            return self.split
        return self.pass_through


T = TypeVar('T', bound=Tile)


def send_beam(grid: Grid[T], start: Coordinate = (0, 0)) -> None:
    """Send a beam throught the contraption."""
    n, m = len(grid), len(grid[0])
    beams: LifoQueue[tuple[Coordinate, Direction]] = LifoQueue()
    beams.put((start, Direction.E))
    while not beams.empty():
        (i, j), d = beams.get()
        # propagate beam
        while 0 <= i < n and 0 <= j < m:
            tile = grid[i][j]
            tile.energized = True  # set the tile as energized
            if isinstance(tile, Splitter) and tile.already_reflect(d):
                break  # don't cycle

            if isinstance(tile, Splitter):
                for new_d in tile.reflect_beam(d):
                    new_pos = complex(j, i) + new_d.value
                    new_pos = int(new_pos.imag), int(new_pos.real)
                    beams.put((new_pos, new_d))
                break

            if isinstance(tile, Mirror):
                d = tile.reflect_beam(d)

            # continue until finding a miror or and edge of the grid
            new_pos = complex(j, i) + d.value
            i, j = int(new_pos.imag), int(new_pos.real)


@section(year=2023, day=16, part=1, sol=7210)
def part_1(data: Iterator[str]) -> int:
    """Code for section 1"""
    grid = lmap(list, data)                           # convert to grid
    grid = grid_map(Tile.from_repr, grid, pos=False)  # convert to Tiles or Mirrors
    send_beam(grid)
    with open("visualisations/16.txt", 'w', encoding='utf-8') as f:
        for row in grid:
            for tile in row:
                f.write("*" if tile.energized else tile.repr)
            f.write('\n')
    return sum((t.energized for row in grid for t in row))


@section(year=2023, day=16, part=2, sol=7673)
def part_2(data: Iterator[str]) -> int:
    """Code for section 2"""
    grid = lmap(list, data)                           # convert to grid
    grid = grid_map(Tile.from_repr, grid, pos=False)  # convert to Tiles or Mirrors
    n, m = len(grid), len(grid[0])
    top_row = zip(repeat(0), range(m))
    bottom_row = zip(repeat(n), range(m))
    left_column = zip(range(n), repeat(0))
    right_column = zip(range(n), repeat(m))

    energized = 0
    for start in chain(top_row, bottom_row, left_column, right_column):
        test_grid = deepcopy(grid)
        send_beam(test_grid, start=start)
        energized = max(energized, sum((t.energized for row in test_grid for t in row)))

    return energized


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    part_1()
    part_2()
