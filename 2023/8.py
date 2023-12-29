"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
import math
from typing import Iterator
from itertools import cycle
from utils import section, lmap


class Node:
    """Contains a node of the map."""

    def __init__(self, row: str) -> None:
        self.name, raw_LR = row.split(" = ")
        self.L, self.R = raw_LR[1:-1].split(', ')

    def build_path(self, dictionnary: dict[str, int], nodes: list[Node]) -> None:
        """Construct the relation between nodes"""
        if isinstance(self.R, str):
            self.R = nodes[dictionnary[self.R]]
        if isinstance(self.L, str):
            self.L = nodes[dictionnary[self.L]]


def rollout(seq: str, node: Node, part=1) -> int:
    """Return the number of steps to reach an end"""
    for steps, d in enumerate(cycle(seq)):
        if part == 1 and node.name == "ZZZ" or part == 2 and node.name[-1] == 'Z':
            return steps
        node = getattr(node, d)
    return -1


@section(year=2023, day=8, part=1, sol=13019)
def part_1(data: Iterator[str]) -> int:
    """Code for section 1"""
    sequence = next(data)
    next(data)  # empty line
    nodes = lmap(Node, data)

    name_to_id = {node.name: i for i, node in enumerate(nodes)}
    for node in nodes:
        node.build_path(name_to_id, nodes)

    return rollout(seq=sequence, node=nodes[0])


@section(year=2023, day=8, part=2, sol=13524038372771)
def part_2(data: Iterator[str]) -> int:
    """Code for section 2"""
    sequence = next(data)
    next(data)  # empty line
    nodes = lmap(Node, data)

    name_to_id = {node.name: i for i, node in enumerate(nodes)}
    for node in nodes:
        node.build_path(name_to_id, nodes)

    start_nodes = set(filter(lambda x: x.name[-1] == 'A', nodes))
    steps = map(lambda n: rollout(seq=sequence, node=n, part=2), start_nodes)

    return math.lcm(*steps)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    part_1()
    part_2()
