import random


class UnifiedNumberOfHints:
    def __init__(self, boards, targetHintCount=28):
        self.boards = boards
        self.size = len(boards[0])
        self.targetHintCount = targetHintCount

    def countHints(self, board):
        # 各盤面のヒント数をカウント,0以外をカウント
        return self.size * self.size - sum(row.count(0) for row in board)

    def unifyHints(self):
        # 各盤面のヒント数を取得
        hintCounts = [self.countHints(board) for board in self.boards]
        maxHints = max(hintCounts)  # 最大ヒント数を取得

        # 最大ヒント数が目標ヒント数より大きければ、その数に合わせる
        targetHints = max(maxHints, self.targetHintCount)

        # 各盤面のヒント数を統一
        for i, board in enumerate(self.boards):
            currentHintCount = self.countHints(board)
            if currentHintCount < targetHints:
                self.addHints(board, targetHints - currentHintCount)

        return self.boards

    def addHints(self, board, hintsToAdd):
        # 空白セルを探す
        positions = [(r, c) for r in range(self.size)
                     for c in range(self.size) if board[r][c] == 0]
        random.shuffle(positions)

        # 指定された数だけヒントを追加
        for _ in range(hintsToAdd):
            if not positions:
                break
            r, c = positions.pop()
            while True:
                value = random.randint(1, self.size)
                if self.canPlaceHint(board, r, c, value):
                    board[r][c] = value
                    break

    def canPlaceHint(self, board, row, col, value):
        # ヒントが行、列、ブロック内で重複しないかを確認
        for i in range(self.size):
            if board[row][i] == value or board[i][col] == value:
                return False

        subblockSize = int(self.size ** 0.5)
        startRow = (row // subblockSize) * subblockSize
        startCol = (col // subblockSize) * subblockSize
        for r in range(startRow, startRow + subblockSize):
            for c in range(startCol, startCol + subblockSize):
                if board[r][c] == value:
                    return False

        return True
