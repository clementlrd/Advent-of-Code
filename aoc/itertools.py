from typing import Callable, Iterable, Iterator
import itertools
from more_itertools import flatten


from . import T, S, Args


def lmap(fn: Callable[[T], S], iterable: Iterable[T]) -> list[S]:
    """list of a map object. Shorthand."""
    return list(map(fn, iterable))


def lfilter(fn: Callable[[T], bool] | None, iterable: Iterable[T]) -> list[T]:
    """list of a map object. Shorthand."""
    return list(filter(fn, iterable))


def starfilter(fn: Callable[[*Args], bool], iterable: Iterable[tuple[*Args]]) -> Iterator[tuple[*Args]]:
    """filter for a function with multiple arguments."""
    return filter(lambda x: fn(*x), iterable)


def iter_split(char: str, iterable: Iterable[str]) -> Iterator[list[str]]:
    """Map a string into a list of strings split on a acharacter. Shorthand."""
    return (s.split(char) for s in iterable)


def find(l: list[T], fn: Callable[[T], bool]) -> tuple[int, T | None]:
    """Find an element in a list along with its index."""
    for i, x in enumerate(l):
        if fn(x):
            return i, x
    return -1, None


def crange(c: tuple[int, int]):
    """[DEPRECATED] try to use itertools.product(range(n), range(m)) instead.
    Enumerate all tuple elements from (0,0) to `c`"""
    return itertools.product(range(c[0]), range(c[1]))


def compose(fn: Callable[[T], S], *func: Callable[[T], T]) -> Callable[[T], S]:
    """Compose functions.
    Returns a function that chain all the functions given in parameter.

    Args:
        *func (Callable): the functions chained, called from right to left.
    """  # fn is used for typing: it allows to determine the output type.

    def wrapper(x: T) -> S:
        for f in reversed(func):
            x = f(x)
        return fn(x)

    return wrapper