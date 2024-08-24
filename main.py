import time
import json
from pulp import LpStatus

from modules.ConvertToNumber import ConvertToNumber
from modules.Validation import Validation
from modules.AddHintToLineSymmetry import AddHintToLineSymmetry
from modules.UnifiedNumberOfHints import UnifiedNumberOfHints
from modules.GenerateUniqueSolution import GenerateUniqueSolution
from utility.displayBoards import displayBoards
from utility.getUserChoice import getUserChoice
from utility.generateSolutionBoard import generateSolutionBoard


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
    boardA = [row[:] for row in dataConvertedToNumbers['boardConvertedToNumber']]  # 元の盤面をコピー
    isSolutionGenerated = generateSolutionBoard(boardA, maxNumber)  # 解盤面Aを生成

    if not isSolutionGenerated:
        print("解盤面Aの生成に失敗しました。")
        return False
    else:
        print("解盤面Aが生成されました")
        print(boardA)

    # 対称性に基づいたヒントを追加するクラスを作成
    symmetryAdder = AddHintToLineSymmetry(dataConvertedToNumbers['boardConvertedToNumber'], boardA)

    # 4つの対称盤面を取得
    symmetricBoards = symmetryAdder.getSymmetricBoards()

    # ヒント数の統一処理
    hintUnifier = UnifiedNumberOfHints(symmetricBoards, targetHintCount=28)
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

    print(f"\n選ばれた盤面: {selectedBoardName}")

    # 唯一解の生成
    uniqueSolutionGenerator = GenerateUniqueSolution(selectedBoard, maxNumber)
    uniqueSolution = uniqueSolutionGenerator.generateUniqueSolution()

    # 唯一解が見つかったかどうかを確認
    if uniqueSolution is not None:
        print("\n唯一解が生成されました:")
        uniqueSolutionGenerator.printBoard(uniqueSolution)

        # 数字のまま保存
        with open('numberOutput.json', 'w', encoding='utf-8') as f:
            json.dump(uniqueSolution, f, ensure_ascii=False, indent=4)
        print("numberOutput.jsonファイルが生成されました。")

        # 数値から文字に変換
        uniqueSolutionAsChars = converter.convertBack(uniqueSolution)

        # JSONファイルとして保存
        with open('output.json', 'w', encoding='utf-8') as f:
            json.dump(uniqueSolutionAsChars, f, ensure_ascii=False, indent=4)

        print("output.jsonファイルが生成されました。")
    else:
        print("\n唯一解が見つかりませんでした。")

    return uniqueSolution is not None


if __name__ == "__main__":
    startTime = time.time()
    isSolved = main()
    endTime = time.time()
    generationTime = endTime - startTime
    print(f"生成時間: {generationTime:.2f}秒")
