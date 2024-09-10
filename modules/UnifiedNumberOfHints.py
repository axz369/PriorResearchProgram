import random
from utility.printBoard import printBoard


class UnifiedNumberOfHints:
    def __init__(self, boards, boardA, targetHintCount=28, symmetry_type='horizontal'):
        self.boards = boards
        self.boardA = boardA
        self.size = len(boards[0])
        self.targetHintCount = targetHintCount
        self.symmetry_type = symmetry_type

    def countHints(self, board):
        return self.size * self.size - sum(row.count(0) for row in board)

    def unifyHints(self):
        hintCounts = [self.countHints(board) for board in self.boards]
        targetHints = max(max(hintCounts), self.targetHintCount)

        for i, board in enumerate(self.boards):
            currentHintCount = self.countHints(board)
            if currentHintCount < targetHints:
                print(f"\n盤面 {i + 1} のヒント追加処理開始:")
                if self.symmetry_type == 'horizontal':
                    self.addHintsHorizontal(board, targetHints - currentHintCount)
                elif self.symmetry_type == 'vertical':
                    self.addHintsVertical(board, targetHints - currentHintCount)
                elif self.symmetry_type == 'diagonal_up':
                    self.addHintsDiagonalUp(board, targetHints - currentHintCount)
                elif self.symmetry_type == 'diagonal_down':
                    self.addHintsDiagonalDown(board, targetHints - currentHintCount)

        return self.boards

    def addHintsHorizontal(self, board, hintsToAdd):
        positions = [(r, c) for r in range(self.size) for c in range(self.size) if board[r][c] == 0]
        random.shuffle(positions)

        for _ in range(hintsToAdd):
            if not positions:
                break

            r, c = positions.pop()
            board[r][c] = self.boardA[r][c]
            print(f"追加: 位置 ({c + 1}, {r + 1}) にヒント {board[r][c]} を追加")

            symR = self.size - 1 - r
            if (symR, c) in positions:
                board[symR][c] = self.boardA[symR][c]
                positions.remove((symR, c))
                print(f"対称追加: 位置 ({c + 1}, {symR + 1}) にヒント {board[symR][c]} を追加")

            self.printBoardStatus(board)

    def addHintsVertical(self, board, hintsToAdd):
        positions = [(r, c) for r in range(self.size) for c in range(self.size) if board[r][c] == 0]
        random.shuffle(positions)

        for _ in range(hintsToAdd):
            if not positions:
                break

            r, c = positions.pop()
            board[r][c] = self.boardA[r][c]
            print(f"追加: 位置 ({c + 1}, {r + 1}) にヒント {board[r][c]} を追加")

            symC = self.size - 1 - c
            if (r, symC) in positions:
                board[r][symC] = self.boardA[r][symC]
                positions.remove((r, symC))
                print(f"対称追加: 位置 ({symC + 1}, {r + 1}) にヒント {board[r][symC]} を追加")

            self.printBoardStatus(board)

    def addHintsDiagonalUp(self, board, hintsToAdd):
        positions = [(r, c) for r in range(self.size) for c in range(self.size) if board[r][c] == 0]
        random.shuffle(positions)

        for _ in range(hintsToAdd):
            if not positions:
                break

            r, c = positions.pop()
            board[r][c] = self.boardA[r][c]
            print(f"追加: 位置 ({c + 1}, {r + 1}) にヒント {board[r][c]} を追加")

            symR, symC = c, r
            if (symR, symC) in positions:
                board[symR][symC] = self.boardA[symR][symC]
                positions.remove((symR, symC))
                print(f"対称追加: 位置 ({symC + 1}, {symR + 1}) にヒント {board[symR][symC]} を追加")

            self.printBoardStatus(board)

    def addHintsDiagonalDown(self, board, hintsToAdd):
        positions = [(r, c) for r in range(self.size) for c in range(self.size) if board[r][c] == 0]
        random.shuffle(positions)

        for _ in range(hintsToAdd):
            if not positions:
                break

            r, c = positions.pop()
            board[r][c] = self.boardA[r][c]
            print(f"追加: 位置 ({c + 1}, {r + 1}) にヒント {board[r][c]} を追加")

            symR, symC = self.size - 1 - c, self.size - 1 - r
            if (symR, symC) in positions:
                board[symR][symC] = self.boardA[symR][symC]
                positions.remove((symR, symC))
                print(f"対称追加: 位置 ({symC + 1}, {symR + 1}) にヒント {board[symR][symC]} を追加")

            self.printBoardStatus(board)

    def printBoardStatus(self, board):
        print("更新後の盤面:")
        printBoard(board)
        print(f"現在のヒント数: {self.countHints(board)}")
        print("--------------------")
