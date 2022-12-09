def lmap(*args, **kwargs):
    return list(map(*args, **kwargs))


def flatten(nested_list):
    flat = []
    for el in nested_list:
        try:
            flat.extend(flatten(el))
        except TypeError:
            flat.append(el)
    return flat


def crange(c):
    x, y = c
    for i in range(x):
        for j in range(y):
            yield (i, j)


def sum(acc, x):
    return acc + x


def mult(acc, x):
    return acc * x
