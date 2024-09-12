import random
from .canBePlaced import canBePlaced


def generateSolutionBoard(solution_board, max_number, current_position=0, depth=0, max_recursion_depth=1000):
    if depth > max_recursion_depth:
        return False  # 再帰の深さが最大値を超えたら False を返す

    if current_position == max_number * max_number:
        return True

    new_position = current_position
    while new_position < max_number * max_number and solution_board[new_position // max_number][new_position % max_number] != 0:
        new_position += 1

    if new_position == max_number * max_number:
        return True

    random_numbers = random.sample(range(1, max_number + 1), max_number)

    for x in random_numbers:
        if canBePlaced(solution_board, max_number, new_position, x):
            solution_board[new_position // max_number][new_position % max_number] = x
            if generateSolutionBoard(solution_board, max_number, new_position + 1, depth + 1, max_recursion_depth):
                return True
            solution_board[new_position // max_number][new_position % max_number] = 0

    return False
