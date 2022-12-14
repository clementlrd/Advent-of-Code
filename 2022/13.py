from utils import lmap, sum, find
from functools import reduce

part = 1


def is_list(el):
    try:
        len(el)
        return True
    except TypeError:
        return False


def compare(paire):
    p1, p2 = paire
    if (not is_list(p1) and not is_list(p2)):
        return p2 - p1
    if(not is_list(p1)):
        p1 = [p1]
    elif(not is_list(p2)):
        p2 = [p2]
    for i in range(min(len(p1), len(p2))):
        c = compare((p1[i], p2[i]))
        if (c < 0):
            return -1
        elif (c > 0):
            return 1
    return 0 if len(p1) == len(p2) else len(p2) - len(p1)


class Packet:
    def __init__(self, list):
        self.list = list

    def __lt__(self, p) -> bool:
        return compare((self.list, p.list)) >= 0

    def __eq__(self, p) -> bool:
        return compare((self.list, p.list)) == 0

    def __repr__(self) -> str:
        return self.list.__repr__()


with open("inputs/13.txt", "r") as file:
    values = lmap(lambda x: x[:-1], file.readlines())
    paires = []
    for i in range(0, len(values), 3):
        paires.append((eval(values[i]), eval(values[i + 1])))

    index_sum = reduce(sum, lmap(lambda x: (
        x[0] + 1) if compare(x[1]) >= 0 else 0, enumerate(paires)))

    print("partie 1 :", index_sum)

    p1, p2 = Packet([[2]]), Packet([[6]])
    packets_list = [p1, p2]
    for paire in paires:
        packets_list.append(Packet(paire[0]))
        packets_list.append(Packet(paire[1]))

    packets_list.sort()
    id1 = find(packets_list, lambda x: x == p1)[0]
    id2 = find(packets_list, lambda x: x == p2)[0]

    print("partie 2 :", (id1 + 1) * (id2 + 1))
