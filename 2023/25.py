"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Iterator, Iterable
from dataclasses import dataclass
import random

from utils import section


@dataclass(frozen=True, slots=True)
class Graph:
    """Represents a graph with a list of edges"""
    vertices: list[str]
    edges: list[tuple[str, str]]

    @classmethod
    def from_text(cls, text: Iterable[str]) -> Graph:
        """Create graph from the input text."""
        verticies, edges = set[str](), []
        for r in text:
            v, es = r.split(': ')
            verticies.add(v)
            for e in es.split(' '):
                verticies.add(e)
                edges.append((v, e))
        return Graph(list(verticies), edges)


def min_cut(graph: Graph):
    """Create a minimum cut using Karger's algorithm.
    It creates a contracted graph by randomly merging vertices.

    Reference:
        - https://en.wikipedia.org/wiki/Karger%27s_algorithm"""
    edges = graph.edges.copy()
    vertices = graph.vertices.copy()
    while len(vertices) > 2:
        u, v = random.choice(edges)
        new_v = '|'.join((u, v))
        contraction = []
        for e in edges:
            if e in ((u, v), (v, u)):
                continue  # selected edges
            if e[0] in (u, v):
                contraction.append((new_v, e[1]))
            elif e[1] in (u, v):
                contraction.append((e[0], new_v))
            else:
                contraction.append(e)
        vertices.remove(u)
        vertices.remove(v)
        vertices.append(new_v)
        edges = contraction
    return edges, vertices


@section(year=2023, day=25, part=1, sol=596376)
def part_1(data: Iterator[str]) -> int:
    """Code for section 1"""
    graph = Graph.from_text(data)
    edges, v1, v2 = [], '', ''
    random.seed(16)   # set a seed because the algorithm is random, allow reproducibility
    while len(edges) != 3:
        # We want to have only 3 edges between the 2 components
        edges, (v1, v2) = min_cut(graph)
    return len(v1.split('|')) * len(v2.split('|'))


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    part_1()
