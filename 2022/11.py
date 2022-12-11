from utils import lmap, sum, mult, to_int
from functools import reduce

part = 1


class Monkey:
    def __init__(self):
        self.bag = []
        self.operation = None
        self.divisible_test = 1
        self.send_to = None
        self.inspect = 0

    def set_bag(self, bag):
        self.bag = lmap(to_int, bag)

    def set_operator(self, op, nbr):
        nbr = nbr if nbr == "old" else int(nbr)
        self.operation = (sum, nbr) if (op == "+") else (mult, nbr)

    def set_divisible_test(self, nbr):
        self.divisible_test = nbr

    def set_senders(self, senders):
        self.send_to = senders

    def pop(self):
        self.inspect += 1
        item = self.bag.pop(0)
        new_item = self.operation[0](
            item, item if self.operation[1] == "old" else self.operation[1])
        if (part == 1):
            new_item //= 3
        return (self.send_to[1 if(new_item % self.divisible_test) else 0], new_item)

    def empty(self, monkeys):
        while len(self.bag):
            send, new_item = self.pop()
            monkeys[send].bag.append(new_item)

    def __repr__(self):
        return f"Monkey\n{self.bag}\n{self.operation}\n{self.divisible_test}, {self.send_to}\n"


with open("inputs/11.txt", "r") as file:
    lignes = lmap(lambda x: x[:-1].split(" "), file.readlines())
    # init monkeys
    monkeys = []
    cpt = 0
    while cpt < len(lignes):
        if (lignes[cpt][0] == "Monkey"):
            monkey = Monkey()
            monkey.set_bag(
                lmap(lambda x: x[:-1] if x[-1] == ',' else x, lignes[cpt + 1][4:]))
            monkey.set_operator(*lignes[cpt + 2][-2:])
            monkey.set_divisible_test(int(lignes[cpt + 3][-1]))
            monkey.set_senders((
                int(lignes[cpt + 4][-1]), int(lignes[cpt + 5][-1])))
            monkeys.append(monkey)
            cpt += 6
        else:
            cpt += 1
    for i in range(20 if part == 1 else 1000):
        for monkey in monkeys:
            monkey.empty(monkeys)
    inspection = sorted(lmap(lambda x: x.inspect, monkeys))
    print(f"partie {part} : ", inspection[-1] * inspection[-2])
