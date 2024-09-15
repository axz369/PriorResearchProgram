import time
import json

from modules.ConvertToNumber import ConvertToNumber
from modules.Validation import Validation
from modules.AddHintToLineSymmetry import AddHintToLineSymmetry
from modules.UnifiedNumberOfHints import UnifiedNumberOfHints
from modules.generateUniqueSolution import generateUniqueSolution

from utility.getUserChoice import getUserChoice
from utility.generateSolutionBoard import generateSolutionBoard
from utility.printBoard import printBoard


if __name__ == "__main__":

    #########################################################
    # プログラム設定
    INPUT_FILE = 'input16.json'
    INPUT_KEY = 'input1'

    if '9' in INPUT_FILE:
        MAX_SOLUTIONS = 60
        TARGET_HINT_COUNT = 28
    elif '16' in INPUT_FILE:
        MAX_SOLUTIONS = 30
        TARGET_HINT_COUNT = 100
    elif '25' in INPUT_FILE:
        MAX_SOLUTIONS = 10
        TARGET_HINT_COUNT = 200
    else:
        MAX_SOLUTIONS = 10
        TARGET_HINT_COUNT = 200
    #########################################################

    # JSONファイルを読み込む
    with open(INPUT_FILE, 'r') as file:
        data = json.load(file)

    # 使用する数独の問題を選択
    sudokuProblem = data["inputs"][INPUT_KEY]
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
        exit(1)
    else:
        print("バリデーション成功")

    # generateSolutionBoard関数を使用して解盤面Aを取得
    boardA = [row[:]
              for row in dataConvertedToNumbers['boardConvertedToNumber']]
    isSolutionGenerated = generateSolutionBoard(boardA)  # 解盤面Aを生成

    if not isSolutionGenerated:
        print("解盤面Aの生成に失敗しました。")
        exit(1)
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
    hintUnifier = UnifiedNumberOfHints(
        symmetricBoards, boardA, targetHintCount=TARGET_HINT_COUNT)
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
    uniqueSolution, numberOfHintsAdded, solutionsPerIteration = generateUniqueSolution(
        selectedBoard, selectedBoardName, MAX_SOLUTIONS)
    endTime = time.time()

    if uniqueSolution:
        print("\n******************************************")
        print("唯一解を持つ問題例(数字):")
        print("******************************************")
        printBoard(uniqueSolution)

        # 数値から文字に変換して表示
        print("\n******************************************")
        print("文字に変換された問題例(文字):")
        print("******************************************")
        printBoard(converter.convertBack(uniqueSolution))
    else:
        print("唯一解の生成に失敗しました。")

    generationTime = endTime - startTime
    print(f"生成時間: {generationTime:.2f}秒")

    # 各内部ループで生成された解の数を表示
    print("\n******************************************")
    print("各内部ループで生成された解の数:")
    print("******************************************")
    for iteration, solutions in enumerate(solutionsPerIteration, 1):
        print(f"ループ {iteration}: {solutions} 個の解が生成されました")
