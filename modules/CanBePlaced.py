class CanBePlaced:
    def __init__(self, board, maxNumber):
        self.board = board
        self.maxNumber = maxNumber
        self.subBlockSize = int(maxNumber ** 0.5)

    def check(self, currentPosition, x):
        rows = currentPosition // self.maxNumber
        columns = currentPosition % self.maxNumber

        # 行と列に同じ数字がないかチェック
        for i in range(self.maxNumber):
            if i < len(self.board) and columns < len(self.board[i]):
                if self.board[i][columns] == x:
                    return False
            if rows < len(self.board) and i < len(self.board[rows]):
                if self.board[rows][i] == x:
                    return False

        # サブブロックに同じ数字がないかチェック
        topLeftCellOfSubblock = (rows // self.subBlockSize) * self.subBlockSize
        leftCellOfSubblock = (columns // self.subBlockSize) * self.subBlockSize
        for i in range(self.subBlockSize):
            for j in range(self.subBlockSize):
                if (topLeftCellOfSubblock + i < len(self.board) and
                    leftCellOfSubblock + j < len(self.board[topLeftCellOfSubblock + i])):
                    if self.board[topLeftCellOfSubblock + i][leftCellOfSubblock + j] == x:
                        return False

        return True