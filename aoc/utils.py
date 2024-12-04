from __future__ import annotations
from typing import Literal, Self, overload, override
import math

Coordinate3D = tuple[int, int, int]

class Coordinate(tuple[int, int]):
    def __neg__(self) -> Self: return self.__class__((-self[0], -self[1]))
    def __sub__(self, b: Self) -> Self: return self.__class__((self[0] - b[0], self[1] - b[1]))
    @override
    def __add__(self, b: Self) -> Self: return self.__class__((self[0] + b[0], self[1] + b[1])) # type: ignore
    @override
    def __rmul__(self, a: int) -> Self: return self.__class__((a * self[0], a * self[1]))       # type: ignore
    def norm(self, p: int=2) -> float:
        match p:
            case 1: return abs(self[0]) + abs(self[1])
            case 2: return math.sqrt(self[0] ** 2 + self[1] ** 2)
            case _: raise NotImplementedError()

class Direction(Coordinate): ...

class Directions:
    N = Direction((-1,0)); S = -N
    E = Direction((0,1)); W = -E
    NE = N + E; NW = N + W
    SE = S + E; SW = S + W

class Neighborhood:
    @overload
    def __new__(cls, mode: Literal['c4'] | Literal['plus'] | Literal['cross']) \
        -> tuple[Direction, Direction, Direction, Direction]: ...
    @overload
    def __new__(cls, mode: Literal['c8']="c8") \
        -> tuple[Direction, Direction, Direction, Direction, Direction, Direction, Direction, Direction]: ...
    def __new__(cls, mode: str="c8") -> tuple[Direction, ...]:
        plus = (Directions.N, Directions.S, Directions.E, Directions.W)
        cross = (Directions.NE, Directions.SE, Directions.NW, Directions.SW)
        match mode:
            case "c4" | "plus": return plus
            case "cross": return cross
            case "c8": return plus + cross
            case _: raise ValueError("neighborhood can be either 'c4', 'c8', 'plus' or 'cross'.")    
