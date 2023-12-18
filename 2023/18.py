"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Iterator
from utils import lines_of_file, section
from utils_types import Coordinate


InputData = Iterator[str]
directions: dict[str, Coordinate] = {'R': (1, 0), 'L': (-1, 0), 'U': (0, 1), 'D': (0, -1)}


def get_data() -> InputData:
    """Retrieve all the data to begin with."""
    return lines_of_file("inputs/18.txt")


def total_points(area: int, border_points: int) -> int:
    """Compute the number of total points according to picks formula.

    Référence:
        - https://en.wikipedia.org/wiki/Pick%27s_theorem
    """
    return area + 1 + border_points // 2


@section(day=18, part=1)
def part_1(data: InputData) -> float:
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


@section(day=18, part=2)
def part_2(data: InputData) -> float:
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


if __name__ == "__main__":
    # TODO: visualization with matplotlib
    part_1(get_data())  # P1: 42317
    part_2(get_data())  # P2: 83605563360288
