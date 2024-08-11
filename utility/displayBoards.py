def displayBoards(unifiedBoardsAsChars, symmetryNames):
    print("次の4つの盤面があります:")
    for i, name in enumerate(symmetryNames):
        print(f"\n{name}:")
        for row in unifiedBoardsAsChars[i]:
            print(" ".join(row))
