"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Iterator
from dataclasses import dataclass, field
from utils import section, lmap


@dataclass(frozen=True, slots=True)
class Card:
    """A class to represents a scratchcard."""
    winning_numbers: set[int]  # the wining numbers of the scratchcard.
    numbers: set[int]          # the numbers of the scratchcard.

    @property
    def valid_numbers(self) -> set[int]:
        """the numbers that are winning."""
        return self.numbers & self.winning_numbers  # set intersection

    @property
    def points(self) -> int:
        """the number of points made by the card."""
        n = len(self.valid_numbers)
        return 2 ** (n - 1) if n else 0

    @classmethod
    def from_repr(cls, _repr: str) -> Card:
        """Create a card from the input string represented as follow:
        `Card [id]: [winning_numbers...] | [numbers...]`
        """
        def format_(n: str) -> set[int]:
            numbers = filter(None, n.split(" "))  # remove white spaces and separate numbers
            return set(map(int, numbers))         # convert numbers to int in a set

        _, win_numbers, numbers = _repr.replace(':', ' |').split('|')
        return cls(format_(win_numbers), format_(numbers))


@dataclass(slots=True)
class Deck:
    """A deck of scratchcard. Compute the final number of cards in the deck."""
    cards: list[Card]                         # scratchcards
    numbers: list[int] = field(init=False)    # final number of each scratchcards

    def __post_init__(self) -> None:
        self.numbers = [1 for _ in self.cards]
        self._compute_deck()

    def _compute_deck(self) -> None:
        """Compute how many scratchcards there is in the final deck
        according to the the valid numbers of each card."""
        for pos, card in enumerate(self.cards):
            for i in range(len(card.valid_numbers)):
                # create a copy of the next n cards
                self.numbers[pos + i + 1] += self.numbers[pos]


@section(year=2023, day=4, part=1, sol=20829)
def part_1(data: Iterator[str]) -> int:
    """Code for section 1"""
    return sum(Card.from_repr(r).points for r in data)


@section(year=2023, day=4, part=2, sol=12648035)
def part_2(data: Iterator[str]) -> int:
    """Code for section 2"""
    return sum(Deck(cards=lmap(Card.from_repr, data)).numbers)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    part_1()
    part_2()
