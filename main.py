import time
import json
import pulp
from pulp import LpStatus

from modules.ConvertToNumber import ConvertToNumber
from modules.Validation import Validation
from modules.AddHintToLineSymmetry import AddHintToLineSymmetry
from modules.UnifiedNumberOfHints import UnifiedNumberOfHints

from utility.getUserChoice import getUserChoice
from utility.generateSolutionBoard import generateSolutionBoard
from utility.printBoard import printBoard


def generateUniqueSolution(board, boardName):
    start_time = time.time()

    print("唯一解生成開始")
    print(f"選ばれた盤面 : {boardName}")
    for row in board:
        print(row)

    size = len(board)
    max_solutions = 30  # 生成する解の最大数

    while True:  # 外部ループ:内部ループ内で解盤面が一つしか見つからなくなったら終了
        solution_count = 0  # 解の数をカウント
        last_solution = None  # 最後に見つかった解を保持

        # 111~999の連続した配列 (0-indexedなので実際は[0][0][0]から[8][8][8])
        occurrence_count = [
            [[0 for _ in range(size)] for _ in range(size)] for _ in range(size)]

        problem = pulp.LpProblem("Sudoku", pulp.LpMinimize)

        # 決定変数の作成
        isValueInCell = pulp.LpVariable.dicts("IsValueInCell",
                                              (range(size), range(size),
                                               range(1, size + 1)),
                                              cat='Binary')

        # 制約条件の追加
        # 1. 各マスには1つの数字のみが入る
        for i in range(size):
            for j in range(size):
                problem += pulp.lpSum([isValueInCell[i][j][k]
                                      for k in range(1, size + 1)]) == 1

        # 2. 各行には1から9の数字が1つずつ入る
        for i in range(size):
            for k in range(1, size + 1):
                problem += pulp.lpSum([isValueInCell[i][j][k]
                                      for j in range(size)]) == 1

        # 3. 各列には1から9の数字が1つずつ入る
        for j in range(size):
            for k in range(1, size + 1):
                problem += pulp.lpSum([isValueInCell[i][j][k]
                                      for i in range(size)]) == 1

        # 4. 各3x3ブロックには1から9の数字が1つずつ入る
        block_size = int(size ** 0.5)
        for bi in range(block_size):
            for bj in range(block_size):
                for k in range(1, size + 1):
                    problem += pulp.lpSum([isValueInCell[i][j][k]
                                           for i in range(bi * block_size, (bi + 1) * block_size)
                                           for j in range(bj * block_size, (bj + 1) * block_size)]) == 1

        # 5. 初期値（ヒント）の設定
        for i in range(size):
            for j in range(size):
                if board[i][j] != 0:
                    problem += isValueInCell[i][j][board[i][j]] == 1

        # 内部ループ
        while solution_count < max_solutions:
            current_time = time.time()
            if current_time - start_time > 1800:  # 30分（1800秒）を超えた場合
                print("30分を超えたため処理を終了します。")
                return None

            # 問題を解く. ()の中はソルバーの出力off設定
            status = problem.solve(pulp.PULP_CBC_CMD(msg=False))

            # 新しい解盤面が見つかったら
            if pulp.LpStatus[status] == 'Optimal':
                solution_count += 1
                solution = [[0 for _ in range(size)] for _ in range(size)]
                for i in range(size):
                    for j in range(size):
                        for k in range(1, size + 1):
                            if pulp.value(isValueInCell[i][j][k]) == 1:
                                solution[i][j] = k

                last_solution = solution  # 最後の解を保持

                # 111~999の連続した配列に情報を格納
                for i in range(size):
                    for j in range(size):
                        value = solution[i][j]
                        occurrence_count[i][j][value - 1] += 1

                # 新しい解を除外する制約を作成
                new_constraint = pulp.LpAffineExpression(
                    [(isValueInCell[i][j][solution[i][j]], 1)
                     for i in range(size) for j in range(size)]
                )
                # 新しい制約を問題に追加
                problem += new_constraint <= 80  # 80マスまでの一致を許容

                print(f"\n解 {solution_count} が見つかりました:")
                printBoard(solution)
            else:
                print("全ての解盤面を生成しました．")
                break

        print(f"生成された解の数: {solution_count}")

        # 解盤面が一つしか見つからなかった(唯一解が確定)
        if solution_count == 1:
            print("唯一解が見つかりました。")
            print("唯一解生成終了")
            return last_solution

        # 最小出現回数のマスを見つける
        min_count = float('inf')
        min_pos = None
        min_value = None
        for i in range(size):
            for j in range(size):
                if board[i][j] == 0:  # 空のマスのみを対象とする
                    for k in range(size):
                        if 0 < occurrence_count[i][j][k] < min_count:
                            min_count = occurrence_count[i][j][k]
                            min_pos = (i, j)
                            min_value = k + 1

        if min_pos is None:
            print("エラー: 最小出現回数のマスが見つかりませんでした。")
            return None

        # 最小出現回数のマスを盤面に追加
        i, j = min_pos
        board[i][j] = min_value
        print(f"マス ({i + 1}, {j + 1}) に {min_value} を追加しました。")

        # 盤面の表示
        print("現在の盤面:")
        printBoard(board)


def main():
    # JSONファイルを読み込む
    with open('input9.json', 'r') as file:
        data = json.load(file)

    # 使用する数独の問題を選択
    sudokuProblem = data["inputs"]["input1"]
    board = sudokuProblem["board"]
    maxNumber = sudokuProblem["maxNumber"]

    # 入力盤面を表示
    print("入力盤面:")
    printBoard(board)

    # 盤面の文字を数値に変換
    converter = ConvertToNumber(board, maxNumber)
    dataConvertedToNumbers = converter.getConvertedData()

    # Validationクラスを使用して入力ファイルの正当性チェック
    validator = Validation(
        dataConvertedToNumbers['charToNumberMap'], dataConvertedToNumbers['boardConvertedToNumber'], maxNumber)
    if not validator.check():
        print("バリデーション失敗")
        return False

    # generateSolutionBoard関数を使用して解盤面Aを取得
    boardA = [row[:] for row in dataConvertedToNumbers['boardConvertedToNumber']]
    isSolutionGenerated = generateSolutionBoard(boardA, maxNumber)  # 解盤面Aを生成

    if not isSolutionGenerated:
        print("解盤面Aの生成に失敗しました。")
        return False
    else:
        print("解盤面Aが生成されました")
        printBoard(converter.convertBack(boardA))

    # 対称性に基づいたヒントを追加するクラスを作成
    symmetryAdder = AddHintToLineSymmetry(
        dataConvertedToNumbers['boardConvertedToNumber'], boardA)

    # 4つの対称盤面を取得
    symmetricBoards = symmetryAdder.getSymmetricBoards()

    # 対称性タイプのリストを定義
    symmetryTypes = ["horizontal", "vertical", "diagonal_up", "diagonal_down"]

    # 対称軸に追加した直後の盤面を表示
    print("******************************************")
    print("対称軸に追加した直後の盤面:")
    print("******************************************")

    for symmetry_type, board in zip(symmetryTypes, symmetricBoards):
        print(f"\n{symmetry_type}Symmetry:")
        printBoard(converter.convertBack(board))

    # ヒント数の統一処理
    hintUnifier = UnifiedNumberOfHints(symmetricBoards, boardA, targetHintCount=28)
    unifiedBoards = hintUnifier.unifyHints()

    # ヒント数統一後の盤面を表示
    print("\n******************************************")
    print("ヒント数統一後の盤面:")
    print("******************************************")
    for symmetry_type, board in zip(symmetryTypes, unifiedBoards):
        print(f"\n{symmetry_type}Symmetry:")
        printBoard(converter.convertBack(board))

    # 盤面を表示してユーザに選択させる
    userChoice = getUserChoice([f"{s}Symmetry" for s in symmetryTypes])

    # 選択された盤面を取得
    selectedBoard = unifiedBoards[userChoice]
    selectedBoardName = f"{symmetryTypes[userChoice]}Symmetry"

    # 唯一解の生成
    startTime = time.time()
    uniqueSolution = generateUniqueSolution(selectedBoard, selectedBoardName)
    endTime = time.time()

    if uniqueSolution:
        print("最終的な唯一解:")
        printBoard(converter.convertBack(uniqueSolution))
    else:
        print("唯一解の生成に失敗しました。")

    generationTime = endTime - startTime
    print(f"生成時間: {generationTime:.2f}秒")


if __name__ == "__main__":
    main()
