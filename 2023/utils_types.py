"""A module including useful types."""
from typing import TypeVar, TypeVarTuple, TypedDict

T = TypeVar('T')
S = TypeVar('S')

Grid = list[list[T]]
Coordinate = tuple[int, int]
Coordinate3D = tuple[int, int, int]

Args = TypeVarTuple('Args')
Kwargs = TypeVar('Kwargs', bound=TypedDict)
