def max_mat(t):  # max of a matrix
    m = t[0][0]
    for i in range(len(t)):
        for j in range(len(t[0])):
            if (t[i][j] > m):
                m = t[i][j]
    return m


def i_max(t):  # return index of max for a list
    m = 0
    im = 0
    for i in range(len(t)):
        if t[i] > m:
            m = t[i]
            im = i
    return im


def print_grid(t, n=None, m=None):
    if n is None:
        n = len(t)
    if m is None:
        m = len(t[0])
    for i in range(n):
        for j in range(m):
            print(t[i][j], sep=' ')
        print()


# function to return key for any value
def get_key(dico, val):
    for key, value in dico.items():
        if val == value:
            return key

    raise Exception("key doesn't exist")
