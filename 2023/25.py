"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from dataclasses import dataclass
import random

from utils import lines_of_file, section


@dataclass
class Graph:
    """Represents a graph with a list of edges"""
    vertices: list[str]
    edges: list[tuple[str, str]]


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


InputData = Graph


def get_data() -> InputData:
    """Retrieve all the data to begin with."""
    verticies = set[str]()
    edges = []
    for r in lines_of_file("inputs/25.txt"):
        v, es = r.split(': ')
        verticies.add(v)
        for e in es.split(' '):
            verticies.add(e)
            edges.append((v, e))
    return Graph(list(verticies), edges)


@section(day=25, part=1, sol=596376)
def part_1(graph: InputData) -> int:
    """Code for section 1"""
    edges, v1, v2 = [], '', ''
    random.seed(16)
    while len(edges) != 3:
        print('iter')
        # We want to have only 3 edges between the 2 components
        edges, (v1, v2) = min_cut(graph)
    return len(v1.split('|')) * len(v2.split('|'))


if __name__ == "__main__":
    part_1(get_data())  # P1:
