import pulp

class GenerateUniqueSolution:
    def __init__(self, board, maxNumber):
        self.board = board
        self.maxNumber = maxNumber
        self.subBlockSize = int(maxNumber ** 0.5)
        self.problem = pulp.LpProblem("Sudoku", pulp.LpMaximize)
        self.choices = pulp.LpVariable.dicts(
            "Choice", 
            (range(maxNumber), range(maxNumber), range(maxNumber)),
            cat=pulp.LpBinary
        )
        self.solutionCount = 0
        self.solutionArray = [[[0 for _ in range(maxNumber)] for _ in range(maxNumber)] for _ in range(maxNumber)]

    def formulateConstraints(self):
        # (1) 一つのマスには一つの文字が入る
        for i in range(self.maxNumber):
            for j in range(self.maxNumber):
                self.problem += pulp.lpSum([self.choices[i][j][k] for k in range(self.maxNumber)]) == 1

        # (2) 同じ列にはすべて違う値が入る
        for j in range(self.maxNumber):
            for k in range(self.maxNumber):
                self.problem += pulp.lpSum([self.choices[i][j][k] for i in range(self.maxNumber)]) == 1

        # (3) 同じ行にはすべて違う値が入る
        for i in range(self.maxNumber):
            for k in range(self.maxNumber):
                self.problem += pulp.lpSum([self.choices[i][j][k] for j in range(self.maxNumber)]) == 1

        # (4) 同じブロックにはすべて違う値が入る
        for k in range(self.maxNumber):
            for blockRow in range(self.subBlockSize):
                for blockCol in range(self.subBlockSize):
                    self.problem += pulp.lpSum(
                        [self.choices[i][j][k] 
                         for i in range(blockRow * self.subBlockSize, (blockRow + 1) * self.subBlockSize)
                         for j in range(blockCol * self.subBlockSize, (blockCol + 1) * self.subBlockSize)]
                    ) == 1

        # (5) 既配置ヒントの定式化
        for i in range(self.maxNumber):
            for j in range(self.maxNumber):
                if self.board[i][j] != 0:
                    k = self.board[i][j] - 1  # インデックスを0から開始するために1を減算
                    self.problem += self.choices[i][j][k] == 1

    def addExclusionConstraint(self, solution):
        # (6) 探索済み盤面パターンを除外する制約を追加
        exclusionConstraint = pulp.lpSum(
            self.choices[i][j][solution[i][j] - 1]
            for i in range(self.maxNumber)
            for j in range(self.maxNumber)
        )
        self.problem += exclusionConstraint <= self.maxNumber * self.maxNumber - 1

    def solve(self):
        # 問題を解く
        self.problem.solve()
        if pulp.LpStatusOptimal == self.problem.status:
            # 最適解が見つかった場合、解を取り出す
            solution = [[0] * self.maxNumber for _ in range(self.maxNumber)]
            for i in range(self.maxNumber):
                for j in range(self.maxNumber):
                    for k in range(self.maxNumber):
                        if self.choices[i][j][k].varValue == 1:
                            solution[i][j] = k + 1  # インデックスを戻す
            return solution
        else:
            # 最適解が見つからなかった場合
            return None

    def adjustToUniqueSolution(self):
        # 初期問題の定式化
        self.formulateConstraints()
        
        # 解の探索を行い、複数解がある場合は調整する
        while True:
            solution = self.solve()
            if solution is None:
                break

            self.solutionCount += 1
            # 解のカウント
            for i in range(self.maxNumber):
                for j in range(self.maxNumber):
                    k = solution[i][j] - 1
                    self.solutionArray[i][j][k] += 1
            
            # 現在の解を除外する制約を追加して次の解を探索
            self.addExclusionConstraint(solution)

        # 解の登場回数が1のものだけを残し、唯一解に調整
        for i in range(self.maxNumber):
            for j in range(self.maxNumber):
                for k in range(self.maxNumber):
                    if self.solutionArray[i][j][k] == 1:
                        self.board[i][j] = k + 1

        return self.board

    def generateUniqueSolution(self):
        # 唯一解への調整
        return self.adjustToUniqueSolution()
