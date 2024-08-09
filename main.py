import time
import json
from pulp import LpStatus

from modules.ConvertToNumber import ConvertToNumber
from modules.FormulateSudoku import FormulateSudoku
from modules.Validation import Validation
from modules.AddHintToLineSymmetry import AddHintToLineSymmetry


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
    symmetryAdder.addSymmetry()
    symmetricBoard = symmetryAdder.getSymmetricBoard()

    # symmetricBoardをJSON形式でsymmetric.jsonとして保存
    with open('symmetric.json', 'w', encoding='utf-8') as f:
        json.dump(symmetricBoard, f, ensure_ascii=False, indent=4)

    print("symmetric.jsonファイルが生成されました。")

    # input6を処理できないので後でAddHintToLineを書き直す

    # どの線対称にするかをランダムに選んだのでヒント数の統一はなしにする

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
