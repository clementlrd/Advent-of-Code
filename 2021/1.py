with open("input/1.txt", "r") as file:
    cpt = 0
    cpt2 = 0
    lignes = file.readlines()
    vals = list(map(lambda x: int(x[:-1]), lignes))
    for i in range(1, len(vals)):
        if(vals[i] - vals[i - 1] > 0):
            cpt += 1
    print("result 1 : " + str(cpt))
    vals2 = []
    for i in range(len(vals) - 2):
        vals2.append(vals[i] + vals[i + 1] + vals[i + 2])
    for i in range(len(vals2)):
        if(vals2[i] - vals2[i - 1] > 0):
            cpt2 += 1
    print("result 2 : " + str(cpt2))
