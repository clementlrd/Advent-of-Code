with open("inputs/6.txt", "r") as file:
    # -- part 1 --
    char = 14
    value = file.readlines()[0][:-1]
    for i in range(char, len(value) - 1):
        if len(set(value[i - char:i])) == char:
            raise Exception("partie 2", i)
