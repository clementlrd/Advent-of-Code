import numpy as np
from Utils import trange
import re


class Rule:

    def __init__(self, command, tr=50):
        self.command = True if command[1] == 'n' else False
        a = command[3:].split(",")

        def shift(pos):
            i = {"x": 0, "y": 1, "z": 2}
            return list(map(lambda x: int(x) + tr, re.split(f"{pos}=|\.\.", a[i[pos]])[1:]))
        self.x = shift("x")
        self.y = shift("y")
        self.z = shift("z")


2

with open("input/22.txt") as file:
    lignes = list(map(lambda x: x[:-1], file.readlines()))
    rules = []
    for ligne in lignes:
        rules.append(Rule(ligne))
    core = np.zeros((101, 101, 101), dtype=bool)
    for rule in rules:
        core[rule.x[0]:(rule.x[1] + 1),
             rule.y[0]:(rule.y[1] + 1),
             rule.z[0]:(rule.z[1] + 1)
             ] = rule.command
    cpt = 0
    for x in trange(core.shape):
        if core[x]:
            cpt += 1
    print("résultat 1 :", cpt)

    """
    représentation creuse des sommets allumés
    projection des sommets sur chaque axe pour trouver une intersection
    Le cas écheant, si même commande (on), rajouter le cuboid tel quelle
    sinon (off) séparer le cuboid restant en autant de cuboids que nécessaire
    ? ségmenter d'abord /x puis /y puis /z ?
    """
