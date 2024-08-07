import time
import json
import random
import string
from pulp import LpProblem, LpVariable, LpMinimize, lpSum, LpStatus



# ユーザ入力の文字を数値に変換する関数
def convertToNumber(board, maxNumber):
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

    # もしcharToNumberMapの要素数がmaxValueの値を超えていたら前提としてアウト
    if len(charToNumberMap) > maxNumber:
        print("文字の種類数がmaxNumberの数より多いため処理不可")

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






# 定式化
def formulateSudoku(board, maxNumber):
    # オブジェクト作成
    problem = LpProblem("SudokuProblem", LpMinimize)

    # 各セルにどの数字が入るかを表すバイナリの決定変数
    # choices[row][col][num]が1ならこのセルにnumが入る. 0ならnumは入らない
    choices = LpVariable.dicts("Choice", (range(maxNumber), range(maxNumber), range(1, maxNumber + 1)), 0, 1, cat="Binary")

    # 与えられた値をそのまま使用する制約を追加
    for row in range(maxNumber):
        for col in range(maxNumber):
            if board[row][col] != 0: # もし初期盤面の該当セルに値が入っていたら
                problem += choices[row][col][board[row][col]] == 1 # (row, col）に数字board[row][col]が入るという制約を追加

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






#def validation(board):   
# okなら1 ngなら0を返却






# 数独パズルを生成, メインの関数
def generateSudoku():
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


    # 定式化する

    # ファイル分けたい

    # 入力ファイルの正当性チェック.そもそも唯一解を出せる入力なのか？
    # if(validation(dataConvertedToNumbers) == 0)処理を終了

    # 対象位置へのヒント配列処理

    # 配置ヒント数の統一処理

    # 唯一解への調整処理



startTime = time.time()
generateSudoku()
endTime = time.time()
generationTime = endTime - startTime
print(f"生成時間: {generationTime:.2f}秒")
