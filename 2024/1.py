from collections import Counter

from aoc import section, load_input


def parse(data: list[str]) -> tuple[list[int], list[int]]:
    """Parse input into two lists of int."""
    # each row contains one element for each one of the two lists, separated by 3 spaces
    parse_row = lambda a: map(int, a.split("   ")) 
    return tuple(zip(*map(parse_row, data)))


@section.p1(sol=1603498)
def part_1() -> int:
    """Code for section 1"""
    # sort the two lists
    l1, l2 = map(sorted, parse(load_input()))
    return sum(abs(a-b) for a, b in zip(l1, l2))


@section.p2(sol=25574739)
def part_2() -> int:
    """Code for section 2"""
    # count the integers in the two lists
    c1, c2 = map(Counter, parse(load_input()))
    return sum( i * n * c2[i] for i, n in c1.items())


if __name__ == "__main__":
    part_1()
    part_2()
