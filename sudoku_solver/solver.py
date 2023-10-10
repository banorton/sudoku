import numpy as np
import elements as el


class Solver:
    def check_validity(p: el.Puzzle):
        # Check boxs for duplicates.
        for box_num in range(1, 10):
            box = p.get_box_num(box_num).flatten()
            box = np.delete(box, np.where(box == 0)).tolist()
            if len(box) > len(set(box)):
                return 0

        # Check rows for duplicates.
        for row_num in range(9):
            row = p.get_row(row_num)
            row = np.delete(row, np.where(row == 0)).tolist()
            if len(row) > len(set(row)):
                return 0

        # Check columns for duplicates.
        for col_num in range(9):
            col = p.get_col(col_num).T
            col = np.delete(col, np.where(col == 0)).tolist()
            if len(col) > len(set(col)):
                return 0

        # Return 1 if the board state is valid.
        return 1
