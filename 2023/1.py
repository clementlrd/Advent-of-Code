"""Resolve a daily problem"""  # pylint: disable=invalid-name
from typing import Callable, Iterator
from functools import partial
import re
from utils import lines_of_file, section, lfilter, compose

InputData = Iterator[str]

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


def calibration_value(s: str) -> int:
    """Compute calibration value of a string with integers represented as digits."""
    integers = lfilter(lambda c: '1' <= c <= '9', s)
    return int(integers[0] + integers[-1])


def tokenize_first_found(s: str, reverse=False) -> str:
    """Tokenize the first handwritten digit seen in the string.
    If `reverse` is set to True, it tokenizes the last one."""
    group = '|'.join(str_digits.keys())
    if not reverse:
        return re.sub(f"({group})", r'<\1>', s, count=1)
    return re.sub(f"({group[::-1]})", r'>\1<', s[::-1], count=1)[::-1]


def token_to_digit_fn(token_value: str) -> Callable[[str], str]:
    """Replace all digit tokens into its integer representation"""
    return lambda s: re.sub(f'<{token_value}>', str_digits[token_value], s)


def get_data() -> InputData:
    """Retrieve all the data to begin with."""
    return lines_of_file("inputs/1.txt")


@section(day=1, part=1)
def part_1(data: InputData) -> int:
    """Code for section 1"""
    return sum(map(calibration_value, data))


@section(day=1, part=2)
def part_2(data: InputData) -> int:
    """Code for section 2"""
    l = list(data)   # convert to list to use the iterator twice

    # create a function to convert all token types to the corresponding digit
    token_to_digit_map = map(token_to_digit_fn, str_digits.keys())
    tokens_to_digits = compose(*token_to_digit_map)

    # transform the first handwritten digit into a token then into a digit
    transform_first = compose(tokens_to_digits, tokenize_first_found)
    start_digits = map(transform_first, l)

    # transform the last word with the same process
    tokenize_last_found = partial(tokenize_first_found, reverse=True)
    transform_last = compose(tokens_to_digits, tokenize_last_found)
    end_digits = map(transform_last, l)

    # add the two strings to call calibration value function
    # because it depends only on the values on the edges
    l = map("".join, zip(start_digits, end_digits))

    return sum(map(calibration_value, l))


if __name__ == "__main__":
    part_1(get_data())  # P1: 55208
    part_2(get_data())  # P2: 54578
