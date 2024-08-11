def getUserChoice(symmetryNames):
    while True:
        print("\nどの盤面を選びますか?")
        for i, name in enumerate(symmetryNames):
            print(f"{i+1}: {name}")

        try:
            choice = int(input("選択: ")) - 1
            if 0 <= choice < len(symmetryNames):
                return choice
            else:
                print("無効な選択です。もう一度選んでください。")
        except ValueError:
            print("無効な入力です。数字で選択してください。")
