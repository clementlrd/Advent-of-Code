"""Resolve a daily problem"""  # pylint: disable=invalid-name
from typing import Iterable, Any
import os
from utils import lines_of_file, neighborhood

DATA_PATH = "inputs/"
DAY = os.path.basename(__file__).split(".")[0]


def get_data() -> Iterable[str]:
    """Retrieve all the data to begin with."""
    l = lines_of_file(f"{DATA_PATH}{DAY}.txt")
    return l


def part_1() -> None:
    """Code for section 1"""
    l = list(get_data())
    part_numbers = []

    for i, row in enumerate(l):
        current_number, is_part_number = "", False
        for j, c in enumerate(row):
            if not '0' <= c <= '9':
                if is_part_number and current_number:
                    # we leave a part number, thus we add it in teh list
                    part_numbers.append(int(current_number))
                # we make sur that we are not working on a number anymore
                current_number, is_part_number = "", False
                continue  # nothing to see here

            # we are in a number. keeping track of it
            current_number += c
            for vi, vj in neighborhood((i, j), mat_size=(len(l), len(row)), connectivity=8):
                neighbor = l[vi][vj]
                if '0' <= neighbor <= '9' or neighbor == '.':
                    # empty space or number, nothing to see here
                    continue
                # a special character has been detected, it is a part number
                is_part_number = True

        # make sur to had a number which is at the end of a line
        if is_part_number and current_number:
            part_numbers.append(int(current_number))

    print_answer(sum(part_numbers), part=1)


def part_2() -> None:
    """Code for section 2"""
    l = list(get_data())

    part_numbers = []
    # keep track of the parts numbers linked to a gear
    gears_linked = {}

    for i, row in enumerate(l):
        current_number, is_part_number, gear = "", False, None
        for j, c in enumerate(row):
            if not '0' <= c <= '9':
                if is_part_number and current_number:
                    part_numbers.append(int(current_number))
                    if gear is not None:
                        # we are around a gear, keep track of the part number
                        gears_linked[gear].append(int(current_number))
                current_number, is_part_number, gear = "", False, None
                continue

            current_number += c
            for vi, vj in neighborhood((i, j), mat_size=(len(l), len(row)), connectivity=8):
                neighbor = l[vi][vj]
                if neighbor == "*":
                    # we found a gear
                    gear = (vi, vj)
                    gears_linked.setdefault(gear, [])
                if '0' <= neighbor <= '9' or neighbor == '.':
                    # empty space or number
                    continue
                is_part_number = True

        if is_part_number and current_number:
            part_numbers.append(int(current_number))
            if gear is not None:
                gears_linked[gear].append(int(current_number))

    # gear ratios as two adjacent part numbers
    l = filter(lambda x: len(x) == 2, gears_linked.values())
    # gear ration is a multiplication of the two part numbers
    l = map(lambda x: x[0] * x[1], l)
    print_answer(sum(l), part=2)


def print_answer(answer: Any, part, print_fn=print) -> None:
    """Shorthand to print answer."""
    print("=" * 50)
    print(f"[DAY {DAY}] Answer to part {part} is:\n\n\t")
    print_fn(answer)
    print("\n", "=" * 50, sep="")


if __name__ == "__main__":
    part_1()  # 514969
    part_2()  # 78915902
