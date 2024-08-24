import random
from modules.CanBePlaced import CanBePlaced


def generateSolutionBoard(solutionBoard, maxNumber, currentPosition=0, depth=0, maxRecursionDepth=1000):
    if depth > maxRecursionDepth:
        return False  # 再帰の深さが最大値を超えたら False を返す

    canBePlacedChecker = CanBePlaced(solutionBoard, maxNumber)

    if currentPosition == maxNumber * maxNumber:
        return True

    newPosition = currentPosition
    while newPosition < maxNumber * maxNumber and solutionBoard[newPosition // maxNumber][newPosition % maxNumber] != 0:
        newPosition += 1

    if newPosition == maxNumber * maxNumber:
        return True

    randomNumbers = random.sample(range(1, maxNumber + 1), maxNumber)

    for x in randomNumbers:
        if canBePlacedChecker.check(newPosition, x):
            solutionBoard[newPosition // maxNumber][newPosition % maxNumber] = x
            if generateSolutionBoard(solutionBoard, maxNumber, newPosition + 1, depth + 1, maxRecursionDepth):
                return True
            solutionBoard[newPosition // maxNumber][newPosition % maxNumber] = 0

    return False
