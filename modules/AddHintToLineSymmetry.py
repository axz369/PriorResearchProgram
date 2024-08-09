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

    def addSymmetry(self):
        # どの線対称にするかをランダムに選ぶ（1: 横, 2: 縦, 3: 右上がり対角, 4: 右下がり対角）
        symmetryType = random.randint(1, 4)
        print("symmetryType:")
        print(symmetryType)

        if symmetryType == 1:
            self.addHorizontalSymmetry()
        elif symmetryType == 2:
            self.addVerticalSymmetry()
        elif symmetryType == 3:
            self.addDiagonalSymmetry()
        elif symmetryType == 4:
            self.addAntiDiagonalSymmetry()

    def addHorizontalSymmetry(self):  # 横対称
        for row in range(self.size):
            for col in range(self.size):
                oppositeRow = self.size - 1 - row  # 下側の対称位置を計算
                self.addToOppositePosition(row, col, oppositeRow, col)

    def addVerticalSymmetry(self):  # 縦対称
        for row in range(self.size):
            for col in range(self.size):
                oppositeCol = self.size - 1 - col  # 右側の対称位置を計算
                self.addToOppositePosition(row, col, row, oppositeCol)

    def addDiagonalSymmetry(self):  # 右上がり
        for row in range(self.size):
            for col in range(self.size):
                oppositeRow = self.size - 1 - col  # 対称位置の行を計算
                oppositeCol = self.size - 1 - row  # 対称位置の列を計算
                self.addToOppositePosition(row, col, oppositeRow, oppositeCol)

    def addAntiDiagonalSymmetry(self):  # 右下がり
        for row in range(self.size):
            for col in range(self.size):
                oppositeRow = col  # 対称位置の行を計算
                oppositeCol = row  # 対称位置の列を計算
                self.addToOppositePosition(row, col, oppositeRow, oppositeCol)

    def addToOppositePosition(self, row, col, oppositeRow, oppositeCol):
        # 現在の位置に値があり、かつ対称位置に値が入っていない場合
        if self.board[row][col] != 0 and self.board[oppositeRow][oppositeCol] == 0:
            attempts = 0
            while attempts < self.maxAttempts:
                randomValue = random.choice(self.possibleValues)
                if self.canBePlacedChecker.check(oppositeRow * self.size + oppositeCol, randomValue):
                    # 配置できる場合、対称位置に値を入れる
                    self.board[oppositeRow][oppositeCol] = randomValue
                    return
                attempts += 1  # 配置できなかった場合、再トライ

    def getSymmetricBoard(self):
        # 対称にヒントを追加した盤面を返す
        return self.board
