"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Iterator, Iterable
import math
from itertools import cycle
from dataclasses import dataclass
from functools import partial

from utils import section


@dataclass(frozen=True, slots=True)
class Node:
    """Contains a node of the map."""
    L: str
    R: str


class Tree:
    """Represents the binary Tree"""

    def __init__(self, nodes_repr: Iterable[str]) -> None:
        self.nodes = dict[str, Node]()
        for node in nodes_repr:
            name, childs = node.split(' = ')
            L, R = childs[1:-1].split(', ')
            self.nodes[name] = Node(L, R)

    def rollout(self, seq: str, start: str, part=1) -> int:
        """Return the number of steps to reach an end"""
        node_name = start
        for steps, d in enumerate(cycle(seq)):
            if part == 1 and node_name == "ZZZ" or part == 2 and node_name[-1] == 'Z':
                return steps
            node_name: str = getattr(self.nodes[node_name], d)
        return -1


@section(year=2023, day=8, part=1, sol=13019)
def part_1(data: Iterator[str]) -> int:
    """Code for section 1"""
    sequence = next(data)
    next(data)  # empty line
    return Tree(data).rollout(seq=sequence, start="AAA")


@section(year=2023, day=8, part=2, sol=13524038372771)
def part_2(data: Iterator[str]) -> int:
    """Code for section 2"""
    sequence = next(data)
    next(data)  # empty line

    tree = Tree(data)
    start_nodes = filter(lambda x: x[-1] == 'A', tree.nodes.keys())
    count_steps = partial(tree.rollout, sequence, part=2)

    return math.lcm(*map(count_steps, start_nodes))


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    part_1()
    part_2()
