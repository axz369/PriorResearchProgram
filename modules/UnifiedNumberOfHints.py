import random

class UnifiedNumberOfHints:
    def __init__(self, boards, boardA, targetHintCount=28):
        self.boards = boards
        self.boardA = boardA
        self.size = len(boards[0])
        self.targetHintCount = targetHintCount

    def countHints(self, board):
        # 各盤面のヒント数をカウント, 0以外をカウント
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
            # 解盤面Aの値を使ってヒントを追加
            board[r][c] = self.boardA[r][c]
