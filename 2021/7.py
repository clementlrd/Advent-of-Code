with open("input/7.txt") as file:
    ligne = file.readline().split(',')
    vals = list(map(int, ligne))
    m = max(vals)
    total_shift = [0] * (m + 1)
    for i in range(len(vals)):
        k = 0
        for j in range(vals[i], -1, -1):
            total_shift[j] += k
            k += 1
        k = 0
        for j in range(vals[i], len(total_shift)):
            total_shift[j] += k
            k += 1
    print("resultat 1 : ", min(total_shift))
    total_shift = [0] * (m + 1)
    for i in range(len(vals)):
        k = 0
        cost = 1
        for j in range(vals[i], -1, -1):
            total_shift[j] += k
            k += cost
            cost += 1
        k = 0
        cost = 1
        for j in range(vals[i], len(total_shift)):
            total_shift[j] += k
            k += cost
            cost += 1
    print("resultat 2 : ", min(total_shift))
