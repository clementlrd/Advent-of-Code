from functools import reduce

# A : Rock (1)
# B : paper (2)
# C : cisoors (3)

# loose : 0
# draw : 3
# win : 6

# i -> A,B,C
# j -> X,Y,Z
s = [[4, 8, 3], [1, 5, 9], [7, 2, 6]]


def getScore(a, b):
    return s[a][b]


def getAction(a, b):
    return a if b == 1 else (a + 1) % 3 if b == 2 else (a - 1) % 3


with open("inputs/2.txt", "r") as file:
    # part 1
    vals = list(
        map(lambda x: (ord(x[0]) - ord('A'), ord(x[2]) - ord('X')), file.readlines()))
    score = reduce(lambda sc, rd: sc + getScore(*rd), vals, 0)
    print(score)
    # part 2
    score = reduce(lambda sc, rd: sc +
                   getScore(rd[0], getAction(*rd)), vals, 0)
    print(score)
