"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Iterable, Callable, Optional, Any, Protocol
# pylint: disable-next=unused-import
from dataclasses import dataclass, field
import os
import __main__
# import numpy as np
from utils import lines_of_file, lmap
from itertools import starmap
from collections import Counter
from enum import Enum

DATA_PATH = "inputs/"
DAY = os.path.basename(__file__).split(".")[0]
PART = 2
TEST = False


class Rule(Protocol):
    cards_order: list[str]
    cards_to_strength: dict[str, int]

    @staticmethod
    def hand_type(h: Hand) -> HandType:
        ...

    @staticmethod
    def islower(h1: Hand, h2: Hand) -> bool:
        ...


class Rule1:
    cards_order = lmap(str, range(2, 10)) + ["T", "J", "Q", "K", "A"]
    cards_to_strength = {k: i for i, k in enumerate(cards_order)}

    @staticmethod
    def hand_type(h: Hand) -> HandType:
        """Generate hand type"""
        n, values = len(h.counter), h.counter.values()
        if n == 5:
            return HandType.HightCard
        if n == 4:
            return HandType.OnePair
        if n == 3:
            if 3 in values and 1 in values:
                return HandType.ThreeOfKind
            if 2 in values and 1 in values:
                return HandType.TwoPair
            raise ValueError("Unknown Hand Type with 3 cards", h)
        if n == 2:
            if 3 in values and 2 in values:
                return HandType.FullHouse
            if 4 in values and 1 in values:
                return HandType.FourOfKind
            raise ValueError("Unknown Hand Type with 2 cards", h)
        if n == 1:
            return HandType.FiveOfKind
        raise ValueError("Unknown Hand Type")

    @staticmethod
    def islower(h1: Hand, h2: Hand) -> bool:
        if h1.hand_type == h2.hand_type:
            for h1_card, h2_card in zip(h1.cards, h2.cards):
                if h1_card == h2_card:
                    continue
                return h1_card < h2_card
            assert ValueError("Hand Equality")
        return h1.hand_type.value < h2.hand_type.value


class Rule2:
    cards_order = ["J"] + lmap(str, range(2, 10)) + ["T", "Q", "K", "A"]
    cards_to_strength = {k: i for i, k in enumerate(cards_order)}

    @staticmethod
    def islower(h1: Hand, h2: Hand) -> bool:
        return Rule1.islower(h1, h2)

    @staticmethod
    def hand_type(h: Hand) -> HandType:
        if 0 in h.counter.keys() and len(h.counter) > 1:
            joker_values = h.counter.pop(0)
            k, _ = h.counter.most_common(1)[0]
            # add Joker to the most common to create the best cards
            h.counter.update({k: joker_values})
        return Rule1.hand_type(h)


class HandType(Enum):
    HightCard = 0
    OnePair = 1
    TwoPair = 2
    ThreeOfKind = 3
    FullHouse = 4
    FourOfKind = 5
    FiveOfKind = 6


@dataclass(slots=False)
class Hand:
    """A class representing a Hand"""
    desc: str  # string representation
    bid: int
    rule: Rule = field(repr=False)
    cards: list[int] = field(init=False)
    counter: Counter[int] = field(init=False)

    def __post_init__(self) -> None:
        self.cards = lmap(lambda c: self.rule.cards_to_strength[c], self.desc)
        self.counter = Counter(self.cards)

    @property
    def hand_type(self) -> HandType:
        return self.rule.hand_type(self)

    def __lt__(self, other: Hand) -> bool:
        return self.rule.islower(h1=self, h2=other)

    @staticmethod
    def from_str(cards: str, bid: str, rule: Rule = Rule1) -> Hand:
        """Create a Hand given its card string"""
        return Hand(desc=cards, bid=int(bid), rule=rule)


def get_data() -> Iterable[list[str]]:
    """Retrieve all the data to begin with."""
    l = lines_of_file(f"{DATA_PATH}{DAY if not TEST else 'test'}.txt")
    l = map(lambda r: r.split(" "), l)
    return l


def part_1() -> None:
    """Code for section 1"""
    l = starmap(Hand.from_str, get_data())
    l = sorted(l)
    total_winings = sum((i + 1) * hand.bid for i, hand in enumerate(l))
    print_answer(total_winings)


def part_2() -> None:
    """Code for section 2"""
    l = get_data()
    l = starmap(lambda cards, bid: Hand.from_str(cards, bid, Rule2), l)
    l = sorted(l)
    total_winings = sum((i + 1) * hand.bid for i, hand in enumerate(l))
    print_answer(total_winings)


def main(fn: Optional[Callable[[], None]] = None) -> None:
    """Main process"""
    if fn is not None:
        return fn()
    ex = vars(__main__)[f"part_{PART}"]
    return ex()


def print_answer(answer: Any, part=PART, print_fn=print) -> None:
    """Shorthand to print answer."""
    print("=" * 50)
    print(f"[DAY {DAY}] Answer to part {part} is:\n\n\t")
    print_fn(answer)
    print("\n", "=" * 50, sep="")


if __name__ == "__main__":
    main()  # 251121738
    # 251421071
