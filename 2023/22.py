"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Iterator
from dataclasses import dataclass, field
from itertools import chain

import matplotlib.pyplot as plt          # noqa
from mpl_toolkits.mplot3d import Axes3D  # noqa
import numpy as np
from numpy.random import sample

from utils import lines_of_file, section, lmap, lfilter
from utils_types import Coordinate3D, Coordinate
from functools import reduce

DAY = 22
TEST = False
VERBOSE = True

alpha = .9
speed = .1


@dataclass
class Brick:
    direction: int
    length: int
    pos: Coordinate3D
    color: np.ndarray = field(default_factory=lambda: sample(size=3))
    proj: set[Coordinate] = field(init=False)  # projection in (x,y) coordinates

    def __post_init__(self) -> None:
        self.proj = set(map(lambda c: c[:-1], self))

    @property
    def z(self) -> int:
        return self.pos[-1]

    @property
    def z_positions(self) -> Iterator[int]:
        if self.direction == 2:
            for l in range(self.length if self.direction == 2 else 1):
                yield self.z + l
            return
        yield self.z

    @classmethod
    def from_repr(cls, _repr: str) -> Brick:
        start, end = _repr.split('~')
        start = lmap(int, start.split(','))
        end = lmap(int, end.split(','))
        x, y, z = (min(a, b) for a, b in zip(start, end))
        if start == end:
            return cls(0, 1, (x, y, z))
        direction = next((i for i, (x1, x2) in enumerate(zip(start, end)) if x1 != x2))
        length = max(start[direction], end[direction]) \
            - min(start[direction], end[direction]) + 1
        return cls(direction, length, (x, y, z))

    def is_brick_under(self, brick: Brick):
        return len(brick.proj & self.proj) > 0 and brick < self

    def __lt__(self, brick: Brick) -> bool:
        return self.z < brick.z

    def __iter__(self) -> Iterator[Coordinate3D]:
        for l in range(self.length):
            x, y, z = (x + (l if self.direction == i else 0) for i, x in enumerate(self.pos))
            yield (x, y, z)


def make_fall(brick_layers: dict[int, list[Brick]], brick: Brick) -> None:
    for z in range(brick.z, 0, -1):
        layer = brick_layers[z]
        brick_under = next(filter(brick.is_brick_under, layer), None)
        if brick_under is not None:
            z = max(brick_under.z_positions)
            if z != brick.z - 1:
                brick.pos = (*brick.pos[:-1], z + 1)
            return
    brick.pos = (*brick.pos[:-1], 1)


def plot_bricks(brick_layers: dict[int, list[Brick]], level: int, ax, size: int = 31):
    if ax is None:
        return

    # Create axis
    z_max = max(brick_layers.keys())
    if z_max < size:
        window_up = z_max - level
        window_down = level - 1
    else:
        if level <= size // 2:
            window_down = level - 1
            window_up = size - window_down - 1
        elif level >= z_max - size // 2:
            window_up = z_max - level
            window_down = size - window_up - 1
        else:
            window_down = size // 2
            window_up = size // 2

    z_min, z_max = level - window_down, level + window_up

    axes = [10, 10, window_down + window_up + 1]

    data = np.zeros(axes)
    colors = np.empty(axes + [4])

    for d in range(z_min, z_max + 1):
        for brick in brick_layers[d]:
            for x, y, z in brick:
                if not (z_min <= z <= z_max):
                    continue
                data[x, y, z - z_min] = 1
                colors[x, y, z - z_min] = [*brick.color, alpha]

    # Plot figure
    ax.cla()
    ax.voxels(data, facecolors=colors, edgecolors='grey')
    ax.set_box_aspect(axes)
    for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
        axis.set_ticklabels([])
    ax.get_figure().canvas.draw_idle()
    ax.get_figure().canvas.start_event_loop(speed)


InputData = list[Brick]


def get_data() -> InputData:
    """Retrieve all the data to begin with."""
    l = lines_of_file(f"inputs/{DAY if not TEST else 'test'}.txt")
    return lmap(Brick.from_repr, l)


@section(day=DAY, part=1)
def part_1(bricks: InputData) -> int:
    """Code for section 1"""
    bricks = sorted(bricks)
    game_layers = dict[int, list[Brick]]()
    # create a grid with a mapping on depth
    for brick in bricks:
        for z in brick.z_positions:
            game_layers.setdefault(z, []).append(brick)
    # create empty layers
    for d in range(1, max(game_layers.keys())):
        if d not in game_layers:
            game_layers[d] = []

    for d, layer_bricks in game_layers.items():
        if len(layer_bricks) != len(set(map(id, layer_bricks))):
            raise RuntimeError(layer_bricks)
        pos = list(reduce(chain, layer_bricks, []))
        if len(set(pos)) != len(pos):
            raise RuntimeError("two bricks are on the same position at depth", d)

    if VERBOSE:
        fig = plt.figure()
        plt.show(block=False)
        ax = fig.add_subplot(111, projection='3d')
    else:
        ax = None

    for brick in bricks:
        before = set(brick.z_positions)  # keep track of previous depths
        make_fall(game_layers, brick)    # update brick depth
        after = set(brick.z_positions)   # new depths

        # update the layers of the game
        for z in before - after:
            if brick not in game_layers[z]:
                raise RuntimeError("Element doesn't exists", brick, z)
            game_layers[z].remove(brick)
        for z in after - before:
            if brick in game_layers[z]:
                raise RuntimeError("Element already exists", brick, z)
            game_layers[z].append(brick)

    if VERBOSE:
        plot_bricks(game_layers, 1, ax, size=4)
        plt.pause(500)

    not_safe = set[int]()
    for brick in bricks:
        if brick.z - 1 not in game_layers:
            continue
        layer_under = game_layers[brick.z - 1]
        bricks_under = lfilter(brick.is_brick_under, layer_under)
        if len(bricks_under) == 0:
            raise RuntimeError('A brick has not completly fallen', brick)
        if len(bricks_under) == 1:
            not_safe.add(id(bricks_under[0]))

    return len(bricks) - len(not_safe)


@section(day=DAY, part=2)
def part_2(data: InputData) -> int:
    """Code for section 2"""
    return 0


if __name__ == "__main__":
    part_1(get_data())  # P1: 407
    part_2(get_data())  # P2:
