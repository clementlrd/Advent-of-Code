from copy import deepcopy


def add(l1, l2):
    return [deepcopy(l1), deepcopy(l2)]


def reduce(li):
    need_reduction = True
    has_exploded = False
    has_been_splited = False

    while(need_reduction):
        # print("\n-----")
        has_exploded = explode(li)
        if has_exploded and False:
            print("explode :")
            print(li)
        if not has_exploded:
            has_been_splited = split(li)
            if has_been_splited and False:
                print("split :")
                print(li)
        need_reduction = has_exploded or has_been_splited

    return li


def explode(li):
    has_exploded = [False]

    def dive(t, depth, b):
        if depth == 4 and not b[0]:
            # print("here")
            g, d = t
            b[0] = True
            return True, False, g, False, d

        if (type(t) != list):
            return False, True, None, True, None

        # left branch
        if (type(t[0]) == list):
            processing, usedg, g, usedd, d = dive(t[0], depth + 1, b)
            if processing:
                # reset pair to 0
                if depth == 3:
                    t[0] = 0
                if not usedd:
                    # print("d :", d)
                    # dive into right branch
                    if (type(t[1]) == int):
                        t[1] += d
                    else:
                        a = t[1]
                        while(type(a[0]) != int):
                            a = a[0]
                        a[0] += d
                return not usedg, usedg, g, True, None

        # right branch
        if (type(t[1]) == list):
            processing, usedg, g, usedd, d = dive(t[1], depth + 1, b)
            if processing:
                # reset pair to 0
                if depth == 3:
                    t[1] = 0
                if not usedg:
                    # print("g :", g)
                    # dive into left branch
                    if (type(t[0]) == int):
                        t[0] += g
                    else:
                        a = t[0]
                        while(type(a[1]) != int):
                            a = a[1]
                        a[1] += g
                return not usedd, True, None, usedd, d

        return False, True, None, True, None

    dive(li, 0, has_exploded)
    return has_exploded[0]


def split(li):
    has_been_splited = [False]

    def dive(t, p, i, b):
        if type(t) == list:
            dive(t[0], t, 0, b)
            dive(t[1], t, 1, b)
        elif not b[0] and t >= 10:
            b[0] = True
            p[i] = [t // 2, (t + 1) // 2]
        else:
            return

    dive(li[0], li, 0, has_been_splited)
    dive(li[1], li, 1, has_been_splited)
    return has_been_splited[0]


def magnitude(t):
    if type(t) == list:
        return 3 * magnitude(t[0]) + 2 * magnitude(t[1])
    else:
        return t


with open("input/18.txt") as file:
    lignes = list(map(lambda x: x[:-1], file.readlines()))
    vals = []
    for i in range(len(lignes)):
        vals.append(eval(lignes[i]))
    val = vals[0]
    for i in range(1, len(vals)):
        val = add(val, vals[i])
        reduce(val)
    print("résultat 1 : ", magnitude(val))
    print(val)

    mag = 0
    for i in range(len(vals)):
        for j in range(len(vals)):
            mag = max(mag, magnitude(reduce(add(vals[i], vals[j]))))
    print("résultat 2 :", mag)
