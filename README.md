# Advent-of-Code

This repository includes all my code for the challenge [Advent of Code (AoC)](https://adventofcode.com) since 2021.

Starting from 2024, I choose to create a global library for commonly used features to ease the development. I limit myself to use only the standard library, along with two packages: `more-itertools` (I like itertools), `tqdm` and `matplotlib` for vizualisation. The package `requests` is used to automatically downloading the day's input if not present. By using the decorator introduced in the [aoc](aoc/__init__.py) package and provided a cookie saved in a `.session` file in the root directory, the day and year is automatically infered from the file path and the corresponding data is downloaded when running the decorated function. One can find a template in the `script` folder.

## Installation

To create the workspace's virtual environment using uv:
```bash
uv venv && source .venv/bin/activate && uv sync
```
If you're using your own method, please refer to the [pyproject.toml](pyproject.toml) and do not forget to install the current project in editable mode: `pip install -e .`.

The code is supposed to be run from the root directory (at least from 2024).
