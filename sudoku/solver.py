import numpy as np
from .helpers import num_to_pos


def check_validity(p):
    # Check boxs for duplicates.
    for box_num in range(1, 10):
        box_pos = num_to_pos(box_num, p.puzzle_dim)
        box = p.boxes.arr[box_pos[0]][box_pos[1]]
        box_cells = box.flatten().np
        box_cells = np.delete(box_cells, np.where(box_cells == 0))
        if box_cells.size > np.unique(box_cells).size:
            return 0

    # Check rows for duplicates.
    for row_num in range(9):
        row = p.cells.get_row(row_num).np
        row = np.delete(row, np.where(row == 0))
        if row.size > np.unique(row).size:
            return 0

    # Check columns for duplicates.
    for col_num in range(9):
        col = p.cells.get_col(col_num).np
        col = np.delete(col, np.where(col == 0))
        if col.size > np.unique(col).size:
            return 0

    # Return 1 if the board state is valid.
    return 1


def find_naked_singles(p):
    for row_num in range(9):
        for col_num in range(9):
            if len(p.cells.notes[row_num][col_num]) == 1:
                if p.cells.np[row_num, col_num] == 0:
                    num = p.cells.notes[row_num][col_num].pop()
                    p.update_cell((row_num, col_num), num)
                    print("Updating pos: ", (row_num, col_num), "to ", num)
