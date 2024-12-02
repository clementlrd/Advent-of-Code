from aoc import section, load_input

def parse(data: list[str]):
    """Parse input into ..."""
    return [ [int(e) for e in report.split(" ")] for report in data]

def is_safe(r: list[int], increasing=True, acc=0, part=1) -> bool:
    if acc > 1: return False
    for i, (e1, e2) in enumerate(zip(r[:-1], r[1:])):
        if increasing and 1 <= e2 - e1 <= 3: continue
        if not increasing and 1 <= e1 - e2 <= 3: continue
        if part == 1: return False
        return is_safe(r[:i] + r[i+1:], increasing, acc+1)\
            or is_safe(r[:i+1] + r[i+2:], increasing, acc+1)
    return True

@section.p1(sol=321)
def part_1() -> int:
    """Code for section 1"""
    data = parse(load_input())
    return sum(is_safe(r) or is_safe(r, increasing=False) for r in data)

@section.p2(sol=386)
def part_2() -> int:
    """Code for section 2"""
    data = parse(load_input())
    return sum(is_safe(r, part=2) or is_safe(r, increasing=False, part=2) for r in data)


if __name__ == "__main__":
    part_1()
    part_2()
