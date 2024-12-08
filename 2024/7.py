from operator import add, mul

from aoc import section, load_input
from aoc.itertools import lmap

def concat(a: int, b: int) -> int: return int(str(a) + str(b))
OPS = {"+": add, "*": mul, "||": concat}


def test_equation(equation: list[int], test_value: int, ops=["+", "*"]) -> bool:
    def test(eq: list[int], acc=0):
        if not len(eq):
            return test_value == acc
        if acc > test_value:
            return False
        return any(test(eq[1:], OPS[op](acc, eq[0])) for op in ops)
    return test(equation)


def parse(data: list[str]) -> tuple[list[int], list[list[int]]]:
    """Parse input into ..."""
    values, equations = zip(*(r.split(": ") for r in data))
    return lmap(int, values), [lmap(int, eq.split(" ")) for eq in equations]


@section.p1(sol=8401132154762)
def part_1() -> int:
    """Code for section 1"""
    values, equations = parse(load_input())
    return sum(v for v, eq in zip(values, equations) if test_equation(eq, v))


@section.p2(sol=95297119227552)
def part_2() -> int:
    """Code for section 2"""
    return sum(
        value for value, eq in zip(*parse(load_input()))
        if test_equation(eq, value) or test_equation(eq, value, ["+", "*", "||"])
    )

if __name__ == "__main__":
    part_1()
    part_2()
