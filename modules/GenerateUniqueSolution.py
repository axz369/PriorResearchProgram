import pulp

class GenerateUniqueSolution:
    def __init__(self, board, maxNumber):
        # 初期盤面と盤面のサイズを設定
        self.c1 = board
        self.maxNumber = maxNumber
        self.subBlockSize = int(maxNumber ** 0.5)
        
        # 線形計画問題を初期化
        self.problem = pulp.LpProblem("Sudoku", pulp.LpMinimize)
        
        # 決定変数を作成: choices[r][c][v] は r行c列にvが入るかどうかを表す
        self.choices = pulp.LpVariable.dicts(
            "Choice", 
            (range(maxNumber), range(maxNumber), range(1, maxNumber + 1)),
            cat=pulp.LpBinary
        )
        
        # 解の出現回数を記録するための3次元配列
        self.memoryArray = [[[0 for _ in range(maxNumber)] for _ in range(maxNumber)] for _ in range(maxNumber)]

    def formulateConstraints(self):
        print("制約条件の設定を開始します。")
        
        # 制約1: 各マスには1つの数字のみが入る
        for r in range(self.maxNumber):
            for c in range(self.maxNumber):
                self.problem += pulp.lpSum(self.choices[r][c][v] for v in range(1, self.maxNumber + 1)) == 1

        # 制約2: 各行には1からmaxNumberまでの数字が1つずつ入る
        for r in range(self.maxNumber):
            for v in range(1, self.maxNumber + 1):
                self.problem += pulp.lpSum(self.choices[r][c][v] for c in range(self.maxNumber)) == 1

        # 制約3: 各列には1からmaxNumberまでの数字が1つずつ入る
        for c in range(self.maxNumber):
            for v in range(1, self.maxNumber + 1):
                self.problem += pulp.lpSum(self.choices[r][c][v] for r in range(self.maxNumber)) == 1

        # 制約4: 各ブロックには1からmaxNumberまでの数字が1つずつ入る
        for br in range(self.subBlockSize):
            for bc in range(self.subBlockSize):
                for v in range(1, self.maxNumber + 1):
                    self.problem += pulp.lpSum(self.choices[r][c][v] 
                                               for r in range(br*self.subBlockSize, (br+1)*self.subBlockSize) 
                                               for c in range(bc*self.subBlockSize, (bc+1)*self.subBlockSize)) == 1

        # 制約5: 既に数字が入っているマスの制約
        for r in range(self.maxNumber):
            for c in range(self.maxNumber):
                if self.c1[r][c] != 0:
                    self.problem += self.choices[r][c][self.c1[r][c]] == 1

        print("制約条件の設定が完了しました。")

    def solve(self):
        # 問題を解く
        status = self.problem.solve()
        if status == pulp.LpStatusOptimal:
            # 最適解が見つかった場合、解を取り出す
            solution = [[0 for _ in range(self.maxNumber)] for _ in range(self.maxNumber)]
            for r in range(self.maxNumber):
                for c in range(self.maxNumber):
                    for v in range(1, self.maxNumber + 1):
                        if pulp.value(self.choices[r][c][v]) == 1:
                            solution[r][c] = v
            return solution
        return None

    def countOccurrences(self, solution):
        # 解の出現回数をカウント
        for r in range(self.maxNumber):
            for c in range(self.maxNumber):
                v = solution[r][c]
                if v != 0:
                    self.memoryArray[r][c][v-1] += 1

    def findMinimumOccurrence(self):
        # 最小出現回数の位置を見つける
        minCount = float('inf')
        minPos = None
        for r in range(self.maxNumber):
            for c in range(self.maxNumber):
                if self.c1[r][c] == 0:  # 元々ヒントがない場所のみ考慮
                    for v in range(self.maxNumber):
                        if 0 < self.memoryArray[r][c][v] < minCount:
                            minCount = self.memoryArray[r][c][v]
                            minPos = (r, c, v+1)
        return minPos

    def addHint(self, pos):
        # ヒントを追加
        if pos:
            r, c, v = pos
            self.c1[r][c] = v
            self.problem += self.choices[r][c][v] == 1

    def addExclusionConstraint(self, solution):
        # 探索済み盤面パターンを除外する制約を追加
        self.problem += pulp.lpSum(self.choices[r][c][solution[r][c]] 
                                   for r in range(self.maxNumber) 
                                   for c in range(self.maxNumber)) <= self.maxNumber * self.maxNumber - 1

    def generateUniqueSolution(self):
        print("唯一解の生成を開始します。")
        self.formulateConstraints()
        
        while True:
            solutions = []
            while True:
                # 解を見つける
                solution = self.solve()
                if solution is None:
                    break
                solutions.append(solution)
                self.countOccurrences(solution)
                
                # 探索済み盤面パターンを除外する制約を追加
                self.addExclusionConstraint(solution)

            if len(solutions) == 1:
                print("唯一解が見つかりました。")
                return solutions[0]
            elif len(solutions) == 0:
                print("解が見つかりませんでした。")
                return None

            # 最小出現回数の位置を見つけてヒントを追加
            minPos = self.findMinimumOccurrence()
            if minPos:
                self.addHint(minPos)
                print(f"ヒントを追加しました: {minPos}")
                # 問題を初期化して再度制約を設定
                self.problem = pulp.LpProblem("Sudoku", pulp.LpMinimize)
                self.choices = pulp.LpVariable.dicts(
                    "Choice", 
                    (range(self.maxNumber), range(self.maxNumber), range(1, self.maxNumber + 1)),
                    cat=pulp.LpBinary
                )
                self.formulateConstraints()
            else:
                print("これ以上ヒントを追加できません。")
                return None

        return None

    def printBoard(self, board):
        # 盤面を表示
        for row in board:
            print(" ".join(str(num) if num != 0 else "." for num in row))

    def printMemoryArray(self):
        # メモリ配列の内容を表示
        for r in range(self.maxNumber):
            for c in range(self.maxNumber):
                print(f"位置 ({r}, {c}):")
                for v in range(self.maxNumber):
                    print(f"  {v+1}: {self.memoryArray[r][c][v]}")
                print()