def canBePlaced(board, max_number, current_position, x):
    sub_block_size = int(max_number ** 0.5)
    rows = current_position // max_number
    columns = current_position % max_number

    # 行と列に同じ数字がないかチェック
    for i in range(max_number):
        if i < len(board) and columns < len(board[i]):
            if board[i][columns] == x:
                return False
        if rows < len(board) and i < len(board[rows]):
            if board[rows][i] == x:
                return False

    # サブブロックに同じ数字がないかチェック
    top_left_cell_of_subblock = (rows // sub_block_size) * sub_block_size
    left_cell_of_subblock = (columns // sub_block_size) * sub_block_size
    for i in range(sub_block_size):
        for j in range(sub_block_size):
            if (top_left_cell_of_subblock + i < len(board) and
                    left_cell_of_subblock + j < len(board[top_left_cell_of_subblock + i])):
                if board[top_left_cell_of_subblock + i][left_cell_of_subblock + j] == x:
                    return False

    return True
