from utils import lmap, print_matrix
from functools import reduce
from enum import Enum

part = 2
debug = False


with open("inputs/15.txt", "r") as file:
    lines_list = lmap(lambda x: lmap(lambda y: tuple(map(int, y.split(','))),
                                     x[:-1].split(" -> ")), file.readlines())
