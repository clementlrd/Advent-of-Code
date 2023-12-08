"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
import math
from typing import Any
from itertools import cycle
import os
from utils import lines_of_file, lmap

DATA_PATH = "inputs/"
DAY = os.path.basename(__file__).split(".")[0]


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


def get_data() -> tuple[str, list[Node]]:
    """Retrieve all the data to begin with."""
    l = lines_of_file(f"{DATA_PATH}{DAY}.txt")
    sequence = next(l)
    next(l)
    return sequence, lmap(Node, l)


def rollout(seq: str, node: Node, part=1) -> int:
    """Return the number of steps to reach an end"""
    for steps, d in enumerate(cycle(seq)):
        if part == 1 and node.name == "ZZZ" or part == 2 and node.name[-1] == 'Z':
            return steps
        node = getattr(node, d)
    return -1


def part_1() -> None:
    """Code for section 1"""
    sequence, l = get_data()
    name_to_id = {node.name: i for i, node in enumerate(l)}
    for node in l:
        node.build_path(name_to_id, l)

    print_answer(rollout(seq=sequence, node=l[0]), part=1)


def part_2() -> None:
    """Code for section 2"""
    sequence, l = get_data()
    name_to_id = {node.name: i for i, node in enumerate(l)}
    for node in l:
        node.build_path(name_to_id, l)

    start_nodes = set(filter(lambda x: x.name[-1] == 'A', l))
    steps = map(lambda n: rollout(seq=sequence, node=n, part=2), start_nodes)

    print_answer(math.lcm(*steps), part=2)


def print_answer(answer: Any, part, print_fn=print) -> None:
    """Shorthand to print answer."""
    print("=" * 50)
    print(f"[DAY {DAY}] Answer to part {part} is:\n\n\t")
    print_fn(answer)
    print("\n", "=" * 50, sep="")


if __name__ == "__main__":
    part_1()  # P1: 13019
    part_2()  # P2: 13524038372771
