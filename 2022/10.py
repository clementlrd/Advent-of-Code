from utils import lmap, sum
from functools import reduce


class CPU:
    def __init__(self) -> None:
        self.x_register = [1]

    def noop(self):
        self.add_xregister()

    def addx(self, value):
        self.noop()
        self.add_xregister(value)

    def add_xregister(self, value=0):
        self.x_register.append(self.x_register[-1] + value)

    def sig_strengh(self, i):
        return i * self.x_register[i - 1]

    def is_CRT_lit(self, i, j):
        return i in range(self.x_register[j] - 1, self.x_register[j] + 2)


with open("inputs/10.txt", "r") as file:
    commands = lmap(lambda x: x[:-1].split(" "), file.readlines())
    part = 1
    cpu = CPU()
    for command in commands:
        if command[0] == "noop":
            cpu.noop()
        elif command[0] == "addx":
            cpu.addx(int(command[1]))

    print("part 1 : ", reduce(
        sum, map(lambda x: cpu.sig_strengh(x), range(20, 221, 40)), 0))

    # -- part 2 --
    for i in range(6):
        for j in range(40):
            print("#" if cpu.is_CRT_lit(j, i * 40 + j) else ".", end="")
        print()
