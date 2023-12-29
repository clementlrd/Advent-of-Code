"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Iterable, Iterator, Protocol, Self
from collections import Counter
from enum import Enum
from dataclasses import dataclass, field
from utils import section, lmap


class Rule(Protocol):
    """A rule is applied to an Hand"""
    cards_order: list[str]
    cards_to_strength: dict[str, int]

    @staticmethod
    def format_with_rule(h: Hand) -> None:
        """Format an hand according to the rules"""


class Rule1:
    """The rule for the first part"""
    cards_order = lmap(str, range(2, 10)) + ["T", "J", "Q", "K", "A"]
    cards_to_strength = {k: i for i, k in enumerate(cards_order)}

    @staticmethod
    def format_with_rule(h: Hand) -> None:
        """Create `cards_strength` and `counter` according to card order"""
        h.card_strengths = lmap(lambda c: Rule1.cards_to_strength[c], h.desc)
        h.counter = Counter(h.desc)


class Rule2:
    """The rule for the second part"""
    cards_order = ["J"] + lmap(str, range(2, 10)) + ["T", "Q", "K", "A"]
    cards_to_strength = {k: i for i, k in enumerate(cards_order)}

    @staticmethod
    def format_with_rule(h: Hand) -> None:
        """Create `cards_strength` and `counter` according to card order
        while dealing with the Joker: it is removed from the counter and added
        to the card that make the best hand"""
        h.card_strengths = lmap(lambda c: Rule2.cards_to_strength[c], h.desc)
        h.counter = Counter(h.desc)
        if "J" in h.counter.keys() and len(h.counter) > 1:
            # count the number of joker (and remove entry)
            joker_values = h.counter.pop("J")
            k, _ = h.counter.most_common(1)[0]
            # add Joker to the most common to create the best cards
            h.counter.update({k: joker_values})


class HandType(Enum):
    """Type of a Hand"""
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
    card_strengths: list[int] = field(init=False)
    counter: Counter[str] = field(init=False)

    def set_rule(self, rule: Rule) -> Self:
        """Apply a rule to the hand"""
        rule.format_with_rule(self)
        return self

    @property
    def hand_type(self) -> HandType:
        """Return the type of the hand."""
        values = self.counter.values()
        # check the number of different cards.
        if len(values) == 5:
            return HandType.HightCard
        if len(values) == 4:
            return HandType.OnePair
        if len(values) == 3:
            if 3 in values and 1 in values:
                return HandType.ThreeOfKind
            if 2 in values and 1 in values:
                return HandType.TwoPair
            raise ValueError("Unknown Hand Type with 3 cards")
        if len(values) == 2:
            if 3 in values and 2 in values:
                return HandType.FullHouse
            if 4 in values and 1 in values:
                return HandType.FourOfKind
            raise ValueError("Unknown Hand Type with 2 cards")
        if len(values) == 1:
            return HandType.FiveOfKind
        raise ValueError("Unknown Hand Type")

    def __lt__(self, other: Hand) -> bool:
        if self.hand_type == other.hand_type:
            for self_card, other_card in zip(self.card_strengths, other.card_strengths):
                if self_card == other_card:
                    continue
                return self_card < other_card
            assert ValueError("Hand Equality")
        return self.hand_type.value < other.hand_type.value

    @classmethod
    def from_repr(cls, _repr: str) -> Hand:
        """Create a Hand given its card string"""
        cards, bid = _repr.split(' ')
        return Hand(desc=cards, bid=int(bid))


def total_winnings(hands: Iterable[Hand]) -> int:
    """Compute the total winning: the rank times the bid added for each hand"""
    return sum((i + 1) * hand.bid for i, hand in enumerate(hands))


@section(year=2023, day=7, part=1, sol=251121738)
def part_1(data: Iterator[str]) -> int:
    """Code for section 1"""
    hands = map(Hand.from_repr, data)
    hands = map(lambda h: h.set_rule(Rule1), hands)  # set rule for hands
    hands = sorted(hands)                            # sort hands

    return total_winnings(hands)


@section(year=2023, day=7, part=2, sol=251421071)
def part_2(data: Iterator[str]) -> int:
    """Code for section 2"""
    hands = map(Hand.from_repr, data)
    hands = map(lambda h: h.set_rule(Rule2), hands)  # set rule for hand
    hands = sorted(hands)                            # sort hands

    return total_winnings(hands)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    part_1()
    part_2()
