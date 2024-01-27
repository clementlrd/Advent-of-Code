"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Optional, Iterator, Iterable
from dataclasses import dataclass
from itertools import combinations, starmap, groupby, product
from functools import partial, reduce
from collections import Counter, defaultdict
from operator import and_, mul
import math

from utils import section, lmap
from utils_types import Coordinate3D, Coordinate


@dataclass(slots=True, frozen=True)
class HailStone:
    """Represents a HailStone by its position and its velocity."""
    p: Coordinate3D
    v: Coordinate3D

    def __getitem__(self, t: float) -> tuple[float, float]:
        """The position of the hailstone at a given time."""
        return (self.p[0] + t * self.v[0], self.p[1] + t * self.v[1])

    def intersect2D(self, h: HailStone, zone: Optional[Coordinate] = None) -> bool:
        """Whether two hailstones intersects in the future. A zone can also be specified."""
        t, u = intersection_time(self, h)
        return t >= 0 and u >= 0 and (zone is None or inside_zone(zone, self[t]))

    @classmethod
    def from_repr(cls, _repr: str) -> HailStone:
        """Create a Hailstone from an input line. Format: 'px, py, pz @ vx, vy, vz'."""
        px, py, pz, vx, vy, vz = lmap(int, _repr.replace(' @', ', ').split(', '))
        return cls((px, py, pz), (vx, vy, vz))


def inside_zone(zone: Coordinate, pos: tuple[float, float]) -> bool:
    """Whether the current position is inside the zone or not."""
    return zone[0] <= pos[0] <= zone[1] and zone[0] <= pos[1] <= zone[1]


def intersection_time(h1: HailStone, h2: HailStone):
    """Returns the time when each hailstone intersect the path of the other.

    Reference:
        - https://en.wikipedia.org/wiki/Line–line_intersection
    """

    x1, y1 = h1.p[0], h1.p[1]
    x2, y2 = x1 + h1.v[0], y1 + h1.v[1]

    x3, y3 = h2.p[0], h2.p[1]
    x4, y4 = x3 + h2.v[0], y3 + h2.v[1]

    d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if d == 0:  # parallel: doesn't intersect
        return -1, -1
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / d
    u = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / d
    return t, u


def factorize(n):
    """Count divisors of n along with its exponents."""
    fs, p = Counter[int](), 1
    while n > 1:
        p += 1
        if p > math.isqrt(n):
            # n is a prime number, it's its own divisor
            fs[n] += 1
            return fs

        while n % p == 0:
            # count p as a divisor with exponent and
            # remove all the divisor occurences from initial number
            n //= p
            fs[p] += 1
    return fs


def divisors(n: int) -> Iterator[int]:
    """Lists all the divisors of n."""
    def remaining_divisors(k: Counter[int]) -> Iterator[int]:
        if not k:
            yield 1
            return

        d, e = k.popitem()
        for r in remaining_divisors(k):
            for i in range(1 + e):
                yield d ** i * r

    return remaining_divisors(factorize(n))


def chinese_remainder(m: list[int], a: list[int]) -> int:
    """Resolves chinese remainder theorem where m is the list of pairwise coprimes
    and a is the list of remainders.

    It solves the following simultaneous congruences system for x: `x = a_i mod m_i`
    """
    _sum, prod = 0, reduce(mul, m)
    for mi, ai in zip(m, a):
        p = prod // mi
        _sum += ai * pow(p, -1, mi) * p
    return _sum % prod


class Contradiction(BaseException):
    """Raised when a contradiction appeares in a congruence system."""


def handle_same_prime(a1, a2, p, exp1, exp2):
    """Reduce two congruence equations where a1 and a2 are the remainders and
    the modulus is the same prime number p to the power of exp1 and exp2"""
    if exp1 >= exp2:
        if a1 % p ** exp2 == a2:
            return (a1, exp1)
        raise Contradiction()
    # otherwise exp2 > exp1
    return handle_same_prime(a1=a2, a2=a1, p=p, exp1=exp2, exp2=exp1)


def solve_system(system: Iterable[tuple[int, int]]) -> int:
    """Solves a system of congruence stored as an iterable of tuple
    where the first element is the remainder and the second element the modulus."""

    # Split congruences equation into equations were m is prime to be able to apply CRT.
    # We keep the power of the prime number to reduce equations with the same prime number later.
    system_split = {
        (a % (prime ** power), prime, power)
        for a, m in system
        for prime, power in factorize(m).items()
    }

    equations = defaultdict(list)
    for a, p, exp in system_split:
        # store equations according to the prime
        equations[p].append((a, exp))

    remainders, modulus = [], []
    for p, eqs in equations.items():
        # reduce equations with the same prime p
        a, exp = eqs[0]
        for _a, _exp in eqs[1:]:
            a, exp = handle_same_prime(a, _a, p, exp, _exp)
        remainders.append(a)
        modulus.append(p ** exp)

    return chinese_remainder(modulus, remainders)


def resolve_coordinate(hailstones: list[HailStone], dim: int) -> int:
    """Find the coordinate of the stone along a dimension."""
    # keep only position and velocity for the current dimension.
    h = lmap(lambda h: (h.p[dim], h.v[dim]), hailstones)
    # group hailstones by velocity to generate candidates for the velocity
    # using the fact that for i,j | v_i = v_j => (v_i - V) divide (p_i - p_j)
    grouped_by_velocity = groupby(sorted(h, key=lambda u: u[1]), lambda u: u[1])
    velocity_candidates = (
        {y * x + vi for y, x in product((1, -1), divisors(abs(pi - pj)))}
        for vi, h in grouped_by_velocity
        for pi, pj in combinations((p for p, _ in h), 2)
    )
    # take intersection to reduce candidates
    velocity_candidates = reduce(and_, velocity_candidates)

    for v in velocity_candidates:
        try:
            # if it returns, a solution has been found
            return solve_system({(pi, abs(vi - v)) for pi, vi in h})
        except Contradiction:
            continue
    raise ValueError('No solutions found to the system')


@section(year=2023, day=24, part=1, sol=11098)
def part_1(data: Iterator[str]) -> int:
    """Code for section 1"""
    hailstones = lmap(HailStone.from_repr, data)
    intersect = partial(HailStone.intersect2D, zone=(int(2e14), int(4e14)))
    return sum(starmap(intersect, combinations(hailstones, 2)))


@section(year=2023, day=24, part=2, sol=920630818300104)
def part_2(data: Iterator[str]) -> int:
    """Code for section 2

    Reference:
        - https://github.com/edoannunziata/jardin/blob/master/aoc23/AdventOfCode23.ipynb
    """
    hailstones = lmap(HailStone.from_repr, data)
    return sum((resolve_coordinate(hailstones, i) for i in range(3)))


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    part_1()
    part_2()
