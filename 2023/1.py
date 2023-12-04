"""Resolve a daily problem"""  # pylint: disable=invalid-name
from typing import Any
import os
import re
from utils import lines_of_file

DATA_PATH = "inputs/"
DAY = os.path.basename(__file__).split(".")[0]

str_digits = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}


def get_data():
    """Retrieve all the data to begin with."""
    return lines_of_file(f"{DATA_PATH}{DAY}.txt")


def int_in_str(s: str) -> str:
    """Retrieve int characters as a substring from an original string."""
    return "".join(filter(lambda c: '1' <= c <= '9', s))


def part_1() -> None:
    """Code for section 1"""
    # retrieve int in string and compute score
    digits = map(int_in_str, get_data())
    calibration_values = map(lambda s: int(s[0] + s[-1]), digits)

    print_answer(sum(calibration_values), part=1)


def replace_all_digit_tokens(s: str) -> str:
    """Replace all digit tokens into its integer representation"""
    for str_digit, digit in str_digits.items():
        s = re.sub(f'<{str_digit}>', digit, s)
    return s


def part_2() -> None:
    """Code for section 2"""
    l = list(get_data())

    # transform the first word into a token then into an int
    reg = rf"({'|'.join(str_digits.keys())})"
    start_digits = map(lambda s: re.sub(reg, r'<\1>', s, count=1), l)  # create token
    start_digits = map(replace_all_digit_tokens, start_digits)
    start_digits = map(int_in_str, start_digits)

    # transform the last word with the same process (reverse string order)
    reg_rev = rf"({'|'.join(str_digits.keys())[::-1]})"
    end_digits = map(lambda s: re.sub(reg_rev, r'>\1<', s[::-1], count=1)[::-1], l)  # create token
    end_digits = map(replace_all_digit_tokens, end_digits)
    end_digits = map(int_in_str, end_digits)

    # compute calibration value
    calibration_values = map(lambda s: int(s[0][0] + s[1][-1]), zip(start_digits, end_digits))

    print_answer(sum(calibration_values), part=2)


def print_answer(answer: Any, part: int, print_fn=print) -> None:
    """Shorthand to print answer."""
    print("=" * 50)
    print(f"[DAY {DAY}] Answer to part {part} is:\n\n\t")
    print_fn(answer)
    print("\n", "=" * 50, sep="")


if __name__ == "__main__":
    part_1()  # 55208
    part_2()  # 54578
