from utils import lmap
from functools import reduce

dirs = {
    "R": (0, 1),
    "L": (0, -1),
    "U": (-1, 0),
    "D": (1, 0),
}


class Rope:
    def __init__(self, length):
        self.head = Head()
        self.body = [Body() for _ in range(length)]
        self.pos_tail_visited = set([(0, 0)])

    def mouve(self, dir, nbr):
        for _ in range(nbr):
            self.head.mouve(dir, self.body[0])
            for i in range(len(self.body) - 1):
                self.body[i].mouve(self.body[i + 1])
            self.body[-1].mouve()
            self.pos_tail_visited.add((self.body[-1].h, self.body[-1].w))

    def __repr__(self):
        return self.head.__repr__() + ", " + self.body.__repr__()


class Head:
    def __init__(self, h=0, w=0):
        self.h = h
        self.w = w

    def mouve(self, dir, next=None):
        dir_h, dir_w = dir
        self.h += dir_h
        self.w += dir_w
        if (next):
            next.rel_h -= dir_h
            next.rel_w -= dir_w

    def __repr__(self):
        return f"head : ({self.h}, {self.w})"


class Body:
    def __init__(self, h=0, w=0):
        self.rel_h = 0
        self.rel_w = 0
        self.h = h
        self.w = w

    def mouve(self, next=None):
        rel = [self.rel_h, self.rel_w]
        d = abs(self.rel_h) + abs(self.rel_w)
        if(d == 0 or d == 1):  # start or near
            return
        elif (d == 2):
            if (self.rel_h == self.rel_w):  # in diag
                return
            else:
                if (not self.rel_h):
                    self.rel_w //= abs(self.rel_w)
                else:
                    self.rel_h //= abs(self.rel_h)
        elif (d == 3):
            if(abs(self.rel_h) == 1):
                self.rel_h = 0
                self.rel_w //= abs(self.rel_w)
            else:
                self.rel_w = 0
                self.rel_h //= abs(self.rel_h)
        elif(d == 4):
            self.rel_h //= abs(self.rel_h)
            self.rel_w //= abs(self.rel_w)
        else:
            raise Exception("error, distance explode")

        pos = [self.h, self.w]
        self.h -= rel[0] - self.rel_h
        self.w -= rel[1] - self.rel_w
        if (next):
            diff = [self.h - pos[0], self.w - pos[1]]
            next.rel_h -= diff[0]
            next.rel_w -= diff[1]

    def __repr__(self):
        return f"body : ({self.h} ({self.rel_h}), {self.w} ({self.rel_w}))"


def mouve_rope(command):
    dir, nbr = command
    rope.mouve(dirs[dir], int(nbr))


with open("inputs/9.txt", "r") as file:
    commands = lmap(lambda x: x[:-1].split(" "), file.readlines())
    part = 2
    rope = Rope(1 if part == 1 else 9)
    reduce(lambda _, c: mouve_rope(c), commands, None)
    print(f"part {part} :", len(rope.pos_tail_visited))
