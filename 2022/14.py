from utils import lmap, print_matrix
from functools import reduce
from enum import Enum

part = 2
debug = False


class Tile(Enum):
    air = 0
    rock = 1
    sand = 2


class Cave:
    def __init__(self, start_w, end_w, start_h, end_h) -> None:
        self.w = (start_w, end_w)
        self.width = end_w - start_w + 1
        self.h = (start_h, end_h)
        self.height = end_h - start_h + 1
        self.sand_generator = (500 - start_w, 0 - start_h)
        self.map = [[Tile.air for _ in range(self.width)]
                    for _ in range(self.height)]

    def draw_rock_line(self, start, end) -> None:
        if (end[0] < start[0] or end[1] < start[1]):
            start, end = end, start
        start = start[0] - self.w[0], start[1] - self.h[0]
        end = end[0] - self.w[0], end[1] - self.h[0]
        # print(start, " -> ", end)
        for i in range(start[1], end[1] + 1):
            for j in range(start[0], end[0] + 1):
                self.map[i][j] = Tile.rock

    def make_sand_flow(self) -> int:
        sand_pos = self.sand_generator
        if (self.map[sand_pos[1]][sand_pos[0]] != Tile.air):
            return 0
        while sand_pos[1] < self.height:
            if (self.map[sand_pos[1]][sand_pos[0]] == Tile.air):
                sand_pos = sand_pos[0], sand_pos[1] + 1
            elif (sand_pos[0] > 0 and self.map[sand_pos[1]][sand_pos[0] - 1] == Tile.air):
                sand_pos = sand_pos[0] - 1, sand_pos[1] + 1
            elif (sand_pos[0] + 1 < self.width and self.map[sand_pos[1]][sand_pos[0] + 1] == Tile.air):
                sand_pos = sand_pos[0] + 1, sand_pos[1] + 1
            else:  # cannot fall anymore
                if (sand_pos[0] <= 0 or sand_pos[0] + 1 >= self.width):
                    return -1
                self.map[sand_pos[1] - 1][sand_pos[0]] = Tile.sand
                return sand_pos[1] - 1
        return -1


with open("inputs/14.txt", "r") as file:
    lines_list = lmap(lambda x: lmap(lambda y: tuple(map(int, y.split(','))),
                                     x[:-1].split(" -> ")), file.readlines())

    mw, Mw, mh, Mh = 500, 500, 0, 0
    for lines in lines_list:
        for point in lines:
            mw, Mw, mh, Mh = min(mw, point[0]), max(
                Mw, point[0]), min(mh, point[1]), max(Mh, point[1])

    if (part == 2):
        mw, Mw, mh, Mh = 500 - Mh - 10, 500 + Mh + 10, 0, Mh + 2
        lines_list.append([(mw, Mh), (Mw, Mh)])

    cave = Cave(mw, Mw, mh, Mh)
    print(cave.w, cave.h, cave.width, cave.height, sep=" | ")

    # draw rock lines
    for lines in lines_list:
        if (len(lines) > 1):
            for k in range(len(lines) - 1):
                cave.draw_rock_line(lines[k], lines[k + 1])
        else:
            raise Exception("one point cannot draw a line")

    # make sand flow
    cpt = 0
    while cave.make_sand_flow() not in [0, -1]:
        cpt += 1

    # -- part 1 --
    print(f"part {part} : ", cpt + (1 if part == 2 else 0))
    if debug:
        m = [lmap(lambda x: "#" if x == Tile.rock else (
            "." if x == Tile.air else "*"), line) for line in cave.map]
        m[cave.sand_generator[1]][cave.sand_generator[0]] = "$"
        print_matrix(m)
