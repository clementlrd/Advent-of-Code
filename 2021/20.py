from copy import deepcopy
from Utils import crange
from scipy.ndimage import convolve
import numpy as np


kernel = np.array([[256, 128, 64],
                   [32, 16, 8],
                   [4, 2, 1]])[::-1, ::-1]


def print_matrix(mat: np.ndarray):
    for i in range(len(mat)):
        print("".join(list(map(lambda x: "#" if x else ".", mat[i]))))


def enhance_picture(enhancement, picture: np.ndarray, k):
    new_picture = np.pad(picture, ((3, 3), (3, 3)),
                         mode="constant", constant_values=k)
    # print(convolve(new_picture[9:12, 9:12], kernel, mode="constant", cval=0))
    new_picture = convolve(new_picture, kernel, mode="constant", cval=k)
    for i, j in crange(new_picture.shape):
        new_picture[i, j] = enhancement[new_picture[i, j]]
    return new_picture


with open("input/20.txt") as file:
    lignes = list(map(lambda x: x[:-1], file.readlines()))
    enhancement = list(lignes[0])
    for i in range(len(enhancement)):
        enhancement[i] = 1 if enhancement[i] == "#" else 0
    picture = np.zeros((len(lignes) - 2, len(lignes[2])), dtype=int)
    for i, j in crange(picture.shape):
        picture[i, j] = 1 if lignes[2 + i][j] == "#" else 0

    for i in range(50):
        # print_matrix(picture)
        new_picture = enhance_picture(enhancement, picture, i % 2)
        picture = new_picture
    # print_matrix(picture)
    print("résultat :", picture.sum())
