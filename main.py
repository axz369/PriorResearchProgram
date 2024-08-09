import time
import json
from pulp import LpStatus


from modules.ConvertToNumber import ConvertToNumber
from modules.FormulateSudoku import FormulateSudoku
from modules.CanBePlaced import CanBePlaced
from modules.Validation import Validation


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

    # 定式化する
    sudokuFormulator = FormulateSudoku(
        dataConvertedToNumbers['boardConvertedToNumber'], maxNumber)
    problem, choices = sudokuFormulator.getProblemAndChoices()

    # 問題を解く
    problem.solve()

    # 解が見つかったかどうかを返す
    return LpStatus[problem.status] == 'Optimal'


if __name__ == "__main__":
    startTime = time.time()
    isSolved = main()
    endTime = time.time()
    generationTime = endTime - startTime
    print(f"生成時間: {generationTime:.2f}秒")
