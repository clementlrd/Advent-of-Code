from typing import Optional, Callable, TypeVar, TypeVarTuple
from pathlib import Path
from time import time
from functools import partial
import requests
import sys


def _section(part: int, sol: Optional[int] = None):
    """Section decorator to handle result printing and time execution.
    Part of the section has to be provided for printing reasons.
    A solution can also be provided to verify the output of the function (usefull in case of refactor)."""

    def decorator(part_fn: Callable):
        def wrapper(*args) -> None:

            # execute section with time recording
            t0 = time()
            result = part_fn()
            execution_time = time() - t0

            # check the result if a solution is given
            if sol is not None and result != sol:
                raise ValueError(
                    "The result of the function is not the result awaited."
                    f"The function returned {result} instead of {sol}"
                )

            # print the answer and execution time 
            print_answer(result, int(Path(sys.argv[0]).stem), part, execution_time)

        return wrapper
    return decorator


class section:
    """Collection of decorators depending on the chosen part.
    Used through @section.p1()."""

    p1 = partial(_section, part=1)
    p2 = partial(_section, part=2)


def load_input(
    day: Optional[int]=None, year: Optional[int]=None,
    path: Optional[Path] = None, test: bool = False
) -> list[str]:
    """Load the data of the day stored in the path `./{year}/inputs/{day}.txt`.
    the day and the year can be automatically determined from the path of the script and can be omitted.
    - If the file doesn't exist, it will requests the input from advent of code.
    For this case, a session cookie has to be saved in a file '.session' for this function to work.
    - If a path is given, the function will try to load the file instead.
    - If `test` is set to True, the function will load the data in `inputs/test.txt` instead."""

    # retrieve day and path if not provided
    script_path = Path(sys.argv[0])
    day_ = day or int(script_path.stem)
    year_ = year or int(script_path.parent.name)

    # build input path
    path_ = Path(path or f"./{year_}/inputs/{day_}.txt").resolve()

    # test mode: make sure the test file exists
    if test:
        path_ = path_.parent / 'test.txt'
        path_.touch(exist_ok=True)

    # download input if the file doesn't exists
    if not path_.exists() and path is None:
        path_.parent.mkdir(exist_ok=True, parents=True)
        download_input(day_, year_, path_)

    # return input as a list of lines
    return path_.read_text().splitlines()


def download_input(day: int, year: int, output_path: Path, cookie: Optional[Path]=None) -> None:
    """Download the input for the given `day` and `year` and write it in the `output_file` file.
    Requires the path to a cookie to be able to download it, default is the `.session` file."""

    cookie_ = cookie or Path(".session")
    if not cookie_.exists():
        raise FileNotFoundError("Cookie `.session` not found, can't download the input.")

    # downloading file
    print(f"downloading input from day {day} of year {year}...")
    session = cookie_.read_text(encoding='utf-8')
    response = requests.get(
        f"https://adventofcode.com/{year}/day/{day}/input",
        headers={"User-Agent": "clem.laroudie@gmail.com"},
        cookies={"session": session}, timeout=1
    )
    if response.status_code != 200:
        raise requests.ConnectionError(response=response)

    # write result to file
    output_path.write_text(response.text, encoding='utf-8')


def print_answer(answer, day: int, part: int, execution_time: Optional[float]=None) -> None:
    """Prettier print of the answer. Needs information about the day and the part.
    The execution time can also be provided."""

    print("=" * 50)
    print(f"[DAY {day}] Answer to part {part} is:\t{answer}")
    if execution_time:
        print(f"\nExecution time: {execution_time:.5f}s", end="")
    print("\n", "=" * 50, sep="")

#
#  Types
#

T = TypeVar('T')
S = TypeVar('S')
Args = TypeVarTuple('Args')
