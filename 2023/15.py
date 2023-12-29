"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Iterator
from dataclasses import dataclass, field
from functools import reduce
from utils import section, find_element, compose


@dataclass
class Lens:
    """Represents a lens. It has a label and a focal length."""
    label: str
    focal_length: int


@dataclass
class Box:
    """Represents a box as available slots."""
    slots: list[Lens] = field(init=False, default_factory=list)

    def add_lens(self, lens: Lens) -> None:
        """Add a lens to the box on top of the other slots.
        If a lens with the same label already exists, it is replaced."""
        i, e = find_element(self.slots, lambda s: s.label == lens.label)
        if e is None:
            self.slots.append(lens)
        else:
            self.slots[i] = lens

    def remove_lens(self, label: str) -> Lens | None:
        """Remove a lens from the box.
        When a lens is retrieved, slots are updated to fill in the gaps.
        """
        i, e = find_element(self.slots, lambda s: s.label == label)
        # if the element is not inside the box, return None
        return e if e is None else self.slots.pop(i)


def hash_str(string: str) -> int:
    """hash a string using HASH procedure."""
    return reduce(lambda acc, c: (acc + ord(c)) * 17 % 256, string, 0)


def execute_procedure(procedures: list[str]) -> list[Box]:
    """Execute a serie of commands according to HASHMAP procedure."""
    boxes = [Box() for _ in range(256)]
    for cmd in procedures:
        if '-' in cmd:
            # retrieve a Lens with a given label from its box
            label = cmd[:-1]
            boxes[hash_str(label)].remove_lens(label)
        elif "=" in cmd:
            # add a lens to a special box
            label, value = cmd.split("=")
            boxes[hash_str(label)].add_lens(Lens(label, focal_length=int(value)))
        else:
            raise ValueError(f"Unknown command {cmd}")
    return boxes


def focusing_power(boxes: list[Box]) -> int:
    """Compute focusing power metric."""
    # TODO: move inside box
    def box_power(box: Box) -> int:
        return sum((slot + 1) * l.focal_length for slot, l in enumerate(box.slots))

    return sum((i + 1) * box_power(box) for i, box in enumerate(boxes))


@section(year=2023, day=15, part=1, sol=509784)
def part_1(data: Iterator[str]) -> int:
    """Code for section 1"""
    operations = next(data).split(',')
    return sum(map(hash_str, operations))


@section(year=2023, day=15, part=2, sol=230197)
def part_2(data: Iterator[str]) -> int:
    """Code for section 2"""
    operations = next(data).split(',')
    return compose(focusing_power, execute_procedure)(operations)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    part_1()
    part_2()
