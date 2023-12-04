from copy import deepcopy


def validation_board(board):
    for i in range(5):
        b1 = board[i][0] and board[i][1] and board[i][2] and board[i][3] and board[i][4]
        b2 = board[0][i] and board[1][i] and board[2][i] and board[3][i] and board[4][i]
        if (b1) or (b2):
            return True
    return False


def validation(boards):
    for i in range(len(boards)):
        if validation_board(boards[i][1]):
            return (True, i)
    return (False, -1)


def play_board(board, val):
    for i in range(5):
        for j in range(5):
            if board[0][i][j] == val:
                board[1][i][j] = True


def play(boards, val):
    for i in range(len(boards)):
        play_board(boards[i], val)


def uncalled_number_sum(board):
    s = 0
    for i in range(5):
        for j in range(5):
            if not board[1][i][j]:
                s += board[0][i][j]
    return s


def validation_delete(boards):
    new_boards = []
    for board in boards:
        if not validation_board(board[1]):
            new_boards.append(board)
    return new_boards


def reset(file):
    lignes = file.readlines()
    numbers = list(map(lambda x: int(x), lignes[0].split(',')))
    boards = []
    # creating boards from file
    for i in range(2, len(lignes), 6):
        board = list(map(lambda x: x.split(' '), lignes[i:i + 5]))
        board = list(map(lambda x: list(filter(lambda y: y != "", x)), board))
        board = list(map(lambda x: list(map(lambda y: int(y), x)), board))
        boards.append(board)
    # adding validation board to each board
    # template
    v_board = [[False] * 5 for _ in range(5)]
    boards = list(map(lambda x: (x, deepcopy(v_board)), boards))
    return boards, numbers


with open("input/4.txt") as file:
    boards, numbers = reset(file)
    # playing the game
    n = len(boards)
    finished = False
    victory_board = -1
    i = 0
    while not finished and i < n:
        play(boards, numbers[i])
        finished, victory_board = validation(boards)
        i += 1
    print("victory board :", victory_board)
    print("after", i, "round")
    for k in range(5):
        print(boards[victory_board][0][k])
        print(boards[victory_board][1][k])
    print("result 1 : ", uncalled_number_sum(
        boards[victory_board]) * numbers[i - 1])

    # doing the same but finding out the last wining board
    boards.pop(victory_board)
    while len(boards) > 1 and i < n:
        play(boards, numbers[i])
        boards = validation_delete(boards)
        i += 1
    finished = False
    while not finished and i < n:
        play(boards, numbers[i])
        finished, _ = validation(boards)
        i += 1
    print("after", i, "round over", len(numbers))
    print("last victory board :")
    for k in range(5):
        print(boards[0][0][k])
        print(boards[0][1][k])
    print("result 2 : ", uncalled_number_sum(
        boards[0]) * numbers[i - 1])
