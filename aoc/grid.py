from __future__ import annotations
from collections.abc import Iterator
from typing import Callable
from dataclasses import dataclass, field

from .itertools import crange

Coordinate = tuple[int, int]

@dataclass
class Grid[S]:
    _data: list[list[S]] = field(repr=False)

    def __post_init__(self) -> None:
        assert all(len(self._data[i]) == len(self._data[0]) for i in range(self.shape[0]))

    def __getitem__(self, idx: Coordinate) -> S:
        return self._data[idx[0]][idx[1]]

    def __iter__(self) -> Iterator[S]:
        return (e for row in self._data for e in row)

    def __len__(self) -> int:
        return len(self._data[0])

    @property
    def shape(self) -> tuple[int, int]:
        return len(self._data), len(self._data[0])

    @property
    def T(self) -> Grid[S]:
        return self.transpose()

    @property
    def rows(self) -> Iterator[list[S]]:
        return iter(self._data)

    @property
    def cols(self) -> Iterator[list[S]]:
        n, m = self.shape
        return ([self[i,j] for i in range(n)] for j in range(m))
    
    def enumerate(self) -> Iterator[tuple[Coordinate, S]]:
        return ( (ij, self[ij]) for ij in crange(self.shape))

    def map(self, fn: Callable[[S], S]) -> Grid[S]:
        return Grid([[ fn(e) for e in row] for row in self._data])

    def map_pos(self, fn: Callable[[Coordinate], S]) -> Grid[S]:
        n, m = self.shape
        return Grid([[ fn((i,j)) for j in range(m)] for i in range(n)])

    def subgrid(self, start: Coordinate, end: Coordinate) -> Grid[S]:
        """Create a subgrid of a grid.
        Works as range objects, but in two dimensions and end is taken in the subgrid."""
        (si, sj), (ei, ej) = start, end
        return Grid([row[sj:ej] for row in self._data[si:ei]])

    def transpose(self) -> Grid[S]:
        """Transpose a grid as it was a matrix."""
        n, m = self.shape
        return Grid([[self[i,j] for i in range(n)] for j in range(m)])

    def flip(self, axis: int=1) -> Grid[S]:
        """Mirror the grid along a given axis."""
        match axis:
            case 0: return Grid(self._data[::-1])
            case 1: return Grid([row[::-1] for row in self._data])
            case _: raise ValueError(f"axis {axis} is not valid. Please enter 0 or 1.")

    def rotate90(self, clockwize=True) -> Grid[S]:
        """Rotates a grid clockwise or not. Defaults: Clockwize."""
        return self.T.flip(axis=int(clockwize))

    def is_valid(self, ij: Coordinate) -> bool:
        (n, m), (i, j) = self.shape, ij
        return 0 <= i < n and 0 <= j < m

    def __repr__(self) -> str:
        return "\n".join(" ".join(map(str, row)) for row in self._data)