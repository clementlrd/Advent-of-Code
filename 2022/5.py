from functools import reduce
from utils import lmap
from collections import deque

# move #1 from #2 to #3

part = 2


def print_stacks():
    print("----")
    for i in range(len(stacks)):
        print(stacks[i])
    print("----")


def make_action(stacks, acts):
    act_move, act_from, act_to = acts
    for i in range(act_move):
        stacks[act_to - 1].append(stacks[act_from - 1].pop())


def make_action_keep_order(stacks, acts):
    act_move, act_from, act_to = acts
    crates = []
    for i in range(act_move):
        crates.append(stacks[act_from - 1].pop())
    crates = crates[::-1]
    for i in range(len(crates)):
        stacks[act_to - 1].append(crates[i])


with open("inputs/5-2.txt", "r") as file:
    # -- part 1 --
    lines = file.readlines()
    acts_vals = lmap(lambda x: lmap(lambda y: int(
        y), x[:-1].split(" ")), lines[10:])
    # create stacks
    stacks_vals = lmap(lambda x: list(x[:-1]), lines[:8])
    stacks_vals = [[stacks_vals[i][k]
                    for i in range(len(stacks_vals))] for k in range(9)]
    # fill deque
    stacks = [deque(filter(lambda x: x != ' ', stacks_vals[i][::-1]))
              for i in range(len(stacks_vals))]
    # make actions
    for i in range(len(acts_vals)):
        if (part == 1):
            make_action(stacks, acts_vals[i])
        elif (part == 2):
            make_action_keep_order(stacks, acts_vals[i])
    print_stacks()
    # print final head
    stacks_head = []
    for i in range(len(stacks)):
        stacks_head.append(stacks[i].pop() if (stacks[i]) else " ")
    print("".join(stacks_head))
