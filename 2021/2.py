with open("input/2.txt", "r") as file:
    lignes = file.readlines()
    vals = list(map(lambda x: int(x[-2]), lignes))
    commands = list(map(lambda x: x[:-3], lignes))
    horizontal = 0
    depth = 0
    for i in range(len(lignes)):
        if (commands[i] == "forward"):
            horizontal += vals[i]
        elif (commands[i] == "down"):
            depth += vals[i]
        elif (commands[i] == "up"):
            depth -= vals[i]
        else:
            print("unknown command")
            break
    print("horizontal : " + str(horizontal))
    print("depth : " + str(depth))
    print("resultat 1 : " + str(depth * horizontal))

    aim = 0
    horizontal = 0
    depth = 0
    for i in range(len(lignes)):
        if (commands[i] == "forward"):
            horizontal += vals[i]
            depth += vals[i] * aim
        elif (commands[i] == "down"):
            aim += vals[i]
        elif (commands[i] == "up"):
            aim -= vals[i]
        else:
            print("unknown command")
            break
    print("horizontal : " + str(horizontal))
    print("depth : " + str(depth))
    print("aim : " + str(aim))
    print("resultat 1 : " + str(depth * horizontal))
