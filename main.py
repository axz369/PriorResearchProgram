import time
import json
import random
import string
from pulp import LpProblem, LpVariable, LpMinimize, lpSum, LpStatus


def convertToNumber(board, maxNumber):  # ユーザ入力の文字を数値に変換する関数
    # maxNumber種類(9種類)のアルファベットを格納する辞書
    charToNumberMap = {}
    # 数値に変換後の盤面
    boardConvertedToNumber = [[0 for _ in range(maxNumber)] for _ in range(maxNumber)]

    # 数値に変換後の配列を作る
    for row in range(len(board)):  # 行の繰り返し
        for col in range(len(board[row])):  # 列の繰り返し
            cellValue = board[row][col]

            # もし0ならスキップ
            if cellValue == "0":
                continue

            # もしすでに見つかっている文字であればスキップ
            if cellValue in charToNumberMap:
                continue

            # 左上から順に探索して見つかった順に数値を割り当てる
            charToNumberMap[cellValue] = len(charToNumberMap) + 1

    # 配列の要素数がmaxNumberに達していないなら別のランダムな文字を割り振る
    if len(charToNumberMap) < maxNumber:
        # charToNumberMapがmaxNumberの値と同じになるまで繰り返し
        while len(charToNumberMap) != maxNumber:
            # 既に割り当てられている以外の値をcharToNumberMapに入れていく
            randomUppercaseLetter = random.choice(string.ascii_uppercase)
            if randomUppercaseLetter in charToNumberMap:
                continue
            charToNumberMap[randomUppercaseLetter] = len(charToNumberMap) + 1

    # 盤面を数値に変換する
    for row in range(len(board)):  # 行の繰り返し
        for col in range(len(board[row])):  # 列の繰り返し
            cellValue = board[row][col]
            if cellValue == "0":
                boardConvertedToNumber[row][col] = 0
            else:
                boardConvertedToNumber[row][col] = charToNumberMap[cellValue]

    # charToNumberMap辞書と数値に変換後の盤面を返す
    return {
        "charToNumberMap": charToNumberMap,
        "boardConvertedToNumber": boardConvertedToNumber
    }


def formulateSudoku(board, maxNumber):  # 定式化
    # オブジェクト作成
    problem = LpProblem("SudokuProblem", LpMinimize)

    # 各セルにどの数字が入るかを表すバイナリの決定変数
    # choices[row][col][num]が1ならこのセルにnumが入る. 0ならnumは入らない
    choices = LpVariable.dicts("Choice", (range(maxNumber), range(maxNumber), range(1, maxNumber + 1)), 0, 1, cat="Binary")

    # 与えられた値をそのまま使用する制約を追加
    for row in range(maxNumber):
        for col in range(maxNumber):
            if board[row][col] != 0:  # もし初期盤面の該当セルに値が入っていたら
                problem += choices[row][col][board[row][col]] == 1  # (row, col）に数字board[row][col]が入るという制約を追加

    # 各行に同じ値が入らない制約
    for row in range(maxNumber):
        for num in range(1, maxNumber + 1):
            problem += lpSum([choices[row][col][num] for col in range(maxNumber)]) == 1

    # 各列に同じ値が入らない制約
    for col in range(maxNumber):
        for num in range(1, maxNumber + 1):
            problem += lpSum([choices[row][col][num] for row in range(maxNumber)]) == 1

    # 各サブブロックに同じ値が入らない制約
    subBlockSize = int(maxNumber ** 0.5)
    for subBlockRow in range(subBlockSize):
        for subBlockCol in range(subBlockSize):
            for num in range(1, maxNumber + 1):
                problem += lpSum([choices[row][col][num]
                                  for row in range(subBlockRow * subBlockSize, (subBlockRow + 1) * subBlockSize)
                                  for col in range(subBlockCol * subBlockSize, (subBlockCol + 1) * subBlockSize)]) == 1

    # 各セルに1つの値が入る制約
    for row in range(maxNumber):
        for col in range(maxNumber):
            problem += lpSum([choices[row][col][num] for num in range(1, maxNumber + 1)]) == 1

    # 目的関数なし
    problem += 0
    return problem, choices


def canBePlaced(board, currentPosition, x, maxNumber):  # 特定の位置に特定の数字が配置可能かどうかをチェックする関数
    subBlockSize = int(maxNumber ** 0.5)
    rows = currentPosition // maxNumber  # 行を計算
    columns = currentPosition % maxNumber  # 列を計算

    # 行と列に同じ数字がないかチェック
    for i in range(maxNumber):
        if board[rows][i] == x or board[i][columns] == x:
            return False

    # サブブロックに同じ数字がないかチェック
    topLeftCellOfSubblock = (rows // subBlockSize) * subBlockSize
    for i in range(subBlockSize):
        for j in range(subBlockSize):
            if board[topLeftCellOfSubblock + i][(columns // subBlockSize) * subBlockSize + j] == x:
                return False

    return True


def validation(charToNumberMap, board, maxNumber):  # 入力盤面の正当性チェック
    subBlockSize = int(maxNumber ** 0.5)

    # 同じ行の値が重複していないか
    for row in range(maxNumber):
        row_values = [val for val in board[row] if val != 0]
        if len(set(row_values)) != len(row_values):
            print("validation失敗 : 同じ行内の重複")
            return False

    # 同じ列の値が重複していないか
    for col in range(maxNumber):
        col_values = [board[row][col] for row in range(maxNumber) if board[row][col] != 0]
        if len(set(col_values)) != len(col_values):
            print("validation失敗 : 同じ列内の重複")
            return False

    # 同じブロックの値が重複していないか
    for subBlockRow in range(subBlockSize):
        for subBlockCol in range(subBlockSize):
            block_values = []
            for row in range(subBlockSize):
                for col in range(subBlockSize):
                    cell_value = board[subBlockRow * subBlockSize + row][subBlockCol * subBlockSize + col]
                    if cell_value != 0:
                        block_values.append(cell_value)
            if len(set(block_values)) != len(block_values):
                print("validation失敗 : 同じブロック内の重複")
                return False

    # 入力された盤面の文字の種類数がmaxNumberを超えていないか
    if (len(charToNumberMap) > maxNumber):
        print("validation失敗 : 入力された盤面の文字の種類数がmaxNumberを超えている")
        return False

    def generateSudokuSolutionBoard(solutionBoard, currentPosition):  # 解が存在するかのチェック
        # すべてのセルが埋まった場合
        if currentPosition == maxNumber * maxNumber:
            return True  # 解答が見つかったことを示す

        # 次にチェックする位置を新しい変数 newPosition に代入
        newPosition = currentPosition
        # 既に数字が埋まっているセルをスキップするループ
        while newPosition < maxNumber * maxNumber and solutionBoard[newPosition // maxNumber][newPosition % maxNumber] != 0:
            newPosition += 1

        # 1 から maxNumber までの数字をランダムに並べたリストを生成
        randomNumbers = random.sample(range(1, maxNumber + 1), maxNumber)

        # ランダムな数字のリストを順に試すループ
        for x in randomNumbers:
            # 数字 x が現在の位置 newPosition に配置可能かをチェック
            if canBePlaced(solutionBoard, newPosition, x, maxNumber):
                # 配置可能な場合、盤面に数字 x を配置
                solutionBoard[newPosition // maxNumber][newPosition % maxNumber] = x
                # 次の位置に進んで再帰的にチェックを続ける
                if generateSudokuSolutionBoard(solutionBoard, newPosition + 1):
                    return True  # 解答が見つかった場合、True を返す
                # 解答が見つからなかった場合、配置した数字をリセットして次の数字を試す
                solutionBoard[newPosition // maxNumber][newPosition % maxNumber] = 0

        # すべての数字を試しても解答が見つからなかった場合、False を返す
        return False

    # 空の盤面を用意して解が存在するかをチェック
    solutionBoard = [row[:] for row in board]  # boardのコピーを作成
    if not generateSudokuSolutionBoard(solutionBoard, 0):
        print("validation失敗 : 解が存在しない")
        return False

    return True


def generateSudoku():  # 数独パズルを生成, メインの関数
    # JSONファイルを読み込む
    with open('input.json', 'r') as file:
        data = json.load(file)

    # 使用する数独の問題を選択
    sudokuProblem = data["inputs"]["input5"]
    board = sudokuProblem["board"]
    maxNumber = sudokuProblem["maxNumber"]

    # 盤面の文字を数値に変換
    dataConvertedToNumbers = convertToNumber(board, maxNumber)
    print(dataConvertedToNumbers)

    # 入力ファイルの正当性チェック.そもそも唯一解を出せる入力なのか？
    if not validation(dataConvertedToNumbers['charToNumberMap'], dataConvertedToNumbers['boardConvertedToNumber'], maxNumber):
        print("バリデーション失敗")
        return False

    # 定式化する
    problem, choices = formulateSudoku(dataConvertedToNumbers['boardConvertedToNumber'], maxNumber)

    # 問題を解く
    problem.solve()

    # 解が見つかったかどうかを返す
    return LpStatus[problem.status] == 'Optimal'
    print(f"解の有無: {'解あり' if isSolved else '解なし'}")


startTime = time.time()
isSolved = generateSudoku()
endTime = time.time()
generationTime = endTime - startTime
print(f"生成時間: {generationTime:.2f}秒")
