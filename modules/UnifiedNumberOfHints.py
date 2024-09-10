import random
from utility.printBoard import printBoard


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
                print(f"\n盤面 {i + 1} のヒント追加処理開始:")
                self.addHints(board, targetHints - currentHintCount)

        return self.boards

    def addHints(self, board, hintsToAdd):
        # 空白セルを探す
        positions = [(r, c) for r in range(self.size)
                     for c in range(self.size) if board[r][c] == 0]
        random.shuffle(positions)

        # 最後に追加したヒント位置
        lastAddedPosition = None

        # 指定された数だけヒントを追加
        for i in range(hintsToAdd):
            if not positions:
                break

            if i % 2 == 0:  # 偶数回目: ランダムな位置にヒントを追加
                r, c = positions.pop()
                board[r][c] = self.boardA[r][c]
                lastAddedPosition = (r, c)
                print(f"偶数回目: 位置 ({r + 1}, {c + 1}) にヒント {board[r][c]} を追加")
            else:  # 奇数回目: 直前の位置と対称な位置にヒントを追加
                lr, lc = lastAddedPosition
                symR = self.size - 1 - lr
                symC = self.size - 1 - lc
                board[symR][symC] = self.boardA[symR][symC]
                print(f"奇数回目: 位置 ({symR + 1}, {symC + 1}) にヒント {board[symR][symC]} を追加")

            print("更新後の盤面:")
            printBoard(board)
            print(f"現在のヒント数: {self.countHints(board)}")
            print("--------------------")
