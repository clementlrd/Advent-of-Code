from helpers import get_key

ERROR_VALUES = {')': 3, ']': 57, '}': 1197, '>': 25137}
INCOMPLETE_VALUES = {')': 1, ']': 2, '}': 3, '>': 4}
BRACKETS_OPEN = {'(': ')', '[': ']', '{': '}', '<': '>'}


class Bracket:
    def __init__(self, bracket):
        self.close = bracket
        self.open = get_key(BRACKETS_OPEN, self.close)
        self.error_value = ERROR_VALUES[self.close]
        self.incomplete_value = INCOMPLETE_VALUES[self.close]

    def __repr__(self):
        return self.open

    def __eq__(self, val):
        if (type(val) == str):
            return val in [self.open, self.close]
        else:
            return self.close == val.close


def add(score, bracket):
    return score * 5 + bracket.incomplete_value


with open("input/10.txt") as file:
    lignes = list(map(lambda x: x[:-1], file.readlines()))
    incomplete = []
    error_score = 0
    for i in range(len(lignes)):
        pile = []
        error = False
        for j in range(len(lignes[i])):
            b = lignes[i][j]
            if b in BRACKETS_OPEN.keys():
                pile.append(Bracket(BRACKETS_OPEN[b]))
            elif not len(pile) or pile[-1] != b:
                error_score += Bracket(b).error_value
                error = True
                break
            else:
                pile.pop()
        if not error:
            incomplete.append(lignes[i])
    print("résultat 1 :", error_score)

    incomplete_score = []
    print(incomplete[0])
    for i in range(len(incomplete)):
        pile = []
        for j in range(len(incomplete[i])):
            b = incomplete[i][j]
            if b in BRACKETS_OPEN.keys():
                pile.append(Bracket(BRACKETS_OPEN[b]))
            elif len(pile) and pile[-1] == b:
                pile.pop()
        score = 0
        for i in range(len(pile) - 1, -1, -1):
            score = add(score, pile[i])
        incomplete_score.append(score)
    incomplete_score.sort()
    print("résultat 2 :", incomplete_score[int(
        len(incomplete_score) / 2)])
