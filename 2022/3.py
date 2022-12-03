from functools import reduce


def getPriority(c):
    return ord(c) - ord('A') + 27 if ord(c) < ord('a') else ord(c) - ord('a') + 1


with open("inputs/3.txt", "r") as file:
    # part 1
    vals = list(map(lambda x: x[:-1], file.readlines()))
    total = 0
    for rucksack in vals:
        size = len(rucksack)
        for i in range(size // 2, size):
            if (rucksack[i] in rucksack[: size // 2]):
                total += getPriority(rucksack[i])
                break
    print(total)
    total = 0
    for k in range(0, len(vals), 3):
        rs = vals[k][:] + vals[k + 1][:] + vals[k + 2][:]
        for r in rs:
            if(r in vals[k][:] and r in vals[k + 1][:] and r in vals[k + 2][:]):
                print(k, " found ", r)
                total += getPriority(r)
                break
    print(total)
