def cpt(vals):
    el = {}
    for e in vals:
        if e not in el.keys():
            el[e] = 0
        else:
            el[e] += 1
    s = list(el.values())
    print("résultat 1 :", max(s) - min(s))


with open("input/14.txt") as file:
    lignes = list(map(lambda x: x[:-1], file.readlines()))
    vals = list(lignes[0])
    rules = {}
    for i in range(2, len(lignes)):
        s = lignes[i].split(' -> ')
        rules[s[0]] = s[1]

    for _ in range(10):
        i = 0
        while i + 1 < len(vals):
            ins = rules[vals[i] + vals[i + 1]]
            vals = vals[:i + 1] + [ins] + vals[i + 1:]
            i += 2

    cpt(vals)

    polymer = {}
    for i in range(len(lignes[0]) - 1):
        if lignes[0][i:i + 2] not in polymer.keys():
            polymer[lignes[0][i:i + 2]] = 1
        else:
            polymer[lignes[0][i:i + 2]] += 1

    for _ in range(40):
        new_polymer = {}
        for e in polymer.keys():
            a = e[0] + rules[e]
            b = rules[e] + e[1]
            if a not in new_polymer.keys():
                new_polymer[a] = polymer[e]
            else:
                new_polymer[a] += polymer[e]
            if b not in new_polymer.keys():
                new_polymer[b] = polymer[e]
            else:
                new_polymer[b] += polymer[e]
        polymer = new_polymer

    letters = {}
    for e in polymer.keys():
        if e[0] not in letters.keys():
            letters[e[0]] = polymer[e]
        else:
            letters[e[0]] += polymer[e]
        if e[1] not in letters.keys():
            letters[e[1]] = polymer[e]
        else:
            letters[e[1]] += polymer[e]
    s = list(letters.values())
    print("résultat 2 :", (max(s) - min(s)) // 2)
