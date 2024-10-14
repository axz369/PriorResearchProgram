from utility.printBoard import printBoard
from utility.generateSolutionBoardP import generateSolutionBoardWrapper as generateSolutionBoardP
from utility.generateSolutionBoardG import generateSolutionBoardWrapper as generateSolutionBoardG
from modules.generateUniqueSolutionG import generateUniqueSolutionG
from modules.generateUniqueSolutionP import generateUniqueSolutionP
from modules.UnifiedNumberOfHints import UnifiedNumberOfHints
from modules.AddHintToLineSymmetry import AddHintToLineSymmetry
from modules.Validation import Validation
from modules.ConvertToNumber import ConvertToNumber
import json
import time


if __name__ == "__main__":

    #########################################################
    # プログラム設定
    INPUT_FILE = 'input9.json'
    INPUT_KEY = 'input2'
    SOLVER_TYPE = 'P'  # 'P':PuLP 'G':Gurobi

    if '9' in INPUT_FILE:
        MAX_SOLUTIONS = 3000
        TARGET_HINT_COUNT = 10
    elif '16' in INPUT_FILE:
        MAX_SOLUTIONS = 300
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
    boardA = [row[:] for row in dataConvertedToNumbers['boardConvertedToNumber']]

    # SOLVER_TYPE に基づいて解盤面Aを生成
    if SOLVER_TYPE == 'P':
        isSolutionGenerated = generateSolutionBoardP(boardA)  # PuLPを使用
    else:
        isSolutionGenerated = generateSolutionBoardG(boardA)  # Gurobiを使用

    if not isSolutionGenerated:
        print("解盤面Aの生成に失敗しました。")
        exit(1)
    else:
        print("解盤面Aが生成されました")
        printBoard(converter.convertBack(boardA))

    # 対称性に基づいたヒントを追加するクラスを作成
    symmetryAdder = AddHintToLineSymmetry(dataConvertedToNumbers['boardConvertedToNumber'], boardA)

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
    hintUnifier = UnifiedNumberOfHints(symmetricBoards, boardA, targetHintCount=TARGET_HINT_COUNT)
    unifiedBoards = hintUnifier.unifyHints()

    # ヒント数統一後の盤面を表示
    print("\n******************************************")
    print("ヒント数統一後の盤面:")
    print("******************************************")
    for symmetry_type, board in zip(symmetryTypes, unifiedBoards):
        print(f"\n{symmetry_type}Symmetry:")
        printBoard(converter.convertBack(board))

    # 4盤面から選択
    while True:
        print("\nどの盤面を選びますか?")
        for i, name in enumerate(symmetryTypes):
            print(f"{i + 1}: {name}Symmetry")

        try:
            choice = int(input("選択: ")) - 1
            if 0 <= choice < len(symmetryTypes):
                selectedBoard = unifiedBoards[choice]
                selectedBoardName = f"{symmetryTypes[choice]}Symmetry"
                break
            else:
                print("無効な選択です。もう一度選んでください。")
        except ValueError:
            print("無効な入力です。数字で選択してください。")

    print(f"選ばれた盤面 : {selectedBoardName}")
    printBoard(selectedBoard)

    # 唯一解の生成
    # 唯一解生成の実行
    startTime = time.time()
    if SOLVER_TYPE == 'G':
        uniqueSolution, numberOfHintsAdded, solutionsPerIteration = generateUniqueSolutionG(selectedBoard, MAX_SOLUTIONS)
    else:
        uniqueSolution, numberOfHintsAdded, solutionsPerIteration = generateUniqueSolutionP(selectedBoard, MAX_SOLUTIONS)
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

    print("\n******************************************")
    print("記録用")
    print("******************************************")
    print(f"{generationTime:.2f}")
    # 解が1つだけの場合は除外する
    solutions_list = [solutions for solutions in solutionsPerIteration if solutions > 1]
    print(f"{len(solutions_list)}{solutions_list}")
