from collections import defaultdict

from aoc import section, load_input


def parse(data: list[str]):
    """Parse input into ..."""
    i = data.index('')
    orders = defaultdict(set[int])
    for o in data[:i]:
        x1, x2 = o.split("|")
        orders[int(x1)].add(int(x2))

    class Page(int):
        def __lt__(self, p2): return self not in orders[p2]

    manuals = [tuple(map(Page, m.split(","))) for m in data[i+1:]]
    return orders, manuals


def is_right_ordered(m) -> bool:
    return all( m[i] < m[j] for i in range(len(m)) for j in range(i+1, len(m)) )


@section.p1(sol=4814)
def part_1() -> int:
    """Code for section 1"""
    orders, manuals = parse(load_input())
    return sum( m[len(m) // 2] for m in manuals if is_right_ordered(m) )


@section.p2(sol=5448)
def part_2() -> int:
    """Code for section 2"""
    orders, manuals = parse(load_input())
    return sum( sorted(m)[len(m) // 2] for m in manuals if not is_right_ordered(m))


if __name__ == "__main__":
    part_1()
    part_2()
