"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Iterator, Iterable, Optional
from dataclasses import dataclass, field
from copy import deepcopy

import matplotlib.pyplot as plt
# pylint: disable-next=unused-import  # It has the side effect to allow 3D projection
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from numpy.random import sample
from tqdm import tqdm

from utils import section, lmap, lfilter
from utils_types import Coordinate3D, Coordinate

VERBOSE = False


@dataclass
class Brick:
    """Represents a brick of sand."""
    direction: int
    length: int
    pos: Coordinate3D
    color: tuple[float, ...] = field(default_factory=lambda: tuple(sample(size=3)))  # display color
    proj: set[Coordinate] = field(init=False)                      # projection in (x,y) coordinates

    def __post_init__(self) -> None:
        self.proj = set(map(lambda c: c[:-1], self))

    @property
    def z(self) -> int:
        """Shorthand for z coordinate."""
        return self.pos[-1]

    @property
    def z_positions(self) -> Iterator[int]:
        """Shorthand to access all the z coordinates occupied by the brick."""
        if self.direction == 2:
            for l in range(self.length if self.direction == 2 else 1):
                yield self.z + l
            return
        yield self.z

    def is_brick_under(self, brick: Brick) -> bool:
        """Returns whether the given brick is under the current_brick."""
        return len(brick.proj & self.proj) > 0 and brick < self

    def __lt__(self, brick: Brick) -> bool:
        """Compare two bricks based on brick height."""
        if self.z == brick.z and self.direction == 2:
            return self.length < brick.length
        return self.z < brick.z

    def __iter__(self) -> Iterator[Coordinate3D]:
        """Iterate over all brick's coordinates."""
        for l in range(self.length):
            x, y, z = (x + (l if self.direction == i else 0) for i, x in enumerate(self.pos))
            yield (x, y, z)

    @classmethod
    def from_repr(cls, _repr: str) -> Brick:
        """Create a brick from its representation 'x1,y1,z1~x2,y2,z2' """
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


class SandFall:
    """Represents a sandfall as a collection of sand bricks.
    It starts as a snapshot and gravity can be applied to make sand brick fall to the bottom.
    It can be displayed.
    """

    def __init__(self, bricks: Iterable[Brick]) -> None:
        self.bricks = sorted(bricks)
        self.dim = (10, 10, self.bricks[-1].z)
        self._init_layers()
        self._init_display()

    def _init_layers(self) -> None:
        """Init layers representation: each height is mapped to
        all the bricks that have a coordinate in that height."""
        self.layers = dict[int, list[Brick]]()
        # create a grid with a mapping on depth
        for brick in self.bricks:
            for z in brick.z_positions:
                self.layers.setdefault(z, []).append(brick)

        # create empty layers
        for d in range(1, self.dim[-1]):
            if d not in self.layers:
                self.layers[d] = []

    def _init_display(self) -> None:
        if not VERBOSE:
            self.fig, self.ax = None, None
            return
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        plt.show(block=False)

    def apply_gravity(self, display_steps=True) -> int:
        """Apply gravity to all the bricks."""
        brick_moved = 0
        for brick in self.bricks:
            if display_steps:
                self.update_display(brick.z)  # display

            before = set(brick.z_positions)   # keep track of previous depths
            if self.make_brick_fall(brick):   # update brick depth
                brick_moved += 1
            after = set(brick.z_positions)    # new depths

            # update the layers of the game
            self.remove_brick(brick, pos=before - after)
            self.add_brick(brick, pos=after - before)

        # update brick order
        self.bricks.sort()

        return brick_moved

    def make_brick_fall(self, brick: Brick) -> bool:
        """Apply gravity to only one brick."""
        for z in range(brick.z, 0, -1):
            brick_under = next(filter(brick.is_brick_under, self.layers[z]), None)
            if brick_under is not None:
                if z != brick.z - 1:
                    brick.pos = (*brick.pos[:-1], z + 1)
                    return True
                return False
        if brick.z == 1:
            return False
        brick.pos = (*brick.pos[:-1], 1)
        return True

    def remove_brick(self, brick: Brick, pos: Optional[Iterable[int]] = None):
        """Remove a brick from the layers of the sandfall."""
        if pos is None:
            pos = brick.z_positions
        for z in pos:
            self.layers[z].remove(brick)

    def add_brick(self, brick: Brick, pos: Optional[Iterable[int]] = None):
        """Add a brick to the layers of the sandfall."""
        if pos is None:
            pos = brick.z_positions
        for z in pos:
            self.layers[z].append(brick)

    def not_safe_desintegrate(self) -> Iterator[Brick]:
        """Compute the bricks that are not safe to desintegrate
        i.e. bricks which make other bricks fall when desintegrated."""
        not_safe = set[int]()
        for brick in self.bricks:
            if brick.z - 1 not in self.layers:
                continue
            layer_under = self.layers[brick.z - 1]
            bricks_under = lfilter(brick.is_brick_under, layer_under)
            if len(bricks_under) == 0:
                raise RuntimeError('A brick hasn\'t fallen over completely', brick)
            if len(bricks_under) == 1 and id(b := bricks_under[0]) not in not_safe:
                not_safe.add(id(b))
                yield b

    def update_display(
        self, level: int = 0,
        timeout: float = .1, size: int = 25, alpha: float = .9
    ) -> None:
        """Update the sandfall view on the display.

        Args:
            level (int, optional): The level of the current view. Defaults to 0.
            timeout (float, optional): The time between two displays. Defaults to .1.
            size (int, optional): The size of the view. Defaults to 25.
            alpha (float, optional): The alpha value for brick's color. Defaults to .9.
        """
        if self.fig is None or self.ax is None:
            return  # no verbose

        # Create axis for the view
        mx, my, mz = self.dim
        if level <= size // 2:
            window_down = level - 1
            window_up = size - window_down - 1 if mz >= size else mz - level
        elif level >= mz - size // 2:
            window_up = mz - level
            window_down = size - window_up - 1 if mz >= size else level - 1
        else:
            window_down = size // 2
            window_up = size // 2
        axes = [mx, my, window_down + window_up + 1]
        z_min, z_max = level - window_down, level + window_up

        # create data to plot
        data, colors = np.zeros(axes), np.empty(axes + [4])

        for d in range(z_min, z_max + 1):
            for brick in self.layers[d]:
                for x, y, z in brick:
                    if not z_min <= z <= z_max:
                        continue
                    data[x, y, z - z_min] = 1
                    colors[x, y, z - z_min] = [*brick.color, alpha]

        # Plot on figure
        self.ax.cla()
        self.ax.voxels(data, facecolors=colors, edgecolors='grey')  # type:ignore
        self.ax.set_box_aspect(axes)                                # type:ignore
        for axis in [self.ax.xaxis, self.ax.yaxis, self.ax.zaxis]:  # type:ignore
            axis.set_ticklabels([])
        self.fig.canvas.draw_idle()
        self.fig.canvas.start_event_loop(timeout)


@section(year=2023, day=22, part=1, sol=407)
def part_1(data: Iterator[str]) -> int:
    """Code for section 1"""
    bricks = lmap(Brick.from_repr, data)
    sand_fall = SandFall(bricks)
    sand_fall.update_display(timeout=1)
    sand_fall.apply_gravity()
    sand_fall.update_display(timeout=1)
    not_safe = sand_fall.not_safe_desintegrate()
    return len(sand_fall.bricks) - len(tuple(not_safe))


@section(year=2023, day=22, part=2, sol=59266)
def part_2(data: Iterator[str]) -> int:
    """Code for section 2"""
    # pylint: disable-next=unused-variable, redefined-outer-name
    VERBOSE = False  # change verbose to avoid create figures while copying the sandfall
    bricks = lmap(Brick.from_repr, data)
    sand_fall = SandFall(bricks)
    sand_fall.apply_gravity(display_steps=False)
    not_safe = sorted(sand_fall.not_safe_desintegrate())

    total = 0
    for brick in tqdm(not_safe[::-1]):
        test_sand_fall = deepcopy(sand_fall)
        test_sand_fall.remove_brick(brick)
        total += test_sand_fall.apply_gravity()

    return total


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    part_1()
    part_2()
