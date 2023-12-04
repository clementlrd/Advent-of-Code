TEST = [
    "00100",
    "11110",
    "10110",
    "10111",
    "10101",
    "01111",
    "00111",
    "11100",
    "10000",
    "11001",
    "00010",
    "01010"
]


def oneCpt(i, t):
    cpt = 0
    for j in range(len(t)):
        if t[j][i] == "1":
            cpt += 1
    return cpt


def bitCritera(isMostCommonBit: bool, i, t):
    n = len(t)
    for j in range(len(t)):
        cpt = oneCpt(i, t)
        if isMostCommonBit:
            return list(filter(lambda x: x[i] == ("1" if n - cpt <= cpt else "0"), t))
        else:
            return list(filter(lambda x: x[i] == ("0" if n - cpt <= cpt else "1"), t))


def bit_to_number(bits: str):
    res = 0
    for i in range(len(bits)):
        p = pow(2, n - 1 - i)
        res += p * (1 if bits[i] == "1" else 0)
    return res


with open("input/3.txt") as file:
    lignes = list(map(lambda x: x[:-1], file.readlines()))
    gamma_rate = 0
    epsilon_rate = 0
    n = len(lignes[0])
    for i in range(n):
        cpt = oneCpt(i, lignes)
        b = len(lignes) - cpt < cpt
        p = pow(2, n - 1 - i)
        gamma_rate += p * (1 if b else 0)
        epsilon_rate += p * (1 if not b else 0)
    print("gamma rate : ", gamma_rate)
    print("epsilon rate : ", epsilon_rate)
    print("resultat 1 : ", epsilon_rate * gamma_rate)

    o2_gen_rating = lignes[:]
    co2_scrub_rating = lignes[:]
    n = len(lignes[0])
    i = 0
    while i < n and len(o2_gen_rating) != 1:
        # print(o2_gen_rating)
        o2_gen_rating = bitCritera(True, i, o2_gen_rating)
        i += 1
    print("len oxygen generator rating : ", len(o2_gen_rating))
    print(o2_gen_rating)
    i = 0
    while i < n and len(co2_scrub_rating) != 1:
        co2_scrub_rating = bitCritera(False, i, co2_scrub_rating)
        i += 1
    print("len CO2 scrubber rating : ", len(co2_scrub_rating))
    print(co2_scrub_rating)
    print("resultat 2 : ", bit_to_number(
        o2_gen_rating[0]) * bit_to_number(co2_scrub_rating[0]))
