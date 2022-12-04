from functools import reduce
from utils import lmap


def is_included(paires):
    paire1, paire2 = paires
    if (paire2[0] == paire1[0] or paire2[1] == paire1[1]):
        return True
    else:
        return paire2[1] < paire1[1] if paire1[0] < paire2[0] else paire2[1] > paire1[1]


def is_overlaping(paires):
    paire1, paire2 = paires
    if (paire2[0] == paire1[0] or paire2[1] == paire1[1] or paire1[0] == paire2[1] or paire1[1] == paire2[0]):
        return True
    else:
        return paire1[1] > paire2[0] if paire1[0] < paire2[0] else paire2[1] > paire1[0]


with open("inputs/4.txt", "r") as file:
    # part 1
    vals = lmap(lambda x: lmap(lambda y: lmap(lambda z: int(z), y.split("-")),
                x[:-1].split(",")), file.readlines())
    total = reduce(lambda acc, x: acc + is_included(x), vals, 0)
    print(total)
    total = reduce(lambda acc, x: acc + is_overlaping(x), vals, 0)
    print(total)
