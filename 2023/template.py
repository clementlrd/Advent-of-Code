"""Resolve a daily problem"""  # pylint: disable=invalid-name
from typing import Iterable, Callable, Optional, Any
# pylint: disable-next=unused-import
from dataclasses import dataclass, field
import os
import __main__
# import numpy as np
from utils import lines_of_file

DATA_PATH = "inputs/"
DAY = os.path.basename(__file__).split(".")[0]
PART = 1
TEST = True


def get_data() -> Iterable[str]:
    """Retrieve all the data to begin with."""
    l = lines_of_file(f"{DATA_PATH}{DAY if not TEST else 'test'}.txt")
    return l


def part_1() -> None:
    """Code for section 1"""
    l = get_data()

    print_answer(None)


def part_2() -> None:
    """Code for section 2"""
    l = get_data()

    print_answer(None)


def main(fn: Optional[Callable[[], None]] = None) -> None:
    """Main process"""
    if fn is not None:
        return fn()
    ex = vars(__main__)[f"part_{PART}"]
    return ex()


def print_answer(answer: Any, part=PART, print_fn=print) -> None:
    """Shorthand to print answer."""
    print("=" * 50)
    print(f"[DAY {DAY}] Answer to part {part} is:\n\n\t")
    print_fn(answer)
    print("\n", "=" * 50, sep="")


if __name__ == "__main__":
    main()
