"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Iterable, Optional
from functools import reduce
from dataclasses import dataclass, field
from operator import mul

from utils import section, lmap


@dataclass
class Set:
    """A set is a number of cube of each color retrieved from the bag once."""
    red: int = field(default=0)
    blue: int = field(default=0)
    green: int = field(default=0)

    @property
    def power(self) -> int:
        """Compute the power metric of the set."""
        return reduce(mul, self.__dict__.values())

    def is_valid(self, max_set: Set) -> bool:
        """Check whether the set is valid."""
        return all((
            getattr(self, color) <= getattr(max_set, color)
            for color in ('red', 'blue', 'green')
        ))

    @classmethod
    def from_repr(cls, _repr: str) -> Set:
        """Create Set from string representation.
        The string representation can have duplicates or no value defined."""
        s = cls()
        for cube_color in _repr.split(", "):
            nbr, color = cube_color.split(" ")
            setattr(s, color, int(nbr))
        return s

    @classmethod
    def max(cls, s1: Set, s2: Set) -> Set:
        """Create a set that corresponds to the max af each color"""
        return cls(**{
            color: max(getattr(s1, color), getattr(s2, color))
            for color in ('red', 'blue', 'green')
        })


@dataclass
class Game:
    """A game is a list of sets."""
    id: int
    sets: list[Set]

    def is_valid(self, max_set: Optional[Set] = None) -> bool:
        """Check whether the game is valid. A valid game is a game that as all its sets valid."""
        if max_set is None:
            max_set = Set(12, 13, 14)
        return all(s.is_valid(max_set) for s in self.sets)

    def reduced(self) -> Set:
        """Create a set that correspond to the set of the minimum cubes required.
        It's the maximum number of a ball color on a game."""
        return reduce(Set.max, self.sets)

    @classmethod
    def from_repr(cls, _repr: str) -> Game:
        """Create a game from its representation. The format is `Game x: [set list]`."""
        info, sets = _repr.split(": ")
        game_id = int(info.split(" ")[-1])
        sets = lmap(Set.from_repr, sets.split('; '))
        return cls(game_id, sets)


@section(year=2023, day=2, part=1, sol=2679)
def part_1(data: Iterable[str]) -> int:
    """Code for section 1"""
    games = map(Game.from_repr, data)
    valid_games = filter(Game.is_valid, games)
    return sum(g.id for g in valid_games)  # sum valid IDs


@section(year=2023, day=2, part=2, sol=77607)
def part_2(data: Iterable[str]) -> int:
    """Code for section 2"""
    games = map(Game.from_repr, data)
    sets = map(Game.reduced, games)
    return sum(s.power for s in sets)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    part_1()
    part_2()
