DAYS_1 = 80
DAYS_2 = 256
BASE = 6
BASE_NEW = 8

# 256/8 = 32

with open("input/6.txt") as file:
    line = file.readline().split(',')
    vals = list(map(int, line))
    for _ in range(DAYS_1):
        new_vals = 0
        for i in range(len(vals)):
            if (vals[i] == 0):
                new_vals += 1
                vals[i] = BASE
            else:
                vals[i] -= 1
        vals.extend([BASE_NEW] * new_vals)
    print("Au jour", DAYS_1, "il ya", len(vals), "lanternfish")

    # optimisation:
    vals = list(map(int, line))
    counter = [0] * 9
    for val in vals:
        counter[val] += 1
    for _ in range(DAYS_2):
        new_counter = [0] * 9
        new_counter[6] = counter[0]
        new_counter[8] = counter[0]
        for i in range(1, 9):
            new_counter[i - 1] += counter[i]
        counter = new_counter
    print("Au jour", DAYS_2, "il y a", sum(counter), "lanternfish")
