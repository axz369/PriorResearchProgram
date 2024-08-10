import random
from modules.CanBePlaced import CanBePlaced

class Validation:
    def __init__(self, charToNumberMap, board, maxNumber):
        self.charToNumberMap = charToNumberMap
        self.board = board
        self.maxNumber = maxNumber
        self.subBlockSize = int(maxNumber ** 0.5)
        self.MAX_RECURSION_DEPTH = 1000  # 再帰の最大深さを設定

    def check(self):
        if not self.checkRows():
            return False
        if not self.checkColumns():
            return False
        if not self.checkBlocks():
            return False
        if not self.checkCharCount():
            return False
        if not self.checkSolutionExists():
            return False
        return True

    def checkRows(self):
        for row in self.board:
            values = [val for val in row if val != 0]
            if len(set(values)) != len(values):
                print("Validation失敗 : 同じ行内の重複")
                return False
        return True

    def checkColumns(self):
        for col in range(self.maxNumber):
            values = [self.board[row][col] for row in range(self.maxNumber) if self.board[row][col] != 0]
            if len(set(values)) != len(values):
                print("Validation失敗 : 同じ列内の重複")
                return False
        return True

    def checkBlocks(self):
        for block_row in range(self.subBlockSize):
            for block_col in range(self.subBlockSize):
                values = []
                for row in range(self.subBlockSize):
                    for col in range(self.subBlockSize):
                        value = self.board[block_row * self.subBlockSize + row][block_col * self.subBlockSize + col]
                        if value != 0:
                            values.append(value)
                if len(set(values)) != len(values):
                    print("Validation失敗 : 同じブロック内の重複")
                    return False
        return True

    def checkCharCount(self):
        if len(self.charToNumberMap) > self.maxNumber:
            print("Validation失敗 : 入力された盤面の文字の種類数がmaxNumberを超えている")
            return False
        return True

    def checkSolutionExists(self):
        solutionBoard = [row[:] for row in self.board]  # boardのコピーを作成
        return self.generateSolutionBoard(solutionBoard, 0, 0)

    def generateSolutionBoard(self, solutionBoard, currentPosition, depth):
        if depth > self.MAX_RECURSION_DEPTH:
            return False  # 再帰の深さが最大値を超えたら False を返す

        canBePlacedChecker = CanBePlaced(solutionBoard, self.maxNumber)

        if currentPosition == self.maxNumber * self.maxNumber:
            return True

        newPosition = currentPosition
        while newPosition < self.maxNumber * self.maxNumber and solutionBoard[newPosition // self.maxNumber][newPosition % self.maxNumber] != 0:
            newPosition += 1

        if newPosition == self.maxNumber * self.maxNumber:
            return True

        randomNumbers = random.sample(range(1, self.maxNumber + 1), self.maxNumber)

        for x in randomNumbers:
            if canBePlacedChecker.check(newPosition, x):
                solutionBoard[newPosition // self.maxNumber][newPosition % self.maxNumber] = x
                if self.generateSolutionBoard(solutionBoard, newPosition + 1, depth + 1):
                    return True
                solutionBoard[newPosition // self.maxNumber][newPosition % self.maxNumber] = 0

        return False