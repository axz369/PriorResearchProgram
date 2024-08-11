import random
from modules.CanBePlaced import CanBePlaced

class AddHintToLineSymmetry:
    def __init__(self, board):
        self.board = board
        self.size = len(board)
        self.possibleValues = list(range(1, self.size + 1))
        # CanBePlacedクラスのインスタンスを作成
        self.canBePlacedChecker = CanBePlaced(board, self.size)
        self.maxAttempts = 1000  # 再トライの最大回数を設定

    def addSymmetries(self):
        # 4つの対称性に基づいた盤面をリストで返却
        boards = []
        boards.append(self.addHorizontalSymmetry())
        boards.append(self.addVerticalSymmetry())
        boards.append(self.addDiagonalSymmetry())
        boards.append(self.addAntiDiagonalSymmetry())
        return boards

    def addHorizontalSymmetry(self):  # 横対称
        board_copy = [row[:] for row in self.board]  # 現在の盤面のコピーを作成
        for row in range(self.size):
            for col in range(self.size):
                oppositeRow = self.size - 1 - row  # 下側の対称位置を計算
                self.addToOppositePosition(board_copy, row, col, oppositeRow, col)
        return board_copy

    def addVerticalSymmetry(self):  # 縦対称
        board_copy = [row[:] for row in self.board]  # 現在の盤面のコピーを作成
        for row in range(self.size):
            for col in range(self.size):
                oppositeCol = self.size - 1 - col  # 右側の対称位置を計算
                self.addToOppositePosition(board_copy, row, col, row, oppositeCol)
        return board_copy

    def addDiagonalSymmetry(self):  # 右上がり
        board_copy = [row[:] for row in self.board]  # 現在の盤面のコピーを作成
        for row in range(self.size):
            for col in range(self.size):
                oppositeRow = self.size - 1 - col  # 対称位置の行を計算
                oppositeCol = self.size - 1 - row  # 対称位置の列を計算
                self.addToOppositePosition(board_copy, row, col, oppositeRow, oppositeCol)
        return board_copy

    def addAntiDiagonalSymmetry(self):  # 右下がり
        board_copy = [row[:] for row in self.board]  # 現在の盤面のコピーを作成
        for row in range(self.size):
            for col in range(self.size):
                oppositeRow = col  # 対称位置の行を計算
                oppositeCol = row  # 対称位置の列を計算
                self.addToOppositePosition(board_copy, row, col, oppositeRow, oppositeCol)
        return board_copy

    def addToOppositePosition(self, board_copy, row, col, oppositeRow, oppositeCol):
        # 現在の位置に値があり、かつ対称位置に値が入っていない場合
        if board_copy[row][col] != 0 and board_copy[oppositeRow][oppositeCol] == 0:
            attempts = 0
            while attempts < self.maxAttempts:
                randomValue = random.choice(self.possibleValues)
                if self.canBePlacedChecker.check(oppositeRow * self.size + oppositeCol, randomValue):
                    # 配置できる場合、対称位置に値を入れる
                    board_copy[oppositeRow][oppositeCol] = randomValue
                    return
                attempts += 1  # 配置できなかった場合、再トライ

    def getSymmetricBoards(self):
        # 4つの対称性に基づいた盤面を返す
        return self.addSymmetries()
