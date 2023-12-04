from functools import reduce


def collapse_calories(collapsed_list, elem):
    if (elem == ""):
        collapsed_list.append(0)
    else:
        collapsed_list[-1] += elem
    return collapsed_list


with open("inputs/1.txt", "r") as file:
    vals = list(map(lambda x: "" if x[:-1] ==
                "" else int(x[:-1]), file.readlines()))
    cals = reduce(collapse_calories, vals, [0])
    m1 = max(cals)
    cals.pop(cals.index(m1))
    m2 = max(cals)
    cals.pop(cals.index(m2))
    m3 = max(cals)
    cals.pop(cals.index(m3))
    print(m1 + m2 + m3)
    # for i in range(1, len(lignes)):
