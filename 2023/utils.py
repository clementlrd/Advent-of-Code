"""A module to make dev faster."""
from typing import TypeVar, Callable, Literal
from collections.abc import Iterable, Iterator
from itertools import chain

T = TypeVar('T')
S = TypeVar('S')


def lmap(fn: Callable[[T], S], iterable: Iterable[T]) -> list[S]:
    """list of a map object. Shorthand."""
    return list(map(fn, iterable))


def lfilter(fn: Callable[[T], bool], iterable: Iterable[T]) -> list[T]:
    """list of a map object. Shorthand."""
    return list(filter(fn, iterable))


def flatten(nested_list: Iterable) -> Iterator:
    """Flatten a nested list. The list can be arbitrary nested.

    Example:
    >>> l = [[1, 2, 3], [[3, 4], 5], [6, [7, [8, 9]]]]
    >>> print(*flatten(l))
    1 2 3 3 4 5 6 7 8 9
    """
    if not isinstance(nested_list, Iterable):
        return iter((nested_list,))
    return (e for l in nested_list for e in flatten(l))


def print_matrix(matrix: list[Iterable]) -> None:
    """Print a matrix in a simple format"""
    for r in matrix:
        print(r)


def find_element(l: list[T], fn: Callable[[T], bool]) -> tuple[int, T | None]:
    """Find an element in a list."""
    for i, x in enumerate(l):
        if fn(x):
            return i, x
    return -1, None


def crange(c: tuple[int, int]):
    """Enumerate all tuple elements from (0,0) to `c`"""
    x, y = c
    for i in range(x):
        for j in range(y):
            yield (i, j)


def neighbourhood(
        x: tuple[int, int],
        mat_size: tuple[int, int],
        connectivity: Literal[4] | Literal[8] = 4
) -> Iterator:
    """enumerate all neighbors positions in a grid with the given connectivity.
    Take into account the size of the grid.

    Args:
        x (tuple[int, int]): The current position.
        mat_size (tuple[int, int]): The size of the matrix.
        connectivity (int, optional): The connectivity of the grid. Defaults to 4.

    Raises:
        NotImplementedError: Only a connectivity of 4 and 8 is implemented

    Yields:
        Iterator: A position of a neighbor.
    """
    n, m, i, j = *mat_size, *x

    cross = iter((
        (max(i - 1, 0), j),
        (min(i + 1, n - 1), j),
        (i, max(j - 1, 0)),
        (i, min(j + 1, m - 1))
    ))

    if connectivity == 4:
        return cross

    diag = iter((
        (max(i - 1, 0), max(j - 1, 0)),
        (min(i + 1, n - 1), min(j + 1, m - 1)),
        (min(i + 1, n - 1), max(j - 1, 0)),
        (max(i - 1, 0), min(j + 1, m - 1))
    ))

    if connectivity == 8:
        return chain(cross, diag)

    raise NotImplementedError


def lines_of_file(path: str) -> Iterator[str]:
    """Return all lines of a file as an iterator. Remove the `\n` escape character."""
    with open(path, "r", encoding="UTF8") as file:
        return map(lambda s: s[:-1], file.readlines())


if __name__ == "__main__":
    pass
