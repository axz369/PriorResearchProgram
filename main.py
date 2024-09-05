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


#解盤面をひとつだけ生成する関数
def generateOneSolution(board):
    print("一つの解盤面生成開始")
    
    size = len(board)
    problem = pulp.LpProblem("Sudoku", pulp.LpMinimize)
    
    # 決定変数の作成
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
                                       for i in range(bi*block_size, (bi+1)*block_size) 
                                       for j in range(bj*block_size, (bj+1)*block_size)]) == 1
    
    # 5. 初期値（ヒント）の設定
    for i in range(size):
        for j in range(size):
            if board[i][j] != 0: #値が入っているセルは初期値として固定
                problem += isValueInCell[i][j][board[i][j]] == 1
    
    # 問題を解く
    problem.solve()
    
    # 整数計画問題を解いた後，その結果から数独の解を取り出す処理
    if pulp.LpStatus[problem.status] == 'Optimal':
        solution = [[0 for _ in range(size)] for _ in range(size)]
        for i in range(size):
            for j in range(size):
                for k in range(1, size + 1):
                    if pulp.value(isValueInCell[i][j][k]) == 1:
                        solution[i][j] = k
        print("一つの解盤面生成終了")
        return solution
    else:
        print("解が見つかりませんでした")
        return None






# 唯一解を生成するための関数
def generateUniqueSolution(board, boardName):
    print("唯一解生成開始")
    print(f"選ばれた盤面 : {boardName}")
    for row in board:
        print(row)
    
    #解盤面をひとつだけ生成
    solution = generateOneSolution(board)
    
    #生成された盤面の表示
    if solution:
        print("生成された解盤面:")
        for row in solution:
            print(row)
    else:
        print("解が見つかりませんでした")
    
    print("唯一解生成終了")
    return solution



















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


    generateUniqueSolution(selectedBoard,selectedBoardName)

    

    # 唯一解の生成


    


if __name__ == "__main__":
    startTime = time.time()
    isSolved = main()
    endTime = time.time()
    generationTime = endTime - startTime
    print(f"生成時間: {generationTime:.2f}秒")
