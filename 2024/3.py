import re

from aoc import section, load_input

MUL = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
ENABLE = re.compile(r"do\(\)(.+?)don't\(\)")


@section.p1()
def part_1(sol=168539636) -> int:
    """Code for section 1"""
    data = " ".join(load_input())
    return sum(int(n1) * int(n2) for n1, n2 in  MUL.findall(data))
    

@section.p2(sol=97529391)
def part_2() -> int:
    """Code for section 2"""
    data = "do()" + " ".join(load_input()) + "don't()"
    return sum(int(n1) * int(n2) for e in ENABLE.findall(data) for n1, n2 in  MUL.findall(e))


if __name__ == "__main__":
    part_1()
    part_2()
