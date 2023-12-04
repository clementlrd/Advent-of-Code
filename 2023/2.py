"""Resolve a daily problem"""  # pylint: disable=invalid-name
from typing import Iterable, Any
import os
from utils import reduce, lines_of_file

DATA_PATH = "inputs/"
DAY = os.path.basename(__file__).split(".")[0]

Set = tuple[int, int, int]
Game = list[Set]


max_number_per_color = 12, 13, 14


def format_set(s: str) -> Set:
    """Return a tuple of int in format (R, G, B) representing
    the number of cubes retrieved from the bag once, during a game."""
    colors: dict[str, int] = {"red": 0, "green": 0, "blue": 0}
    for cube_color in s.split(", "):
        nbr, color = cube_color.split(" ")
        colors[color] = int(nbr)
    return (colors["red"], colors["green"], colors["blue"])


def get_data() -> Iterable[tuple[int, Game]]:
    """Retrieve all the data to begin with."""
    l = lines_of_file(f"{DATA_PATH}{DAY}.txt")
    l = map(lambda s: s.split(": ")[-1], l)         # retrieve all the sets as a string
    l = map(lambda s: s.split("; "), l)             # split all the sets
    l = map(lambda g: list(map(format_set, g)), l)  # format the sets as a tuple (R,G,B)
    # add the id along with the game
    return map(lambda idg: (idg[0] + 1, idg[1]), enumerate(l))


def is_valid_game(game: Game) -> bool:
    """Check if a game has a valid number of cubes retrieved."""
    return all(
        # the number of cubes is smaller than the max for this color
        n <= M
        for cube_set in game
        for n, M in zip(cube_set, max_number_per_color)
    )


def valid_game_id(game_with_id: tuple[int, Game]) -> int:
    """Return game id if the game is valid. Otherwise return 0."""
    id, game = game_with_id
    return id if is_valid_game(game) else 0


def part_1() -> None:
    """Code for section 1"""
    l = get_data()
    s = sum(map(valid_game_id, l))  # sum valid IDs

    print_answer(s, part=1)


def reduce_game(game_with_id: tuple[int, Game]) -> Set:
    """Reduce a game to the set of the minimum cubes required.
    It's the maximum number of a ball color on a game."""
    return reduce(
        lambda fs, s: (
            max(fs[0], s[0]),  # type: ignore
            max(fs[1], s[1]),  # type: ignore
            max(fs[2], s[2])   # type: ignore
        ),
        game_with_id[1], (0, 0, 0)
    )


def set_power(s: Set):
    """Return the power value of a set."""
    return s[0] * s[1] * s[2]


def part_2() -> None:
    """Code for section 2"""
    l = get_data()
    l = map(reduce_game, l)
    power = sum(map(set_power, l), start=0)

    print_answer(power, part=2)


def print_answer(answer: Any, part: int, print_fn=print) -> None:
    """Shorthand to print answer."""
    print("=" * 50)
    print(f"[DAY {DAY}] Answer to part {part} is:\n\n\t")
    print_fn(answer)
    print("\n", "=" * 50, sep="")


if __name__ == "__main__":
    part_1()  # 2679
    part_2()  # 77607
