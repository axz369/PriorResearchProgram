from .countHints import countHints


def printBoard(board):
    size = len(board)
    print(f"ヒント数: {countHints(board)}")
    print("+" + "---+" * size)
    for i, row in enumerate(board):
        print("|", end="")
        for j, val in enumerate(row):
            print(f" {val if val != 0 and val != '0' else ' '} ", end="|")
        print()
        if i < size - 1:
            print("+" + "---+" * size)
    print("+" + "---+" * size)
