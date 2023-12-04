"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Iterable, Any
from dataclasses import dataclass, field
import os
from utils import lines_of_file, lmap

DATA_PATH = "inputs/"
DAY = os.path.basename(__file__).split(".")[0]


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

    @staticmethod
    def from_input(line: str) -> Card:
        """Create a card from the input string represented as follow:
        `Card [id]: [winning_numbers...] | [numbers...]`
        """
        _, line = line.split(":")                  # remove unused text
        win_numbers, numbers = lmap(
            lambda x: filter(None, x.split(" ")),  # remove white spaces and separate numbers
            line.split("|")                        # split winning numbers and numbers
        )
        # convert numbers to int
        win_numbers, numbers = map(int, win_numbers), map(int, numbers)
        return Card(set(win_numbers), set(numbers))


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


def get_data() -> Iterable[Card]:
    """Retrieve all the data to begin with."""
    l = lines_of_file(f"{DATA_PATH}{DAY}.txt")
    return map(Card.from_input, l)


def part_1() -> None:
    """Code for section 1"""
    l = map(lambda x: x.points, get_data())

    print_answer(sum(l), part=1)


def part_2() -> None:
    """Code for section 2"""
    deck = Deck(cards=list(get_data()))

    print_answer(sum(deck.numbers), part=2)


def print_answer(answer: Any, part, print_fn=print) -> None:
    """Shorthand to print answer."""
    print("=" * 50)
    print(f"[DAY {DAY}] Answer to part {part} is:\n\n\t")
    print_fn(answer)
    print("\n", "=" * 50, sep="")


if __name__ == "__main__":
    part_1()  # P1: 20829
    part_2()  # P2: 12648035
