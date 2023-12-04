nbr_segment = [6, 2, 5, 5, 4, 5, 6, 3, 7, 6]
segments = ["a", "b", "c", "d", "e", "f", "g"]


""" class Digit:

    def __init__(self):
        self.segments = {}
        for segment in segments:
            self.segments[segment] = Segment(segment)

    def segment(self, val):
        return self.segments[val]


class Segment:

    def __init__(self, name):
        self.name = name
        self.wires = segments.copy()

    def unselect(self, val):
        wires = []
        for e in self.wires:
            if e != val:
                wires.append(e)
        self.wires = wires
 """

with open("input/8.txt") as file:
    lignes = file.readlines()
    input_vals = list(map(lambda x: x.split("|")[0][:-1], lignes))
    input_vals = list(map(lambda x: x.split(" "), input_vals))
    output_vals = list(map(lambda x: x.split("|")[1][1:-1], lignes))
    output_vals = list(map(lambda x: x.split(" "), output_vals))
    vals = []
    for i in range(len(lignes)):
        vals.append(input_vals[i] + output_vals[i])

    cpt = 0
    for i in range(len(output_vals)):
        for j in range(len(output_vals[0])):
            if len(output_vals[i][j]) in [2, 3, 4, 7]:
                cpt += 1
    print("résultat 1:", cpt)

    decrypted = [[-1] * 4 for _ in range(len(output_vals))]
    for i in range(len(output_vals)):
        digit = [None for _ in range(10)]
        digit[8] = set(segments)
        five_gp = []
        six_gp = []
        for j in range(len(vals[i])):
            e = len(vals[i][j])
            if e in [2, 3, 4]:
                digit[nbr_segment.index(e)] = set(vals[i][j])
            elif e == 5:
                s = set(vals[i][j])
                if s not in five_gp:
                    five_gp.append(s)
            elif e == 6:
                s = set(vals[i][j])
                if s not in six_gp:
                    six_gp.append(s)
        # find up
        up = ""
        t = digit[7] - digit[1]
        if len(t) == 1:
            up = t.pop()
        else:
            raise Exception("pb up")

        # find down & digit 9
        down = ""
        for d in six_gp:
            t = (d - digit[4]) - set(up)
            if len(t) == 1:
                down = t.pop()
                digit[9] = six_gp.pop(six_gp.index(d))

        # find middle & digit 3
        middle = ""
        for d in five_gp:
            t = (d - digit[7]) - set(down)
            if len(t) == 1:
                middle = t.pop()
                digit[3] = five_gp.pop(five_gp.index(d))

        # find digit 0
        digit[0] = six_gp.pop(six_gp.index(digit[8] - set(middle)))

        # find digit 6
        if len(six_gp) == 1:
            digit[6] = six_gp.pop()
        else:
            raise Exception("pb digit 6")

        # find digit 5
        for d in five_gp:
            t = ((d - digit[4]) - set(up)) - set(down)
            if not len(t):
                digit[5] = five_gp.pop(five_gp.index(d))

        # find digit 2
        if len(five_gp) == 1:
            digit[2] = five_gp.pop()
        else:
            raise Exception("pb digit 2")

        # decrypte
        for j in range(len(output_vals[i])):
            decrypted[i][j] = digit.index(set(output_vals[i][j]))

    result = 0
    print(decrypted)
    for i in range(len(decrypted)):
        print(result)
        for j in range(len(decrypted[i])):
            result += decrypted[i][j] * (10**(3 - j))
    print("resultat 2 :", result)
