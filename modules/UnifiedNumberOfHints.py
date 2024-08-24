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

        last_added_position = None  # 直前に追加したヒント位置を保持する

        # 指定された数だけヒントを追加
        for i in range(hintsToAdd):
            if not positions:
                break

            if i % 2 == 0:
                # 奇数回目: ランダムな位置にヒントを追加
                r, c = positions.pop()
                board[r][c] = self.boardA[r][c]
                last_added_position = (r, c)
            else:
                # 偶数回目: 直前の位置と対称な位置にヒントを追加
                if last_added_position:
                    lr, lc = last_added_position
                    sym_r = self.size - 1 - lr
                    sym_c = self.size - 1 - lc
                    if board[sym_r][sym_c] == 0:
                        board[sym_r][sym_c] = self.boardA[sym_r][sym_c]
                    else:
                        # 対称位置が埋まっている場合、新たにランダムな位置にヒントを追加
                        r, c = positions.pop()
                        board[r][c] = self.boardA[r][c]
                else:
                    # 直前に追加した位置がない場合（安全のための処理）
                    r, c = positions.pop()
                    board[r][c] = self.boardA[r][c]

