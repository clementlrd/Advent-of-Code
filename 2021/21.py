START = [10, 1]  # from 1 to 10

score = [0, 0]
pos = START.copy()
dice = 1
i = 0
while score[(i + 1) % 2] < 1000:
    val = dice % 101 + dice // 101
    while val > 100:
        val = val % 101 + val // 101
    a = pos[i % 2] + (3 * val + 3)
    pos[i % 2] = a % 11 + a // 11
    while pos[i % 2] > 10:
        pos[i % 2] = pos[i % 2] % 11 + pos[i % 2] // 11
    score[i % 2] += pos[i % 2]
    dice += 3
    i += 1
# loosing player
print("résultat 1 :", score[i % 2] * (dice - 1))
