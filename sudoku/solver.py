import numpy as np
from .helpers import num_to_pos


def check_validity(puzzle):
    # Check boxs for duplicates.
    for box_num in range(1, 10):
        box_pos = num_to_pos(box_num, puzzle.puzzle_dim)
        box = puzzle.boxes.arr[box_pos[0]][box_pos[1]]
        box_cells = box.flatten().np
        box_cells = np.delete(box_cells, np.where(box_cells == 0))
        if box_cells.size > np.unique(box_cells).size:
            return 0

    # Check rows for duplicates.
    for row_num in range(9):
        row = puzzle.cells.get_row(row_num, to_np=True)
        row = np.delete(row, np.where(row == 0))
        if row.size > np.unique(row).size:
            return 0

    # Check columns for duplicates.
    for col_num in range(9):
        col = puzzle.cells.get_col(col_num, to_np=True)
        col = np.delete(col, np.where(col == 0))
        if col.size > np.unique(col).size:
            return 0

    # Return 1 if the board state is valid.
    return 1
