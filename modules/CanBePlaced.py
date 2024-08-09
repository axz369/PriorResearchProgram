class CanBePlaced:
    def __init__(self, board, maxNumber):
        self.board = board
        self.maxNumber = maxNumber
        self.subBlockSize = int(maxNumber ** 0.5)

    def check(self, currentPosition, x):
        rows = currentPosition // self.maxNumber  # 行を計算
        columns = currentPosition % self.maxNumber  # 列を計算

        # 行と列に同じ数字がないかチェック
        for i in range(self.maxNumber):
            if self.board[rows][i] == x or self.board[i][columns] == x:
                return False

        # サブブロックに同じ数字がないかチェック
        topLeftCellOfSubblock = (rows // self.subBlockSize) * self.subBlockSize
        for i in range(self.subBlockSize):
            for j in range(self.subBlockSize):
                if self.board[topLeftCellOfSubblock + i][(columns // self.subBlockSize) * self.subBlockSize + j] == x:
                    return False

        return True
