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
        exit(1)

    # generateSolutionBoard関数を使用して解盤面Aを取得
    boardA = [row[:] for row in dataConvertedToNumbers['boardConvertedToNumber']]
    isSolutionGenerated = generateSolutionBoard(boardA, maxNumber)  # 解盤面Aを生成

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
