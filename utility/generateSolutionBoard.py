import random
from .canBePlaced import canBePlaced

def generateSolutionBoard(board, max_number, current_position=0):
    if current_position == max_number * max_number:
        return True

    row, col = current_position // max_number, current_position % max_number
    
    if board[row][col] != 0:
        return generateSolutionBoard(board, max_number, current_position + 1)
    
    numbers = list(range(1, max_number + 1))
    random.shuffle(numbers)
    
    for num in numbers:
        if canBePlaced(board, max_number, current_position, num):
            board[row][col] = num
            if generateSolutionBoard(board, max_number, current_position + 1):
                return True
            board[row][col] = 0
    
    return False

# mainから呼び出される関数
def generateSolutionBoardWrapper(board, max_number):
    board_copy = [row[:] for row in board]
    if generateSolutionBoard(board_copy, max_number):
        for i in range(max_number):
            for j in range(max_number):
                board[i][j] = board_copy[i][j]
        return True
    return False