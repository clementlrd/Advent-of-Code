"""A module including useful types."""
from typing import TypeVar

T = TypeVar('T')
S = TypeVar('S')
Grid = list[list[T]]
Coordinate = tuple[int, int]
