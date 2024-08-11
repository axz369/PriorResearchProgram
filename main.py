import time
import json
from pulp import LpStatus

from modules.ConvertToNumber import ConvertToNumber
from modules.Validation import Validation
from modules.AddHintToLineSymmetry import AddHintToLineSymmetry
from modules.UnifiedNumberOfHints import UnifiedNumberOfHints  # クラスをインポート


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
    print(dataConvertedToNumbers)

    # Validationクラスを使用して入力ファイルの正当性チェック
    validator = Validation(
        dataConvertedToNumbers['charToNumberMap'], dataConvertedToNumbers['boardConvertedToNumber'], maxNumber)
    if not validator.check():
        print("バリデーション失敗")
        return False

    # 線対称にヒントを追加
    symmetryAdder = AddHintToLineSymmetry(
        dataConvertedToNumbers['boardConvertedToNumber'])
    symmetricBoards = symmetryAdder.getSymmetricBoards()  # 4つの対称盤面を取得
    print(symmetricBoards)

    # ヒント数の統一処理
    hintUnifier = UnifiedNumberOfHints(symmetricBoards, targetHintCount=28)
    unifiedBoards = hintUnifier.unifyHints()

    # 確認のためファイルを作る
    # 対称性の名前
    symmetryNames = ["horizontalSymmetry", "verticalSymmetry",
                     "diagonalSymmetry", "antiDiagonalSymmetry"]
    # 盤面を辞書形式で保存
    unifiedBoardsDict = {}
    for i, board in enumerate(unifiedBoards):
        unifiedBoardsDict[symmetryNames[i]] = board
    # unifiedBoardsDictをJSON形式でunified_symmetric.jsonとして保存
    with open('unified_symmetric.json', 'w', encoding='utf-8') as f:
        json.dump(unifiedBoardsDict, f, ensure_ascii=False, indent=4)

    print("unified_symmetric.jsonファイルが生成されました。")

    # ユーザに見せて一つ選ばせるときは文字に変換してから

    # 定式化する
    # sudokuFormulator = FormulateSudoku(
    #    dataConvertedToNumbers['boardConvertedToNumber'], maxNumber)
    # problem, choices = sudokuFormulator.getProblemAndChoices()

    # 問題を解く
    # problem.solve()

    # 解が見つかったかどうかを返す
    # return LpStatus[problem.status] == 'Optimal'


if __name__ == "__main__":
    startTime = time.time()
    isSolved = main()
    endTime = time.time()
    generationTime = endTime - startTime
    print(f"生成時間: {generationTime:.2f}秒")
