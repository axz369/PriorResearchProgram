import time
import json
import pulp
from pulp import LpStatus

from modules.ConvertToNumber import ConvertToNumber
from modules.Validation import Validation
from modules.AddHintToLineSymmetry import AddHintToLineSymmetry
from modules.UnifiedNumberOfHints import UnifiedNumberOfHints
from utility.displayBoards import displayBoards
from utility.getUserChoice import getUserChoice
from utility.generateSolutionBoard import generateSolutionBoard


def generateUniqueSolution(board, boardName):
    print("唯一解生成開始")
    print(f"選ばれた盤面 : {boardName}")
    for row in board:
        print(row)

    size = len(board)
    max_solutions = 10  # 生成する解の最大数

    # 解盤面を管理する配列
    solution_boards = []
    # 111~999の連続した配列 (0-indexedなので実際は[0][0][0]から[8][8][8])
    occurrence_count = [[[0 for _ in range(size)] for _ in range(size)] for _ in range(size)]

    # 問題の初期化
    problem = pulp.LpProblem("Sudoku", pulp.LpMinimize)

    # バイナリ変数の作成
    isValueInCell = pulp.LpVariable.dicts("IsValueInCell",
                                          (range(size), range(size), range(1, size + 1)),
                                          cat='Binary')

    # 制約条件の追加
    # 1. 各マスには1つの数字のみが入る
    for i in range(size):
        for j in range(size):
            problem += pulp.lpSum([isValueInCell[i][j][k] for k in range(1, size + 1)]) == 1

    # 2. 各行には1から9の数字が1つずつ入る
    for i in range(size):
        for k in range(1, size + 1):
            problem += pulp.lpSum([isValueInCell[i][j][k] for j in range(size)]) == 1

    # 3. 各列には1から9の数字が1つずつ入る
    for j in range(size):
        for k in range(1, size + 1):
            problem += pulp.lpSum([isValueInCell[i][j][k] for i in range(size)]) == 1

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

    # 生成する回数に達するまで解盤面生成を行う
    while len(solution_boards) < max_solutions:
        # 問題を解く
        status = problem.solve()

        # pulpの結果から数独の盤面を構築
        if pulp.LpStatus[status] == 'Optimal':
            solution = [[0 for _ in range(size)] for _ in range(size)]
            for i in range(size):
                for j in range(size):
                    for k in range(1, size + 1):
                        # 値が1(対称の値が入っている)ならi行j列にの値kを
                        # solution(直前のコードブロックで生成された数独の1つの解盤面を入れる配列)に記録
                        if pulp.value(isValueInCell[i][j][k]) == 1:
                            solution[i][j] = k

            # 解盤面も保存
            solution_boards.append(solution)

            # 111~999の連続した配列に情報を格納
            for i in range(size):
                for j in range(size):
                    value = solution[i][j]
                    occurrence_count[i][j][value - 1] += 1

            # 今回探索した解を除外する制約を追加
            problem += pulp.lpSum(isValueInCell[i][j][solution[i][j]]
                                  for i in range(size) for j in range(size)) <= size * size - 1
        else:
            break  # 解が見つからない場合はループを抜ける

    print(f"生成された解の数: {len(solution_boards)}")
    print("111~999の連続した配列の内容:")
    for i in range(size):
        for j in range(size):
            print(f"位置 ({i + 1}, {j + 1}):")
            for k in range(size):
                print(f"  {k + 1}: {occurrence_count[i][j][k]}")

    print("唯一解生成終了")
    return solution_boards, occurrence_count


def main():  # 数独パズルを生成, メインの関数
    # JSONファイルを読み込む
    with open('input.json', 'r') as file:
        data = json.load(file)

    # 使用する数独の問題を選択
    sudokuProblem = data["inputs"]["input1"]
    board = sudokuProblem["board"]
    maxNumber = sudokuProblem["maxNumber"]

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
    boardA = [row[:]
              # 元の盤面をコピー
              for row in dataConvertedToNumbers['boardConvertedToNumber']]
    isSolutionGenerated = generateSolutionBoard(boardA, maxNumber)  # 解盤面Aを生成

    if not isSolutionGenerated:
        print("解盤面Aの生成に失敗しました。")
        return False
    else:
        print("解盤面Aが生成されました")
        print(boardA)

    # 対称性に基づいたヒントを追加するクラスを作成
    symmetryAdder = AddHintToLineSymmetry(
        dataConvertedToNumbers['boardConvertedToNumber'], boardA)

    # 4つの対称盤面を取得
    symmetricBoards = symmetryAdder.getSymmetricBoards()

    # ヒント数の統一処理
    hintUnifier = UnifiedNumberOfHints(
        symmetricBoards, boardA, targetHintCount=28)
    unifiedBoards = hintUnifier.unifyHints()

    # 数値から元の文字盤面に戻す
    unifiedBoardsAsChars = []
    for board in unifiedBoards:
        unifiedBoardsAsChars.append(converter.convertBack(board))

    # 対称性の名前
    symmetryNames = ["horizontalSymmetry", "verticalSymmetry",
                     "diagonalSymmetry", "antiDiagonalSymmetry"]

    # 盤面を表示してユーザに選択させる
    displayBoards(unifiedBoardsAsChars, symmetryNames)
    userChoice = getUserChoice(symmetryNames)

    # 選択された盤面を取得
    selectedBoard = unifiedBoards[userChoice]
    selectedBoardName = symmetryNames[userChoice]

    generateUniqueSolution(selectedBoard, selectedBoardName)

    # 唯一解の生成


if __name__ == "__main__":
    startTime = time.time()
    isSolved = main()
    endTime = time.time()
    generationTime = endTime - startTime
    print(f"生成時間: {generationTime:.2f}秒")
