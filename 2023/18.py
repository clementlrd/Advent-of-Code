"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Iterator
import matplotlib.pyplot as plt

from utils import section
from utils_types import Coordinate

VERBOSE = True
directions: dict[str, Coordinate] = {'R': (1, 0), 'L': (-1, 0), 'U': (0, 1), 'D': (0, -1)}


def total_points(area: int, border_points: int) -> int:
    """Compute the number of total points according to picks formula.

    Référence:
        - https://en.wikipedia.org/wiki/Pick%27s_theorem
    """
    return area + 1 + border_points // 2


@section(year=2023, day=18, part=1, sol=42317)
def part_1(data: Iterator[str]) -> float:
    """Code for section 1"""
    x1, y1, area, border_points = 0, 0, 0, 0
    for raw_edges in data:
        d, step, _ = raw_edges.split(" ")
        step, dx, dy = int(step), *directions[d]

        border_points += step  # compute the number of points on the border
        x2, y2 = x1 + step * dx, y1 + step * dy        # compute next point
        # compute area according to Shoelace triangle formula
        # Référence: https://en.wikipedia.org/wiki/Shoelace_formula
        area += (x1 * y2 - x2 * y1) / 2
        x1, y1 = x2, y2
    return total_points(int(abs(area)), border_points)


@section(year=2023, day=18, part=2, sol=83605563360288)
def part_2(data: Iterator[str]) -> float:
    """Code for section 2"""
    dir_code = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}
    x1, y1, area, border_points = 0, 0, 0, 0
    for raw_edges in data:
        _, _, color = raw_edges.split(" ")
        dx, dy = directions[dir_code[color[-2]]]
        step = int(f'0x{color[2:-2]}', base=16)

        border_points += step  # compute the number of points on the border
        x2, y2 = x1 + step * dx, y1 + step * dy        # compute next point
        # compute area according to Shoelace triangle formula
        # Référence: https://en.wikipedia.org/wiki/Shoelace_formula
        area += (x1 * y2 - x2 * y1) / 2
        x1, y1 = x2, y2
    return total_points(int(abs(area)), border_points)


@section(year=2023, day=18)
def visualize(data: Iterator[str]) -> None:
    """Create a plot of the areas."""
    fig, (ax1, ax2) = plt.subplots(1, 2)

    dir_code = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}
    x1, y1, x2, y2 = 0, 0, 0, 0
    for raw_edges in data:
        d, step, color = raw_edges.split(" ")

        # part1
        step, dx, dy = int(step), *directions[d]
        ax1.plot([x1, x1 + dx * step], [y1, y1 + dy * step])
        x1, y1 = x1 + dx * step, y1 + dy * step

        # part2
        dx, dy = directions[dir_code[color[-2]]]
        step = int(f'0x{color[2:-2]}', base=16)
        ax2.plot([x2, x2 + dx * step], [y2, y2 + dy * step])
        x2, y2 = x2 + dx * step, y2 + dy * step

    fig.savefig('visualizations/18.png')


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    part_1()
    part_2()
    if VERBOSE:
        visualize()
