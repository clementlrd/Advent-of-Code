from utils import lmap
from functools import reduce

MAX_DIR_SIZE = 100000
MAX_FREE_SPACE = 30000000
DISK_SIZE = 70000000


class File:
    def __init__(self, name, size, parent=None):
        self.name = name
        self.size = size
        self.parent = parent


class Dir:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.subdirs = []
        self.files = []

    def addSubDir(self, subdir):
        self.subdirs.append(subdir)

    def addFile(self, file):
        self.files.append(file)


def flattenDir(dir):
    return reduce(lambda acc, d: acc + flattenDir(d), dir.subdirs, [dir])


def getDir(dir, name):
    if (name == ".."):
        return dir.parent
    for x in dir.subdirs:
        if x.name == name:
            return x


def printDir(dir, pad=0):
    if not pad:
        print(".")
    for file in dir.files:
        print(" " * pad + f"├-- {file.name} ({file.size})")
    for subdir in dir.subdirs:
        subdir.size = getSizeDir(subdir)
        print(" " * pad + f"├-- {subdir.name}/ ({subdir.size})")
        printDir(subdir, pad + 2)


def find_dirs(root, heavy=False):
    dirs = []
    for subdir in root.subdirs:
        subdir_size = getSizeDir(subdir)
        if not heavy and subdir_size <= MAX_DIR_SIZE:
            dirs.append(subdir)
        dirs.extend(find_dirs(subdir, heavy=heavy))
    return dirs


def getSizeDir(dir):
    size = reduce(lambda acc, f: acc + f.size, dir.files, 0)
    for subdir in dir.subdirs:
        size += getSizeDir(subdir)
    return size


with open("inputs/7.txt", "r") as file:
    # -- part 1 --
    cout = lmap(lambda x: x[:-1], file.readlines()[1:])
    tree = Dir("/")
    currentDir = tree
    for i, line in enumerate(cout):
        words = line.split(" ")
        print(words)
        # command
        if (words[0] == "$"):
            if (words[1] == "cd"):
                currentDir = getDir(currentDir, words[2])
            elif (words[1] == "ls"):
                pass
        # in ls mode
        else:
            # file
            if words[0].isdigit():
                currentDir.addFile(File(words[1], int(words[0])))
            # subdir
            elif words[0] == "dir":
                currentDir.addSubDir(Dir(words[1], currentDir))
            else:
                raise Exception(f"command not found in line {i}:", line, words)
    printDir(tree)
    not_heavy_dirs = find_dirs(tree, heavy=False)
    print(f"total size of heavy dirs (<= {MAX_DIR_SIZE}) : ", end="")
    print(reduce(lambda acc, d: acc + getSizeDir(d), not_heavy_dirs, 0))

    # -- part 2 --
    size_to_free = MAX_FREE_SPACE - (DISK_SIZE - getSizeDir(tree))
    print("Need to free ", size_to_free)
    for dir in sorted(flattenDir(tree), key=lambda d: getSizeDir(d)):
        if getSizeDir(dir) >= size_to_free:
            print(
                f"lowest folder to delete to get desired space : {dir.name} ({getSizeDir(dir)})")
            break
