import random
from modules.CanBePlaced import CanBePlaced

class Validation:
    def __init__(self, charToNumberMap, board, maxNumber):
        self.charToNumberMap = charToNumberMap
        self.board = board
        self.maxNumber = maxNumber
        self.subBlockSize = int(maxNumber ** 0.5)

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
        for row in range(self.maxNumber):
            rowValues = [val for val in self.board[row] if val != 0]
            if len(set(rowValues)) != len(rowValues):
                print("Validation失敗 : 同じ行内の重複")
                return False
        return True

    def checkColumns(self):
        for col in range(self.maxNumber):
            colValues = [self.board[row][col] for row in range(self.maxNumber) if self.board[row][col] != 0]
            if len(set(colValues)) != len(colValues):
                print("Validation失敗 : 同じ列内の重複")
                return False
        return True

    def checkBlocks(self):
        for subBlockRow in range(self.subBlockSize):
            for subBlockCol in range(self.subBlockSize):
                blockValues = []
                for row in range(self.subBlockSize):
                    for col in range(self.subBlockSize):
                        cellValue = self.board[subBlockRow * self.subBlockSize + row][subBlockCol * self.subBlockSize + col]
                        if cellValue != 0:
                            blockValues.append(cellValue)
                if len(set(blockValues)) != len(blockValues):
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
        return self.generateSolutionBoard(solutionBoard, 0)

    def generateSolutionBoard(self, solutionBoard, currentPosition):
        canBePlacedChecker = CanBePlaced(solutionBoard, self.maxNumber)  # クラスインスタンス化

        # すべてのセルが埋まった場合
        if currentPosition == self.maxNumber * self.maxNumber:
            return True  # 解答が見つかったことを示す

        # 次にチェックする位置を新しい変数 newPosition に代入
        newPosition = currentPosition
        # 既に数字が埋まっているセルをスキップするループ
        while newPosition < self.maxNumber * self.maxNumber and solutionBoard[newPosition // self.maxNumber][newPosition % self.maxNumber] != 0:
            newPosition += 1

        # 1 から maxNumber までの数字をランダムに並べたリストを生成
        randomNumbers = random.sample(range(1, self.maxNumber + 1), self.maxNumber)

        # ランダムな数字のリストを順に試すループ
        for x in randomNumbers:
            # 数字 x が現在の位置 newPosition に配置可能かをチェック
            if canBePlacedChecker.check(newPosition, x):  # クラスのメソッドを使用
                # 配置可能な場合、盤面に数字 x を配置
                solutionBoard[newPosition // self.maxNumber][newPosition % self.maxNumber] = x
                # 次の位置に進んで再帰的にチェックを続ける
                if self.generateSolutionBoard(solutionBoard, newPosition + 1):
                    return True  # 解答が見つかった場合、True を返す
                # 解答が見つからなかった場合、配置した数字をリセットして次の数字を試す
                solutionBoard[newPosition // self.maxNumber][newPosition % self.maxNumber] = 0

        # すべての数字を試しても解答が見つからなかった場合、False を返す
        return False
