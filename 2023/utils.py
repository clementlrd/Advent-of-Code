"""A module to make dev faster."""
from typing import Callable, Literal, Any
from collections.abc import Iterable, Iterator
from itertools import chain
from functools import reduce
import time
from utils_types import T, S, Coordinate, Grid

#  ============================
#
#  Specific to advent of code
#
#  ============================


def section(day: int, part: int):
    """Section decorator to handle result printing and time execution."""
    def decorator(part_fn: Callable):
        def wrapper(*args, **kwargs) -> None:
            t0 = time.time()
            result = part_fn(*args, **kwargs)
            execution_time = time.time() - t0

            def print_fn(x):
                return print(x, f"\n\nExecution time: {execution_time:.5f}s", end="")
            print_answer(result, day=day, part=part, print_fn=print_fn)

        return wrapper
    return decorator


def lines_of_file(path: str) -> Iterator[str]:
    """Return all lines of a file as an iterator. Remove the `\n` escape character."""
    with open(path, "r", encoding="utf-8") as file:
        return map(lambda s: s[:-1], file.readlines())


def print_answer(answer, day: int, part: int, print_fn=print) -> None:
    """Shorthand to print answer."""
    print("=" * 50)
    print(f"[DAY {day}] Answer to part {part} is:\n\n\t")
    print_fn(answer)
    print("\n", "=" * 50, sep="")

# ======
#
#  Utils
#
# ======

#
#  Itertools
#


def lmap(fn: Callable[[T], S], iterable: Iterable[T]) -> list[S]:
    """list of a map object. Shorthand."""
    return list(map(fn, iterable))


def lfilter(fn: Callable[[T], bool] | None, iterable: Iterable[T]) -> list[T]:
    """list of a map object. Shorthand."""
    return list(filter(fn, iterable))


def iter_split(char: str, iterable: Iterable[str]) -> Iterable[list[str]]:
    """Map a string into a list of strings split on a acharacter. Shorthand."""
    return map(lambda s: s.split(char), iterable)


def flatten(nested_list: Iterable) -> Iterator:
    """[DEPRECATED] Use more_itertools.flatten instead
    Flatten a nested list. The list can be arbitrary nested.

    Example:
    >>> l = [[1, 2, 3], [[3, 4], 5], [6, [7, [8, 9]]]]
    >>> print(*flatten(l))
    1 2 3 3 4 5 6 7 8 9
    """
    if not isinstance(nested_list, Iterable):
        return iter((nested_list,))
    return (e for l in nested_list for e in flatten(l))


def find_element(l: list[T], fn: Callable[[T], bool]) -> tuple[int, T | None]:
    """Find an element in a list."""
    for i, x in enumerate(l):
        if fn(x):
            return i, x
    return -1, None


def crange(c: tuple[int, int]):
    """[DEPRECATED] use itertools.product(range(n), range(m)) instead
    Enumerate all tuple elements from (0,0) to `c`"""
    x, y = c
    for i in range(x):
        for j in range(y):
            yield (i, j)


def compose(
        fn: Callable[[Any], S],
        *func: Callable[[T], Any],
        repeat: int = 1
) -> Callable[[T], S]:
    """Compose functions.
    Returns a function that chain all the functions given in parameter.

    Args:
        *func (Callable): the functions chained, called from right to left.
        repeat (int): The number of times to repeat the composition. Default: 1.
    """  # fn is used for typing: it allows to determine the output type.

    def comp(f, g):
        return lambda x: f(g(x))

    return reduce(comp, (fn, *func) * repeat)

#
#  Grid
#


def grid_map(
    fn: Callable[[tuple[int, int], T], S] | Callable[[T], S],
    grid: Grid[T],
    pos=False
) -> Grid[S]:
    """Map a function over a grid. The function needs to take the position and the element as input.
    It returns a new grid."""
    return [
        [fn((i, j), e) if pos else fn(e) for j, e in enumerate(row)]  # type: ignore
        for i, row in enumerate(grid)
    ]


def enumerate_grid(grid: Grid[T]) -> Iterator[tuple[Coordinate, T]]:
    """Enumerate over a grid, yield an element along with its position."""
    for i, row in enumerate(grid):
        for j, e in enumerate(row):
            yield (i, j), e


def enumerate_cols(grid: Grid[T]) -> Iterator[tuple[int, list[T]]]:
    """Iterate over the columns of a grid."""
    for j in range(len(grid[0])):
        yield j, [grid[i][j] for i in range(len(grid))]


def transpose(grid: Grid[T]) -> Grid[T]:
    """Transpose a grid as it was a matrix."""
    return [[grid[i][j] for i in range(len(grid))] for j in range(len(grid[0]))]


def mirror(grid: Grid[T], axis=1) -> Grid[T]:
    """Mirror the grid along a given axis."""
    if axis == 0:
        return grid[::-1]
    if axis == 1:
        return [row[::-1] for row in grid]
    raise ValueError(f"axis {axis} is not valid. Please enter 0 or 1.")


def rotate90(grid: Grid[T], clockwize=True) -> Grid[T]:
    """Rotates a grid clockwise or not. Defaults: Clockwize."""
    return mirror(transpose(grid), axis=clockwize)


def subgrid(grid: Grid[T], start: Coordinate, end: Coordinate) -> Grid[T]:
    """Create a subgrid of a grid. Works as range objects, but in two dimensions."""
    (si, sj), (ei, ej) = start, end
    return [row[sj:ej] for row in grid[si:ei]]


def print_grid(grid: Grid) -> None:
    """Print a matrix in a simple format."""
    for r in grid:
        print(*r)


def neighborhood(
        x: Coordinate,
        mat_size: tuple[int, int],
        connectivity: Literal[4] | Literal[8] = 4,
        coordinates=True
) -> Iterator[Coordinate]:
    """enumerate all neighbors positions in a grid with the given connectivity.
    Take into account the size of the grid.

    Args:
        x (Coordinate): The current position.
        mat_size (tuple[int, int]): The size of the matrix.
        connectivity (int, optional): The connectivity of the grid. Defaults to 4.
        coordinates (bool, optional): Returns the coordinates if True, returns the directions
        otherwise. Defaults True.

    Raises:
        NotImplementedError: Only a connectivity of 4 and 8 is implemented

    Yields:
        Iterator[Coordinates]: A position of a neighbor.
    """
    n, m, i, j = *mat_size, *x

    c4 = iter(((-1, 0), (1, 0), (0, -1), (0, 1)))
    c8 = iter(((-1, -1), (1, 1), (-1, 1), (1, -1)))

    directions = c4
    if connectivity == 8:
        directions = chain(directions, c8)
    if connectivity not in (4, 8):
        raise NotImplementedError(f"connectivity {connectivity} is not supported")

    for di, dj in directions:
        if 0 <= i + di < n and 0 <= j + dj < m:
            if coordinates:
                yield i + di, j + dj
            else:
                yield di, dj


def manhattan_distance(x1: Coordinate, x2: Coordinate) -> int:
    """Compute manhattan distance for two points."""
    return sum(abs(x - y) for x, y in zip(x1, x2))
