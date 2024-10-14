import gurobipy as gp


def generateSolutionBoard(board):
    max_number = len(board)

    # 問題の定義
    prob = gp.Model("Sudoku")

    # 出力をオフにする
    prob.setParam('OutputFlag', 0)

    # 決定変数の作成
    choices = {}
    for r in range(max_number):
        for c in range(max_number):
            for n in range(1, max_number + 1):
                choices[r, c, n] = prob.addVar(vtype=gp.GRB.BINARY, name=f"Choice_{r}_{c}_{n}")

    # 目的関数（この場合は特に必要ないので、ダミーの目的関数を設定）
    prob.setObjective(0, gp.GRB.MINIMIZE)

    # 制約条件の追加
    # 1. 各セルには1つの数字のみが入る
    for r in range(max_number):
        for c in range(max_number):
            prob.addConstr(gp.quicksum(choices[r, c, n] for n in range(1, max_number + 1)) == 1)

    # 2. 各行には1からmax_numberの数字が1つずつ入る
    for r in range(max_number):
        for n in range(1, max_number + 1):
            prob.addConstr(gp.quicksum(choices[r, c, n] for c in range(max_number)) == 1)

    # 3. 各列には1からmax_numberの数字が1つずつ入る
    for c in range(max_number):
        for n in range(1, max_number + 1):
            prob.addConstr(gp.quicksum(choices[r, c, n] for r in range(max_number)) == 1)

    # 4. 各ブロックには1からmax_numberの数字が1つずつ入る
    block_size = int(max_number ** 0.5)
    for br in range(block_size):
        for bc in range(block_size):
            for n in range(1, max_number + 1):
                prob.addConstr(gp.quicksum(choices[r, c, n]
                                           for r in range(br * block_size, (br + 1) * block_size)
                                           for c in range(bc * block_size, (bc + 1) * block_size)) == 1)

    # 5. 既に数字が入っているセルの制約
    for r in range(max_number):
        for c in range(max_number):
            if board[r][c] != 0:
                prob.addConstr(choices[r, c, board[r][c]] == 1)

    # 問題を解く
    prob.optimize()

    # 解が見つかった場合、盤面を更新
    if prob.status == gp.GRB.OPTIMAL:
        for r in range(max_number):
            for c in range(max_number):
                for n in range(1, max_number + 1):
                    if choices[r, c, n].x > 0.5:
                        board[r][c] = n
        return True
    else:
        return False


# mainから呼び出される関数
def generateSolutionBoardWrapper(board):
    board_copy = [row[:] for row in board]
    if generateSolutionBoard(board_copy):
        for i in range(len(board)):
            for j in range(len(board)):
                board[i][j] = board_copy[i][j]
        return True
    return False
