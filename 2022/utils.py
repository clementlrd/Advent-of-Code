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


def print_matrix(mat):
    for i in range(len(mat)):
        print(mat[i])


def find(list, fn):
    for i, x in enumerate(list):
        if fn(x):
            return i, x
    return -1, None


def crange(c):
    x, y = c
    for i in range(x):
        for j in range(y):
            yield (i, j)


def neighbourhood(x, mat_size, size=4):
    n, m = mat_size
    i, j = x
    neighbours = []
    if size == 4:
        neighbours = [(max(i - 1, 0), j), (min(i + 1, n - 1), j),
                      (i, max(j - 1, 0)), (i, min(j + 1, m - 1))]
    for v in neighbours:
        yield v


def sum(acc, x):
    return acc + x


def mult(acc, x):
    return acc * x


def to_int(x):
    return int(x)
