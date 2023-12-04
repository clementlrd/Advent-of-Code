from utils import lmap, flatten
from functools import reduce


class Tree:
    def __init__(self, h, w, size):
        self.h = h
        self.w = w
        self.size = size

    def __lt__(self, t):
        return self.size < t.size

    def __repr__(self):
        return f"({self.h},{self.w} | {self.size})"


def is_tree_visible(forest, tree):
    line, col = forest[tree.h], [x[tree.w] for x in forest]
    dirs = [line[:tree.w], line[tree.w + 1:], col[:tree.h], col[tree.h + 1:]]
    return reduce(lambda acc, d: acc or reduce(lambda acc2, t: acc2 and t < tree, d, True), dirs, False)


def get_tree_distance(tree_size, dir):
    for i, t in enumerate(dir):
        if (t.size >= tree_size):
            return i + 1
    return len(dir)


def get_scenic(forest, tree):
    line, col = forest[tree.h], [x[tree.w] for x in forest]
    dirs = [line[:tree.w][::-1], line[tree.w + 1:],
            col[:tree.h][::-1], col[tree.h + 1:]]
    # print("tree ", tree, lmap(lambda d: get_tree_distance(tree.size, d), dirs))
    return reduce(lambda acc, x: acc * x,
                  lmap(lambda d: get_tree_distance(tree.size, d), dirs))


with open("inputs/8.txt", "r") as file:
    # -- part 1 --
    forest = lmap(lambda x: lmap(lambda y: Tree(x[0], y[0], int(y[1])),
                  enumerate(x[1][:-1])), enumerate(file.readlines()))
    interior = [x[1:-1] for x in forest[1:-1]]
    visible_tree = reduce(lambda acc, t: acc +
                          is_tree_visible(forest, t), flatten(interior), 0)
    border_tree = 2 * (len(forest) + len(forest[0])) - 4
    print("visible tree : ", visible_tree + border_tree)
    # -- part 2 --
    scenic_max = max(lmap(lambda x: get_scenic(forest, x), flatten(interior)))
    print("max scenic", scenic_max)
