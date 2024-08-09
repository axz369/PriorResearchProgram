from pulp import LpProblem, LpVariable, LpMinimize, lpSum


class FormulateSudoku:
    def __init__(self, board, maxNumber):
        self.board = board
        self.maxNumber = maxNumber
        self.problem = None
        self.choices = None
        self.formulate()

    def formulate(self):
        # 問題を作成
        self.problem = LpProblem("SudokuProblem", LpMinimize)

        # 各セルにどの数字が入るかを表すバイナリの決定変数
        self.choices = LpVariable.dicts(
            "Choice",
            (range(self.maxNumber), range(self.maxNumber),
             range(1, self.maxNumber + 1)),
            0, 1, cat="Binary"
        )

        # 与えられた値をそのまま使用する制約を追加
        for row in range(self.maxNumber):
            for col in range(self.maxNumber):
                if self.board[row][col] != 0:
                    self.problem += self.choices[row][col][self.board[row][col]] == 1

        # 各行に同じ値が入らない制約
        for row in range(self.maxNumber):
            for num in range(1, self.maxNumber + 1):
                self.problem += lpSum([self.choices[row][col][num]
                                      for col in range(self.maxNumber)]) == 1

        # 各列に同じ値が入らない制約
        for col in range(self.maxNumber):
            for num in range(1, self.maxNumber + 1):
                self.problem += lpSum([self.choices[row][col][num]
                                      for row in range(self.maxNumber)]) == 1

        # 各サブブロックに同じ値が入らない制約
        subBlockSize = int(self.maxNumber ** 0.5)
        for subBlockRow in range(subBlockSize):
            for subBlockCol in range(subBlockSize):
                for num in range(1, self.maxNumber + 1):
                    self.problem += lpSum([
                        self.choices[row][col][num]
                        for row in range(subBlockRow * subBlockSize, (subBlockRow + 1) * subBlockSize)
                        for col in range(subBlockCol * subBlockSize, (subBlockCol + 1) * subBlockSize)
                    ]) == 1

        # 各セルに1つの値が入る制約
        for row in range(self.maxNumber):
            for col in range(self.maxNumber):
                self.problem += lpSum([self.choices[row][col][num]
                                      for num in range(1, self.maxNumber + 1)]) == 1

    def getProblemAndChoices(self):  # キャメルケース
        return self.problem, self.choices
