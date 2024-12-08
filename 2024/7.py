from aoc import section, load_input
from aoc.itertools import lmap

def parse(data: list[str]):
    """Parse input into ..."""
    values, equations = zip(*(r.split(": ") for r in data))
    return lmap(int, values), [lmap(int, eq.split(" ")) for eq in equations]
    

def test_equation(eq: list[int], test_value: int, acc=0) -> bool:
    if not len(eq):
        return test_value == acc
    return test_equation(eq[1:], test_value, acc + eq[0]) \
        or test_equation(eq[1:], test_value, acc * eq[0])

def test_equation_2(eq: list[int], test_value: int, acc=0) -> bool:
    if not len(eq):
        return test_value == acc
    return test_equation_2(eq[1:], test_value, acc + eq[0]) \
        or test_equation_2(eq[1:], test_value, acc * eq[0]) \
        or test_equation_2(eq[1:], test_value, int(str(acc) + str(eq[0])))

@section.p1(sol=8401132154762)
def part_1() -> int:
    """Code for section 1"""
    values, equations = parse(load_input())
    return sum(v for v, eq in zip(values, equations) if test_equation(eq, v) )
    

@section.p2(sol=95297119227552)
def part_2() -> int:
    """Code for section 2"""
    values, equations = parse(load_input())
    return sum(v for v, eq in zip(values, equations) if test_equation(eq, v) or test_equation_2(eq, v) )

if __name__ == "__main__":
    part_1()
    part_2()
